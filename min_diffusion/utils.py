# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_utils.ipynb.

# %% auto 0
__all__ = ['show_image', 'image_grid', 'plot_schedules']

# %% ../nbs/01_utils.ipynb 2
import torch
from PIL import Image
import matplotlib.pyplot as plt
from textwrap import wrap
from typing import List

# %% ../nbs/01_utils.ipynb 3
def show_image(image, scale=0.5, plot=True):
    "Displays the given `image` resized based on `scale`."
    img = image.resize(((int)(image.width * scale), (int)(image.height * scale)))
    if plot:
        plt.figure()
        plt.imshow(img)
    #display(img)
    return img


def image_grid(images, rows = 1, width=256, height=256, title=None):
    "Display an array of images in a grid with the given number of `rows`"
    count = len(images)
    cols = int(count / rows)
    if cols * rows < count:
        rows += 1
    # Calculate fig size based on individual image sizes    
    px = 1/plt.rcParams['figure.dpi']
    w = cols * width * px
    # Add some extra space for the caption/title since that can wrap
    h = (rows * height * px) + (rows * 30 * px)
    fig, axes = plt.subplots(rows, cols, figsize=(w, h))
    for y in range(rows):
        for x in range(cols):
            index = y*cols + x
            ref = axes[x] if rows == 1 else axes[y] if cols == 1 else axes[y, x]
            ref.axis('off')
            if index > count - 1:
                continue
            img = images[index]
            txt = f'Frame: {index}'
            if title is not None:
                if isinstance(title, str):
                    txt = f'{title}: {index}'
                elif isinstance(title, List):
                    txt = title[index]
            # small change for bigger, more visible titles
            txt = '\n'.join(wrap(txt, width=70))
            ref.set_title(txt, fontsize='x-large')
            ref.imshow(img)
            ref.axis('off')
            

def plot_schedules(scheds, rows = 1, width=256, height=256, titles=None):
    "Display an array of images in a nice grid, or single row"
    count = len(scheds)
    cols = int(count / rows)
    if cols * rows < count:
        rows += 1
    # Calculate fig size based on individual image sizes    
    px = 1/plt.rcParams['figure.dpi']
    w = cols * width * px
    # Add some extra space for the caption/title since that can wrap
    h = (rows * height * px) + (rows * 30 * px)
    fig, axes = plt.subplots(rows, cols, figsize=(w, h))
    for y in range(rows):
        for x in range(cols):
            index = y*cols + x
            ref = axes[x] if rows == 1 else axes[y] if cols == 1 else axes[y, x]
            if index > count - 1:
                ref.axis('off')
                continue
            sched = scheds[index]
            txt = f'Frame: {index}'
            if titles is not None:
                if isinstance(titles, str):
                    txt = f'{titles}: {index}'
                elif isinstance(titles, List) or isinstance(titles, L):
                    txt = titles[index]
            # small change for bigger, more visible titles
            txt = '\n'.join(wrap(txt, width=30))
            ref.set_title(txt, fontsize='x-large')
            ref.plot(sched)
            #ref.axis('off')
            ref.set_xlabel('Diffusion Timesteps')
            ref.set_ylabel('Guidance Parameter')
    fig.tight_layout()
