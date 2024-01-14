import base64
from io import BytesIO
from typing import Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ..config import SIYUAN


class DrawText:

    def __init__(self, image: ImageDraw.ImageDraw, font: str) -> None:
        self._img = image
        self._font = str(font)

    def get_box(self, text: str, size: int):
        return ImageFont.truetype(self._font, size).getbbox(text)

    def draw(self,
            pos_x: int,
            pos_y: int,
            size: int,
            text: str,
            color: Tuple[int, int, int, int] = (255, 255, 255, 255),
            anchor: str = 'lt',
            stroke_width: int = 0,
            stroke_fill: Tuple[int, int, int, int] = (0, 0, 0, 0),
            multiline: bool = False):

        font = ImageFont.truetype(self._font, size)
        if multiline:
            self._img.multiline_text((pos_x, pos_y), str(text), color, font, anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)
        else:
            self._img.text((pos_x, pos_y), str(text), color, font, anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)
    
    def draw_partial_opacity(self,
            pos_x: int,
            pos_y: int,
            size: int,
            text: str,
            po: int = 2,
            color: Tuple[int, int, int, int] = (255, 255, 255, 255),
            anchor: str = 'lt',
            stroke_width: int = 0,
            stroke_fill: Tuple[int, int, int, int] = (0, 0, 0, 0)):

        font = ImageFont.truetype(self._font, size)
        self._img.text((pos_x + po, pos_y + po), str(text), (0, 0, 0, 128), font, anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)
        self._img.text((pos_x, pos_y), str(text), color, font, anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)


def draw_gradient(width: int, 
        height: int, 
        rgb_start: Tuple[int, int, int] = (203, 162, 253), 
        rgb_stop: Tuple[int, int, int] = (251, 244, 127), 
        horizontal: Tuple[bool, bool, bool] = (False, False, False)
    ) -> Image.Image:
    result = np.zeros((height, width, 3), dtype=np.uint8)
    for i, (start, stop, is_ho) in enumerate(zip(rgb_start, rgb_stop, horizontal)):
        if is_ho:
            result[:, :, i] = np.tile(np.linspace(start, stop, width), (height, 1))
        else:
            result[:, :, i] = np.tile(np.linspace(start, stop, height), (width, 1)).T

    return Image.fromarray(result).convert('RGBA')


def text_to_image(text: str) -> Image.Image:
    font = ImageFont.truetype(str(SIYUAN), 24)
    padding = 10
    margin = 4
    lines = text.strip().split('\n')
    max_width = 0
    for line in lines:
        l, t, r, b = font.getbbox(line)
        max_width = max(max_width, r)
    wa = max_width + padding * 2
    ha = b * len(lines) + margin * (len(lines) - 1) + padding * 2
    im = Image.new('RGB', (wa, ha), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)
    for index, line in enumerate(lines):
        draw.text((padding, padding + index * (margin + b)), line, font=font, fill=(0, 0, 0))
    return im


def to_bytes_io(text: str) -> BytesIO:
    bio = BytesIO()
    text_to_image(text).save(bio, format='PNG')
    bio.seek(0)

    return bio


def image_to_base64(img: Image.Image, format='PNG') -> str:
    output_buffer = BytesIO()
    img.save(output_buffer, format)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode()
    return 'base64://' + base64_str


def image_to_bytesio(img: Image.Image, format_='PNG') -> BytesIO:
    bio = BytesIO()
    img.save(bio, format_)
    bio.seek(0)
    return bio
