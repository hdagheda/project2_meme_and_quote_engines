# MemeEngine/meme_engine.py
import os
import random
import textwrap
import uuid
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

class MemeEngine:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def make_meme(
        self,
        img_path: str,
        text: Optional[str],
        author: Optional[str],
        width: int = 500,
    ) -> str:
        """Create a meme image with quote text and return the saved file path.

        Uses Pillow to resize the image and draw text onto it.
        """
        if not img_path or not os.path.exists(img_path):
            raise FileNotFoundError(f"Image not found: {img_path}")

        quote_text = ""
        if text:
            quote_text = f"{text}"
        if author:
            quote_text = f"{quote_text} - {author}" if quote_text else f"- {author}"

        with Image.open(img_path) as im:
            # Resize maintaining aspect ratio
            w_percent = width / float(im.width)
            h_size = int(float(im.height) * w_percent)
            im = im.resize((width, h_size))

            if quote_text:
                draw = ImageDraw.Draw(im)

                # Load font (fallback to default if not found)
                font = self._load_font(size=max(16, width // 22))

                # Wrap text to fit image width
                max_chars = max(20, width // 12)
                wrapped = textwrap.fill(quote_text, width=max_chars)

                # Position text randomly with margins
                text_w, text_h = self._multiline_text_size(draw, wrapped, font)
                margin = 10
                x = margin
                y = random.randint(margin, max(margin, im.height - text_h - margin))

                # Draw text using Pillow with a stroke for readability
                self._draw_text_with_outline(draw, (x, y), wrapped, font)

            out_path = os.path.join(self.output_dir, f"meme_{uuid.uuid4().hex}.jpg")
            im.save(out_path, format="JPEG", quality=85)

        return out_path

    @staticmethod
    def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        candidates = [
            "arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
        for path in candidates:
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                continue
        return ImageFont.load_default()

    @staticmethod
    def _multiline_text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
        try:
            bbox = draw.multiline_textbbox((0, 0), text, font=font)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        except Exception:
            # Fallback approximation
            lines = text.splitlines() if text else [""]
            widths = [draw.textlength(line, font=font) for line in lines]
            line_height = font.getbbox("Ay")[3] if hasattr(font, "getbbox") else font.size
            return int(max(widths) if widths else 0), int(line_height * len(lines) * 1.2)

    @staticmethod
    def _draw_text_with_outline(
        draw: ImageDraw.ImageDraw,
        position: tuple[int, int],
        text: str,
        font,
        fill: str = "white",
        outline: str = "black",
        stroke_width: int = 2,
    ) -> None:
        # Prefer Pillow's stroke rendering
        try:
            draw.multiline_text(
                position,
                text,
                font=font,
                fill=fill,
                align="left",
                stroke_width=stroke_width,
                stroke_fill=outline,
            )
        except TypeError:
            # Fallback: manual outline
            x, y = position
            for dx in (-stroke_width, 0, stroke_width):
                for dy in (-stroke_width, 0, stroke_width):
                    if dx == 0 and dy == 0:
                        continue
                    draw.multiline_text((x + dx, y + dy), text, font=font, fill=outline)
            draw.multiline_text((x, y), text, font=font, fill=fill)