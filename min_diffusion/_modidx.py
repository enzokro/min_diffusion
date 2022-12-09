# Autogenerated by nbdev

d = { 'settings': { 'branch': 'main',
                'doc_baseurl': '/min_diffusion',
                'doc_host': 'https://enzokro.github.io',
                'git_url': 'https://github.com/enzokro/min_diffusion',
                'lib_path': 'min_diffusion'},
  'syms': { 'min_diffusion.core': { 'min_diffusion.core.MinimalDiffusion': ('core.html#minimaldiffusion', 'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.__init__': ( 'core.html#minimaldiffusion.__init__',
                                                                                      'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.diffuse_step': ( 'core.html#minimaldiffusion.diffuse_step',
                                                                                          'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.encode_text': ( 'core.html#minimaldiffusion.encode_text',
                                                                                         'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.generate': ( 'core.html#minimaldiffusion.generate',
                                                                                      'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.get_initial_latents': ( 'core.html#minimaldiffusion.get_initial_latents',
                                                                                                 'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.image_from_latents': ( 'core.html#minimaldiffusion.image_from_latents',
                                                                                                'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.k_sampling_loop': ( 'core.html#minimaldiffusion.k_sampling_loop',
                                                                                             'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.load': ( 'core.html#minimaldiffusion.load',
                                                                                  'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.load_scheduler': ( 'core.html#minimaldiffusion.load_scheduler',
                                                                                            'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.load_text_pieces': ( 'core.html#minimaldiffusion.load_text_pieces',
                                                                                              'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.load_unet': ( 'core.html#minimaldiffusion.load_unet',
                                                                                       'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.load_vae': ( 'core.html#minimaldiffusion.load_vae',
                                                                                      'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.set_initial_latents': ( 'core.html#minimaldiffusion.set_initial_latents',
                                                                                                 'min_diffusion/core.py'),
                                    'min_diffusion.core.MinimalDiffusion.to_device': ( 'core.html#minimaldiffusion.to_device',
                                                                                       'min_diffusion/core.py')},
            'min_diffusion.kdiff': { 'min_diffusion.kdiff.CFGDenoiser': ('kdiff.html#cfgdenoiser', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.CFGDenoiser.__init__': ( 'kdiff.html#cfgdenoiser.__init__',
                                                                                   'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.CFGDenoiser.forward': ( 'kdiff.html#cfgdenoiser.forward',
                                                                                  'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.CFGDenoiser.get_noise_prediction': ( 'kdiff.html#cfgdenoiser.get_noise_prediction',
                                                                                               'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.DPM2AncestralSampler': ( 'kdiff.html#dpm2ancestralsampler',
                                                                                   'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.DPM2Sampler': ('kdiff.html#dpm2sampler', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.DPMAdaptiveSampler': ('kdiff.html#dpmadaptivesampler', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.DPMFastSampler': ('kdiff.html#dpmfastsampler', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.DPMPP2MSampler': ('kdiff.html#dpmpp2msampler', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.DPMPP2SAncestralSampler': ( 'kdiff.html#dpmpp2sancestralsampler',
                                                                                      'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.DPMPPSDESampler': ('kdiff.html#dpmppsdesampler', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.EulerAncestralSampler': ( 'kdiff.html#eulerancestralsampler',
                                                                                    'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.EulerSampler': ('kdiff.html#eulersampler', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.HeunSampler': ('kdiff.html#heunsampler', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.ImageSampler': ('kdiff.html#imagesampler', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.ImageSampler.__init__': ( 'kdiff.html#imagesampler.__init__',
                                                                                    'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.KDiffusionNames': ('kdiff.html#kdiffusionnames', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.KDiffusionSampler': ('kdiff.html#kdiffusionsampler', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.KDiffusionSampler.__init__': ( 'kdiff.html#kdiffusionsampler.__init__',
                                                                                         'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.KDiffusionSampler.sample': ( 'kdiff.html#kdiffusionsampler.sample',
                                                                                       'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.LMSSampler': ('kdiff.html#lmssampler', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.ModelWrapper': ('kdiff.html#modelwrapper', 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.ModelWrapper.__init__': ( 'kdiff.html#modelwrapper.__init__',
                                                                                    'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.ModelWrapper.apply_model': ( 'kdiff.html#modelwrapper.apply_model',
                                                                                       'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.WrappedCompVisDenoiser': ( 'kdiff.html#wrappedcompvisdenoiser',
                                                                                     'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.WrappedCompVisDenoiser.apply_model': ( 'kdiff.html#wrappedcompvisdenoiser.apply_model',
                                                                                                 'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.WrappedCompVisVDenoiser': ( 'kdiff.html#wrappedcompvisvdenoiser',
                                                                                      'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.WrappedCompVisVDenoiser.apply_model': ( 'kdiff.html#wrappedcompvisvdenoiser.apply_model',
                                                                                                  'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.sample_dpm_adaptive': ( 'kdiff.html#sample_dpm_adaptive',
                                                                                  'min_diffusion/kdiff.py'),
                                     'min_diffusion.kdiff.sample_dpm_fast': ('kdiff.html#sample_dpm_fast', 'min_diffusion/kdiff.py')},
            'min_diffusion.utils': { 'min_diffusion.utils.get_device': ('utils.html#get_device', 'min_diffusion/utils.py'),
                                     'min_diffusion.utils.image_grid': ('utils.html#image_grid', 'min_diffusion/utils.py'),
                                     'min_diffusion.utils.maybe_add_batch_dim': ( 'utils.html#maybe_add_batch_dim',
                                                                                  'min_diffusion/utils.py'),
                                     'min_diffusion.utils.plot_grid': ('utils.html#plot_grid', 'min_diffusion/utils.py'),
                                     'min_diffusion.utils.show_image': ('utils.html#show_image', 'min_diffusion/utils.py')}}}
