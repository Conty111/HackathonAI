import os
from tensorflow import keras
from BaseModel import BaseModel

import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline


class BannerModel(BaseModel):
    def __init__(self) -> None:
        device = "cuda"
        model_id_or_path = "runwayml/stable-diffusion-v1-5"
        self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
        self.pipe = self.pipe.to(device)

    def process(self, promt: str, path_to_save: str, path_to_img: str, unique_id: int) -> str:
        """
            Возвращает путь до сгенерированного файла
        """
        init_image = Image.open(path_to_img).convert("RGB")
        init_image = init_image.resize((1920, 1080))

        images = self.pipe(prompt=promt, image=init_image, strength=0.75, guidance_scale=7.5, negative_prompt=BannerModel.NEGATIV_PROMT).images
        path = os.path.join(path_to_save, f"preview_{unique_id:05d}.jpg")
        images[0].save(path)
        return path