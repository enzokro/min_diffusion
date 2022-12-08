# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_kdiff.ipynb.

# %% auto 0
__all__ = ['SAMPLERS', 'SAMPLER_LOOKUP', 'ImageSampler', 'ModelWrapper', 'WrappedCompVisDenoiser', 'WrappedCompVisVDenoiser',
           'KDiffusionNames', 'CFGDenoiser', 'KDiffusionSampler', 'sample_dpm_adaptive', 'sample_dpm_fast',
           'DPMFastSampler', 'DPMAdaptiveSampler', 'DPM2Sampler', 'DPM2AncestralSampler', 'DPMPP2MSampler',
           'DPMPPSDESampler', 'DPMPP2SAncestralSampler', 'EulerSampler', 'EulerAncestralSampler', 'HeunSampler',
           'LMSSampler']

# %% ../nbs/02_kdiff.ipynb 2
# imports for diffusion models
from abc import ABC
import importlib
from PIL import Image
import torch
from tqdm    import tqdm
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers    import AutoencoderKL, UNet2DConditionModel
from diffusers    import LMSDiscreteScheduler, EulerDiscreteScheduler, DPMSolverMultistepScheduler, EulerAncestralDiscreteScheduler
import torch
from torch import nn
from . import utils
try:
    from k_diffusion.external import CompVisDenoiser, CompVisVDenoiser
    from k_diffusion.sampling import get_sigmas_karras
    import k_diffusion.sampling as k_sampling
except:
    print(f'WARNING: Could not import k_diffusion')

# %% ../nbs/02_kdiff.ipynb 4
class ImageSampler(ABC):
    short_name: str
    name: str
    default_steps: int
    default_size: int

    def __init__(self, model):
        self.model = model
        self.device = utils.get_device()
        
        
class ModelWrapper:
    def __init__(self, model, alphas_cumprod):
        self.model = model
        self.alphas_cumprod = alphas_cumprod

    def apply_model(self, *args, **kwargs):
        return self.model(*args, **kwargs).sample
        
        
class WrappedCompVisDenoiser(CompVisDenoiser):
    """Short wrapping for more general calls to `apply_model`.
    """
    def apply_model(self, *args, **kwargs):
        return self.inner_model.apply_model(*args, **kwargs)


class WrappedCompVisVDenoiser(CompVisVDenoiser):
    """Short wrapping for more general calls to `apply_model`.
    """
    def apply_model(self, *args, **kwargs):
        return self.inner_model.apply_model(*args, **kwargs)

    

class KDiffusionNames:
    # PLMS = "plms"
    # DDIM = "ddim"
    K_DPM_FAST           = "k_dpm_fast"
    K_DPM_ADAPTIVE       = "k_dpm_adaptive"
    K_LMS                = "k_lms" 
    K_DPM_2              = "k_dpm_2"
    K_DPM_2_ANCESTRAL    = "k_dpm_2_a"
    K_DPMPP_2M           = "k_dpmpp_2m"
    K_DPMPP_2S_ANCESTRAL = "k_dpmpp_2s_a"
    K_EULER              = "k_euler"
    K_EULER_ANCESTRAL    = "k_euler_a"
    K_HEUN               = "k_heun"
    K_DPMPP_SDE          = 'k_dpmpp_sde'
    
    
    


