import os
import sys
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import warnings

# textsize() is deprecated since PIL 10.0.0
warnings.filterwarnings("ignore", category=DeprecationWarning)


def extract_and_save_characters(font_path, output_path):
    font = ImageFont.truetype(font_path, size=100)
    ttfont = TTFont(font_path)

    for table in ttfont['cmap'].tables:
        for char_code, _ in table.cmap.items():
            image = Image.new("RGB", (128, 128), color="white")
            draw = ImageDraw.Draw(image)
            text = chr(char_code)
            width, height = draw.textsize(text, font=font)
            draw.text(((128 - width) / 2, (128 - height) / 2), text, font=font, fill="black")

            output_file = os.path.join(output_path, f"{char_code:04x}.png")
            image.save(output_file)

    ttfont.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <font_path> [output_path]")
        sys.exit(1)

    font_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "data/fonts/"
    output_path = os.path.join(output_path, os.path.basename(font_path).split(".")[0])

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else: 
        print("Output path already exists. Ignoring.")
        exit(0)

    try:
        extract_and_save_characters(font_path, output_path)
    except KeyboardInterrupt:
        print("Interrupted. Terminating...")
        os.remove(output_path)
        print("Unfinished output data removed.")
        
    print("Characters extracted and saved.")