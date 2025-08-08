from PIL.Image import Image
from diffusers import DiffusionPipeline, StableDiffusionUpscalePipeline, DPMSolverMultistepScheduler
from typing import Optional

_current_pipe: Optional[DiffusionPipeline] = None
import torch
import os
from flask import json
from numpy.f2py.auxfuncs import throw_error

from prompt import Prompt

TEMP_PATH = 'static/temp-images/'

def is_generated(request_id):
    return os.path.exists(TEMP_PATH + 'image-' + request_id + '.png')

def setup():
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)

def get_pipeline(model_path: str) -> DiffusionPipeline:
    global _current_pipe

    if _current_pipe is None or _current_pipe.config['_name_or_path'] != model_path:
        if not torch.cuda.is_available():
            throw_error("CUDA is not available")

        _current_pipe = DiffusionPipeline.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            safety_checker=None,
            use_safetensors=False,
        )
        _current_pipe.safety_checker = None
        _current_pipe.scheduler = DPMSolverMultistepScheduler.from_config(_current_pipe.scheduler.config)
        _current_pipe.to("cuda")

    return _current_pipe

# Generate the image
def generate(prompt: Prompt):
    if not torch.cuda.is_available():
        throw_error("CUDA is not available")

    pipe = get_pipeline(prompt.model_path)

    try:
        # Need generator (with seed) for a consistent image given a prompt
        generator = torch.Generator(device="cuda").manual_seed(int(prompt.seed))

        output = pipe(
            prompt=prompt.get_prompt_text(),
            negative_prompt=prompt.negative_prompt,
            num_inference_steps=int(prompt.inference_steps),
            height=int(prompt.resolution[1]),
            width=int(prompt.resolution[0]),
            guidance_scale=float(prompt.guidance_scale),
            num_images_per_prompt=1,
            generator=generator,
        )

        ad_images = output.images
        image = ad_images[0]

        image_filename = TEMP_PATH + 'image-' + prompt.request_id + '.png'

        if prompt.upscale_small_images and prompt.resolution[0] <= 512 and prompt.resolution[1] <= 512:
            print('Upscaling image')
            try:
                image_upscaled = upscale(prompt, image)
                image_upscaled.save(image_filename)
                return image_filename
            except Exception as e:
                print(f"Error upscaling image: {e}")

        # Save standard image
        image.save(image_filename)
        return image_filename

    except Exception as e:
        print(e)
        throw_error(e)


def save_temp_prompt(prompt: Prompt):
    try:
        filename = TEMP_PATH + prompt.request_id + '.json'
        with open(filename, 'w') as f:
            json.dump(prompt.to_json(), f, indent=4)
        return filename
    except Exception as e:
        print(f"Error saving prompt to file: {e}")
        return None


def upscale(prompt: Prompt, image: Image):
    if not torch.cuda.is_available():
        throw_error("CUDA is not available")

    pipe = StableDiffusionUpscalePipeline.from_pretrained(
        "stabilityai/stable-diffusion-x4-upscaler",
        torch_dtype=torch.float16,
        use_safetensors=True
    ).to("cuda")

    if prompt.use_memory_efficient:
        pipe.enable_attention_slicing()

    generator = torch.Generator(device="cuda").manual_seed(int(prompt.seed))

    with torch.no_grad():
        image_upscaled = pipe(
            prompt=prompt.get_prompt_text(),
            negative_prompt=prompt.negative_prompt,
            guidance_scale=float(prompt.guidance_scale),
            num_inference_steps=int(prompt.inference_steps),
            image=image,
            generator=generator,
        ).images[0]

    torch.cuda.empty_cache()

    return image_upscaled