# %% ../nbs/02_kdiff.ipynb 6
class CFGDenoiser(nn.Module):
    """Runs Classifier-free Guidance with optional schedules and normalizations.
    """
    def __init__(self, model, guide_tfm=None):
        super().__init__()
        self.inner_model = model
        self.guide_tfm = guide_tfm
        self.device = utils.get_device()

    def forward(
        self,
        x,
        sigma,
        uncond,
        cond,
        mask=None,
        mask_noise=None,
        orig_latent=None,
        g_idxs=None,
    ):
        def _wrapper(noisy_latent_in, time_encoding_in, conditioning_in):
            return self.inner_model(
                noisy_latent_in, time_encoding_in, cond=conditioning_in
            )

        noise_pred = self.get_noise_prediction(
            denoise_func=_wrapper,
            noisy_latent=x,
            time_encoding=sigma,
            uncond=uncond,
            cond=cond,
            g_idxs=g_idxs,
        )
        return noise_pred
    
    def get_noise_prediction(
        self,
        denoise_func,
        noisy_latent,
        time_encoding,
        uncond,
        cond,
        g_idxs,
    ):
        # pad the latent with batch dimensions if needed
        noisy_latent = utils.maybe_add_batch_dim(noisy_latent)
        
        # prepare the noisy latents for conditional and unconditional inputs
        noisy_latent_in = torch.cat([noisy_latent] * 2)
        time_encoding_in = torch.cat([time_encoding] * 2)

        # prepare the unconditional and conditional prompts
        text_embeds = torch.cat([uncond, cond])

        # the k-diffusion samplers actually return the denoised predicted latents but things seem
        # to work anyway
        noise_pred_neutral, noise_pred_positive = denoise_func(
            noisy_latent_in, time_encoding_in, text_embeds
        ).chunk(2)
    
        # run the guidance scheduler and normalization
        noise_pred = self.guide_tfm(noise_pred_neutral, noise_pred_positive, next(g_idxs))

        return noise_pred

# %% ../nbs/02_kdiff.ipynb 8
class KDiffusionSampler(ImageSampler, ABC):
    sampler_func: callable

    def __init__(self, model, model_name):
        super().__init__(model)
        # TODO: better handling for model names
        denoiseer_cls = (
            WrappedCompVisVDenoiser
            if model_name.split('/')[-1] in ('stable-diffusion-2', 'stable-diffusion-2-1')
            else WrappedCompVisDenoiser
        )
        self.cv_denoiser = denoiseer_cls(model)

    def sample(
        self,
        num_steps,
        shape,
        neutral_conditioning,
        positive_conditioning,
        batch_size=1,
        mask=None,
        orig_latent=None,
        initial_latent=None,
        t_start=None,
        guide_tfm=None,
        use_karras_sigmas=True,
    ):

        if initial_latent is None:
            initial_latent = torch.randn(shape, device="cpu").to(self.device)

        #log_latent(initial_latent, "initial_latent")
        if t_start is not None:
            t_start = num_steps - t_start + 1
        
        if use_karras_sigmas:
            print(f'Using Karras sigma schedule')
            sigmas = k_sampling.get_sigmas_karras(n=num_steps, sigma_min=0.1, sigma_max=10, device=self.device)
        else:
            sigmas = self.cv_denoiser.get_sigmas(num_steps)[t_start:]
        
        # build timestep iterator for schedules
        g_idxs = []
        for i in range(len(sigmas)):
            if 'sde' or '2s_a' or 'dpm_2' in self.short_name:
                g_idxs.extend([i,i])
            else:
                g_idxs.append(i)
        g_idxs = iter(g_idxs)

        # if our number of steps is zero, just return the initial latent
        if sigmas.nelement() == 0:
            if orig_latent is not None:
                return orig_latent
            return initial_latent

        x = initial_latent * sigmas[0]
        #log_latent(x, "initial_sigma_noised_tensor")
        model_wrap_cfg = CFGDenoiser(self.cv_denoiser, guide_tfm=guide_tfm)

        mask_noise = None
        if mask is not None:
            mask_noise = torch.randn_like(initial_latent, device="cpu").to(
                initial_latent.device
            )

        samples = self.sampler_func(
            model=model_wrap_cfg,
            x=x,
            sigmas=sigmas,
            extra_args={
                "cond": positive_conditioning,
                "uncond": neutral_conditioning,
                "mask": mask,
                "mask_noise": mask_noise,
                "orig_latent": orig_latent,
                "g_idxs": g_idxs,
            },
            disable=False,
            #callback=callback,
        )

        return samples

# %% ../nbs/02_kdiff.ipynb 10
def sample_dpm_adaptive(
    model, x, sigmas, extra_args=None, disable=False, callback=None
):
    sigma_min = sigmas[-2]
    sigma_max = sigmas[0]
    return k_sampling.sample_dpm_adaptive(
        model=model,
        x=x,
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        extra_args=extra_args,
        disable=disable,
        callback=callback,
    )


