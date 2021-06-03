import os

from PIL import Image as PILImage
from PIL import UnidentifiedImageError


class Image:
    def __init__(self, image: str):
        try:
            self.image = PILImage.open(image)
        except UnidentifiedImageError as e:
            raise e

    def rotate(self, angle: str):
        try:
            angle = float(angle)
        except ValueError:
            raise ValueError(f"Invalid value '{angle}' for rotate")
        self.image = self.image.rotate(angle)

    def gray_scale(self):
        self.image = self.image.convert("1")

    def overlay(self, overlay_image: str):
        self._type_check(overlay_image, [".png"])

        img = PILImage.open(overlay_image).convert("RGBA")
        alpha_range = img.getextrema()[-1]
        if alpha_range == (255, 255):
            raise TypeError(f"Image '{img.filename}' is not transparent")

        self.image.paste(img, (0, 0))

    def save(self, output_image: str):
        self._type_check(output_image, [".jpg", ".png"])
        self.image.save(output_image)

    def _type_check(self, image: str, valid_types: list = []):
        filename, extension = os.path.splitext(image)
        if extension not in valid_types:
            types = " or ".join(valid_types)
            raise TypeError(f"File '{filename}' is not {types} formatted")
