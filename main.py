from fastapi import Depends, FastAPI
from fastapi.security.api_key import APIKey

import uvicorn
import generator as gen
import pathlib

app = FastAPI()


@app.get("/get_generated_image/{image_name}")
async def info(image_name: str, additional_prompt: None | str = gen.additional_prompt):
    """
    Generates image, saves it to S3 bucket, deletes it on EC2 GPU instance
    and Returns url of image on S3.
    """
    generated_image = gen.generate_image(image_name=image_name, additional_prompt=additional_prompt)
    gen.save_file_to_bucket(file_name=generated_image)
    gen.delete_file(pathlib.Path(f"/{gen.full_outputs_path}/{generated_image}/"))
    s3_url = gen.get_file_url(f"{generated_image}.png")

    return s3_url


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
