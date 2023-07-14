import os
import boto3
import pathlib

# S3
client = boto3.client("s3")
s3 = boto3.resource("s3")
bucket_name = "stable-diffusion-s3bucket"

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


def save_file_to_bucket(file_name: str, path_to_file: str = full_outputs_path, bucket_name: str = bucket_name) -> bool:
    """
    Saves file to S3 bucket.
    Used only for saving images from generate_image().
    Return: True if successfully saved.
    """
    path_to_file = f"/{path_to_file}/{file_name}/samples/00000.png"
    uploaded = client.upload_file(path_to_file, bucket_name, f"{file_name}.png")
    
    if uploaded != None:
        return False
    
    return True


def get_file_url(file_name: str, expiration: int = 3600) -> str:
    """
    Generates url to access the file on the S3 bucket.
    Return: url to the file on S3 bucket.
    """
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": file_name},
        ExpiresIn=expiration
    )
    
    return url


def delete_file(path_to_file: pathlib.Path) -> bool:
    """
    Deletes a file/directory by absolute path.
    Return: True if the file exists.
    """
    if os.path.exists(path_to_file):
        for sub in path_to_file.iterdir():
            if sub.is_dir():
                delete_file(sub)
            else:
                sub.unlink()
    
        path_to_file.rmdir()
        
        return True
    
    else:
        print(f"The file {path_to_file} does not exist")
        
        return False 
