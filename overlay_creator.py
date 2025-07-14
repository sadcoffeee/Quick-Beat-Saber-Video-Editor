import sys
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Fonts (need updating so they are not hard-coded paths)
TITLE_FONT_PATH = resource_path("fonts/Prompt-Black.ttf")
SUB_FONT_PATH = resource_path("fonts/Lato-Regular.ttf")
TEXT_COLOR = (255, 255, 255, 255)

def generate_overlay(map_id: str, output_path="overlay.png", width=2560, height=1440) -> str:
    # 1: Fetch BeatSaver data
    url = f"https://api.beatsaver.com/maps/id/{map_id}"
    response = requests.get(url)
    data = response.json()

    title = data["name"]
    subtitle = "Mapped by " + data["uploader"]["name"]
    cover_url = data["versions"][0]["coverURL"]

    # 2: Proportional layout config
    cover_size = (width // 8, width // 8)                  # 1/8th of width
    corner_offset = (width // 20, width // 20)             # 1/20th of width
    title_size = height // 24                              # 1/24th of height
    sub_size = height // 30                                # 1/30th of height
    spacing = height // 72                                 # 1/72nd of height

    # 3: Fetch and resize cover image
    cover_img = Image.open(BytesIO(requests.get(cover_url).content)).convert("RGBA")
    cover_img = cover_img.resize(cover_size)

    # 4: Create transparent overlay canvas
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay.paste(cover_img, corner_offset, cover_img)

    # 5: Draw title + subtitle
    draw = ImageDraw.Draw(overlay)
    title_font = ImageFont.truetype(TITLE_FONT_PATH, title_size)
    sub_font = ImageFont.truetype(SUB_FONT_PATH, sub_size)

    text_x = corner_offset[0] + cover_size[0] + 4 * spacing
    text_y = corner_offset[1] + cover_size[1] // 2 - title_size - sub_size // 2

    draw.text((text_x, text_y), title, font=title_font, fill=TEXT_COLOR)
    draw.text((text_x, text_y + title_size + spacing), subtitle, font=sub_font, fill=TEXT_COLOR)

    # 6: Save overlay
    overlay.save(output_path)
    print(f"Overlay saved as {output_path}")
    return output_path
