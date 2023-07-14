import os
import boto3
import pathlib


# Info for generator
additional_prompt = " recipe photo, professional photo, restaurant like," \
                    " high resolution, professional food photography, colourful food, realistic photo"
stable_diffusion_path = "/home/ubuntu/stable-diffusion"
model_name = "v1-5-pruned-emaonly.ckpt"
txt2img_path = "scripts/txt2img.py"
outputs_path = "outputs/txt2img-samples"
full_outputs_path = "home/ubuntu/stable-diffusion/outputs/txt2img-samples"


def generate_image(image_name: str, additional_prompt: str = additional_prompt) -> str:
    """
    Generates image via stable diffusion.
    Return: the name of the file that was generated. The actual generated image
    is stored in the "file_name/samples/00000.png".
    """
    image_name = image_name.replace("\n", "")
    prompt = image_name + additional_prompt
    file_name = image_name.replace(' ', '_').lower()
    
    os.chdir(stable_diffusion_path)
    command = f'python {txt2img_path} --prompt "{prompt}" --plms --ckpt {model_name} --n_samples 1 --skip_grid --outdir {outputs_path}/{file_name} --n_iter 1'
    executed = os.system(command)
    
    return file_name
