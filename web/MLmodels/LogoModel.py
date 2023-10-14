import keras_cv
from tensorflow import keras
from BaseModel import BaseModel
import os


class LogoModel(BaseModel):
    def __init__(self) -> None:
        keras.mixed_precision.set_global_policy("float32")
        self.model = keras_cv.models.StableDiffusion(
            jit_compile=True, img_width=800, img_height=800
        )

    def process(self, promt: str, path_to_save: str, unique_id: int) -> [str]:
        images = self.model.text_to_image(
            f"{promt}"
            "high quality, elegant, closeup",
            batch_size=3, negative_prompt=LogoModel.NEGATIV_PROMT
        )
        res = []
        for img in images:
            path = os.path.join(path_to_save, f"logotip_{unique_id:05d}.jpg")
            keras.utils.save_img(path, img)
            res.append(path)
        return res