def sample_dpm_fast(model, x, sigmas, extra_args=None, disable=False, callback=None):
    sigma_min = sigmas[-2]
    sigma_max = sigmas[0]
    return k_sampling.sample_dpm_fast(
        model=model,
        x=x,
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        n=len(sigmas),
        extra_args=extra_args,
        disable=disable,
        callback=callback,
    )

class DPMFastSampler(KDiffusionSampler):
    short_name = KDiffusionNames.K_DPM_FAST
    name = "Diffusion probabilistic models - fast"
    default_steps = 15
    sampler_func = staticmethod(sample_dpm_fast)


class DPMAdaptiveSampler(KDiffusionSampler):
    short_name = KDiffusionNames.K_DPM_ADAPTIVE
    name = "Diffusion probabilistic models - adaptive"
    default_steps = 40
    sampler_func = staticmethod(sample_dpm_adaptive)


class DPM2Sampler(KDiffusionSampler):
    short_name = KDiffusionNames.K_DPM_2
    name = "Diffusion probabilistic models - 2"
    default_steps = 40
    sampler_func = staticmethod(k_sampling.sample_dpm_2)


class DPM2AncestralSampler(KDiffusionSampler):
    short_name = KDiffusionNames.K_DPM_2_ANCESTRAL
    name = "Diffusion probabilistic models - 2 ancestral"
    default_steps = 40
    sampler_func = staticmethod(k_sampling.sample_dpm_2_ancestral)


class DPMPP2MSampler(KDiffusionSampler):
    short_name = KDiffusionNames.K_DPMPP_2M
    name = "Diffusion probabilistic models - 2m"
    default_steps = 15
    sampler_func = staticmethod(k_sampling.sample_dpmpp_2m)
    
    
class DPMPPSDESampler(KDiffusionSampler):
    short_name = KDiffusionNames.K_DPMPP_SDE
    name = "Diffusion probabilistic models - 2m"
    default_steps = 30
    sampler_func = staticmethod(k_sampling.sample_dpmpp_sde)


class DPMPP2SAncestralSampler(KDiffusionSampler):
    short_name = KDiffusionNames.K_DPMPP_2S_ANCESTRAL
    name = "Ancestral sampling with DPM-Solver++(2S) second-order steps."
    default_steps = 15
    sampler_func = staticmethod(k_sampling.sample_dpmpp_2s_ancestral)


class EulerSampler(KDiffusionSampler):
    short_name = KDiffusionNames.K_EULER
    name = "Algorithm 2 (Euler steps) from Karras et al. (2022)"
    default_steps = 40
    sampler_func = staticmethod(k_sampling.sample_euler)


class EulerAncestralSampler(KDiffusionSampler):
    short_name = KDiffusionNames.K_EULER_ANCESTRAL
    name = "Euler ancestral"
    default_steps = 40
    sampler_func = staticmethod(k_sampling.sample_euler_ancestral)


class HeunSampler(KDiffusionSampler):
    short_name = KDiffusionNames.K_HEUN
    name = "Algorithm 2 (Heun steps) from Karras et al. (2022)."
    default_steps = 40
    sampler_func = staticmethod(k_sampling.sample_heun)


class LMSSampler(KDiffusionSampler):
    short_name = KDiffusionNames.K_LMS
    name = "LMS"
    default_steps = 40
    sampler_func = staticmethod(k_sampling.sample_lms)

    
    
SAMPLERS = [
    DPMFastSampler,
    DPMAdaptiveSampler,
    LMSSampler,
    DPM2Sampler,
    DPM2AncestralSampler,
    DPMPP2MSampler,
    DPMPPSDESampler,
    DPMPP2SAncestralSampler,
    EulerSampler,
    EulerAncestralSampler,
    HeunSampler,
]

SAMPLER_LOOKUP = {sampler.short_name: sampler for sampler in SAMPLERS}



