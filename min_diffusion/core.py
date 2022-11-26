# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['MinimalDiffusion']

# %% ../nbs/00_core.ipynb 2
# imports for diffusion models
from PIL import Image
import torch
from tqdm.auto    import tqdm
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers    import AutoencoderKL, UNet2DConditionModel
from diffusers    import LMSDiscreteScheduler, EulerDiscreteScheduler

# %% ../nbs/00_core.ipynb 3
class MinimalDiffusion:
    """Loads a Stable Diffusion pipeline.
    
    The goal is to have more control of the image generation loop. 
    This class loads the following individual pieces:
        - Tokenizer
        - Text encoder
        - VAE
        - U-Net
        - Sampler
        
    The `self.generate` function uses these pieces to run a Diffusion image generation loop.
    
    This class can be subclasses and any of its methods overriden to gain even more control over the Diffusion pipeline. 
    """
    def __init__(self, model_name, device, dtype, generator=None):
        self.model_name = model_name
        self.device = device
        self.dtype = dtype
        self.generator = None 
        
        
    def load(self, unet_attn_slice=True,  better_vae=''):
        """Loads and returns the individual pieces in a Diffusion pipeline.        
        """
        # load the pieces
        self.load_text_pieces()
        self.load_vae(better_vae)
        self.load_unet(unet_attn_slice)
        self.load_scheduler()
        # put them on the device
        self.to_device()
    

    def load_text_pieces(self):
        """Creates the tokenizer and text encoder.
        """
        tokenizer = CLIPTokenizer.from_pretrained(
            self.model_name,
            subfolder="tokenizer",
            torch_dtype=self.dtype)
        text_encoder = CLIPTextModel.from_pretrained(
            self.model_name,
            subfolder="text_encoder",
            torch_dtype=self.dtype)
        self.tokenizer = tokenizer
        self.text_encoder = text_encoder
    
    
    def load_vae(self, better_vae=''):
        """Loads the Variational Auto-Encoder.
        
        Optionally loads an improved `better_vae` from the stability.ai team.
            It can be either the `ema` or `mse` VAE.
        """
        # optionally use a VAE from stability that was trained for longer 
        if better_vae:
            assert better_vae in ('ema', 'mse')
            print(f'Using the improved VAE "{better_vae}" from stabiliy.ai')
            vae = AutoencoderKL.from_pretrained(
                f"stabilityai/sd-vae-ft-{better_vae}",
                torch_dtype=self.dtype)
        else:
            vae = AutoencoderKL.from_pretrained(self.model_name, subfolder='vae',
                                                torch_dtype=self.dtype)
        self.vae = vae

        
    def load_unet(self, unet_attn_slice=True):
        """Loads the U-Net.
        
        Optionally uses attention slicing to fit on smaller GPU cards.
        """
        unet = UNet2DConditionModel.from_pretrained(
            self.model_name,
            subfolder="unet",
            torch_dtype=self.dtype)
        # optionally enable unet attention slicing
        if unet_attn_slice:
            print('Enabling default unet attention slicing.')
            slice_size = unet.config.attention_head_dim // 2
            unet.set_attention_slice(slice_size)
        self.unet = unet
        
                
    def load_scheduler(self):
        """Loads the scheduler.
        """
        if self.model_name == 'stabilityai/stable-diffusion-2':
            sched_kls = EulerDiscreteScheduler
        else:
            sched_kls = LMSDiscreteScheduler
        print(f'Using scheduler: {sched_kls}')
        scheduler = sched_kls.from_pretrained(self.model_name, 
                                              subfolder="scheduler")
        self.scheduler = scheduler 


    def generate(
        self,
        prompt,
        guide_tfm=None,
        width=512,
        height=512,
        steps=50,
        **kwargs
    ):
        """Main image generation loop.
        """
        # if no guidance transform was given, use the default update
        if guide_tfm is None:
            print('Using the default Classifier-free Guidance.')
            G = 7.5
            guide_tfm = lambda u, t, idx: u + G*(t - u)
        self.guide_tfm = guide_tfm
        
        # prepare the text embeddings
        text = self.encode_text(prompt)
        neg_prompt = kwargs.get('negative_prompt', '')
        if neg_prompt:
            print(f'Using negative prompt: {neg_prompt}')
        uncond = self.encode_text(neg_prompt)
        text_emb = torch.cat([uncond, text]).type(self.unet.dtype)
        
        # start from the shared, initial latents
        if getattr(self, 'init_latents', None) is None:
            self.init_latents = self.get_initial_latents(height, width)
            
        latents = self.init_latents.clone().to(self.unet.device)
        self.scheduler.set_timesteps(steps)
        latents = latents * self.scheduler.init_noise_sigma
        
        # run the diffusion process
        for i,ts in enumerate(tqdm(self.scheduler.timesteps)):
            latents = self.diffuse_step(latents, text_emb, ts, i)

        # decode the final latents and return the generated image
        image = self.image_from_latents(latents)
        return image    


    def diffuse_step(self, latents, text_emb, ts, idx):
        """Runs a single diffusion step.
        """
        inp = self.scheduler.scale_model_input(torch.cat([latents] * 2), ts)
        with torch.no_grad(): 
            tf = ts
            if torch.has_mps:
                tf = ts.type(torch.float32)
            preds = self.unet(inp, tf, encoder_hidden_states=text_emb)
            u, t  = preds.sample.chunk(2)
        
        # run classifier-free guidance
        pred = self.guide_tfm(u, t, idx)
        
        # update and return the latents
        latents = self.scheduler.step(pred, ts, latents).prev_sample
        return latents
    

    def encode_text(self, prompts, maxlen=None):
        """Extracts text embeddings from the given `prompts`.
        """
        maxlen = maxlen or self.tokenizer.model_max_length
        inp = self.tokenizer(prompts, padding="max_length", max_length=maxlen, 
                             truncation=True, return_tensors="pt")
        inp_ids = inp.input_ids.to(self.device)
        return self.text_encoder(inp_ids)[0]

    
    def to_device(self, device=None):
        """Places to pipeline pieces on the given device
        
        Note: assumes we keep Scheduler and Tokenizer on the cpu.
        """
        device = device or self.device
        for m in (self.text_encoder, self.vae, self.unet):
            m.to(device)
    
    
    def set_initial_latents(self, latents):
        """Sets the given `latents` as the initial noise latents.
        """
        self.init_latents = latents
        
        
    def get_initial_latents(self, height, width):
        """Returns 
        """
        return torch.randn((1, self.unet.in_channels, height//8, width//8),
                           dtype=self.dtype, generator=self.generator)
    
    
    def image_from_latents(self, latents):
        """Scales diffusion `latents` and turns them into a PIL Image.
        """
        # scale and decode the latents
        latents = 1 / 0.18215 * latents
        with torch.no_grad():
            data = self.vae.decode(latents).sample[0]
        # Create PIL image
        data = (data / 2 + 0.5).clamp(0, 1)
        data = data.cpu().permute(1, 2, 0).float().numpy()
        data = (data * 255).round().astype("uint8")
        image = Image.fromarray(data)
        return image
