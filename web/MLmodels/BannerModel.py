import keras_cv
import os
from tensorflow import keras
from BaseModel import BaseModel

import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline


class BannerModel(BaseModel):
    def __init__(self) -> None:
        keras.mixed_precision.set_global_policy("float32")
        self.model = keras_cv.models.StableDiffusion(
            jit_compile=True, img_width=2204, img_height=804
        )

        device = "cuda"
        model_id_or_path = "runwayml/stable-diffusion-v1-5"
        self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
        self.pipe = self.pipe.to(device)

    def process(self, promt: str, path_to_save: str, path_to_img: str, unique_id: int) -> [str]:
        """
            Возвращает путь до сгенерированного файла
        """
        if not path_to_img:
            images = self.model.text_to_image(
                f"{promt}"
                "high quality, elegant, closeup",
                batch_size=3, negative_prompt=BannerModel.NEGATIV_PROMT
            )
            res = []
            for img in images:
                path = os.path.join(path_to_save, f"banner_{unique_id:05d}.jpg")
                keras.utils.save_img(path, img)
                res.append(path)
            return res
        else:
            init_image = Image.open(path_to_img).convert("RGB")
            init_image = init_image.resize((1920, 1080))

            images = self.pipe(prompt=promt, image=init_image, strength=0.75, guidance_scale=7.5, negative_prompt=BannerModel.NEGATIV_PROMT).images
            images[0].save("testPreviewRes.png")
