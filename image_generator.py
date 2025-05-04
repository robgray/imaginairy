from diffusers import DiffusionPipeline
import torch
import os
from flask import json
from prompt import Prompt

TEMP_PATH = 'static/temp-images/'

def is_generated(request_id):
    return os.path.exists(TEMP_PATH + 'image-' + request_id + '.png')

def setup():
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)

# Generate the image
def generate(prompt: Prompt):
    print(prompt.get_prompt_text())

    pipe = DiffusionPipeline.from_pretrained(
        prompt.model_path, torch_dtype=torch.float16,
        safety_checker=None, use_safetensors=False
    )
    pipe.to("cuda")

    # Need generator (with seed) for a consistent image given a prompt
    generator = torch.Generator(device="cuda").manual_seed(int(prompt.seed))

    image = pipe(
        prompt=prompt.get_prompt_text(),
        negative_prompt=prompt.negative_prompt,
        num_inference_steps=int(prompt.inference_steps),
        height=int(prompt.resolution[1]),
        width=int(prompt.resolution[0]),
        guidance_scale=float(prompt.guidance_scale),
        generator=generator,
    ).images[0]

    image_filename = TEMP_PATH + 'image-' + prompt.request_id + '.png'
    image.save(image_filename)

    # Return the filename
    return image_filename

def save_temp_prompt(prompt: Prompt):
    try:
        filename = TEMP_PATH + prompt.request_id + '.json'
        with open(filename, 'w') as f:
            json.dump(prompt.to_json(), f, indent=4)
        return filename
    except Exception as e:
        print(f"Error saving prompt to file: {e}")
        return None
