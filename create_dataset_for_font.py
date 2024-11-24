from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os
from tqdm import tqdm
from koshur.font_analyzer import check_text_glyphs
import textwrap
import argparse


def draw_text(text, font_file):
    # TODO: Add more stuff like min width etc
    LINE_SPACING = 30
    PAGE_LINES = 20
    new_text = []
    st_idx = 0
    for idx, char in enumerate(text):
        if char == "\n":
            line = text[st_idx:idx]
            wrapped_line = "\n".join(textwrap.wrap(line, 120))
            new_text.append(wrapped_line + "\n")
            st_idx = idx + 1
    images_text = []
    for page_idx in range(0, len(new_text), PAGE_LINES):
        page_text = "".join(new_text[page_idx : page_idx + PAGE_LINES])
        if not page_text.strip():
            continue
        font = ImageFont.truetype(font_file, size=30)

        # Create a temporary image and drawing context
        tmp_img = Image.new("RGB", (1, 1), (255, 255, 255))
        draw = ImageDraw.Draw(tmp_img)

        # Get the bounding box of multiline text
        bbox = draw.multiline_textbbox(
            (0, 0),
            page_text,
            font=font,
            align="right",
            spacing=LINE_SPACING,
        )

        # Calculate size from bounding box and convert to integers
        width = int(bbox[2] - bbox[0])
        height = int(bbox[3] - bbox[1])

        # Create the actual image with the correct size
        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Draw the text aligned to the right
        draw.multiline_text(
            (width, 0),
            page_text,
            font=font,
            fill="black",
            align="right",
            anchor="ra",
            spacing=LINE_SPACING,
        )

        images_text.append((img, page_text))

    return images_text


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("font_path")
    args = parser.parse_args()

    font_path = args.font_path

    files = list(Path("./kashmiri_wiki_articles/").glob("*"))

    texts = " ".join(path.read_text() for path in files)

    chars = set(texts)
    _, missing_chars = check_text_glyphs("".join(chars), font_path)
    missing_chars.remove("\n")
    print(f"{missing_chars = }")

    dataset_base_path = f"dataset/{os.path.basename(font_path).split('.')[0]}/"
    os.makedirs(dataset_base_path)
    os.makedirs(os.path.join(dataset_base_path, "images"))
    os.makedirs(
        os.path.join(
            dataset_base_path,
            "text",
        )
    )
    for file in tqdm(files):
        text = file.read_text()
        for char in missing_chars:
            text = text.replace(char, "")

        images_text = draw_text(text, font_path)
        for page_no, (img, page_text) in enumerate(images_text):
            file_name = f"{os.path.basename(file).split(".")[0]}_{page_no}"
            img.save(os.path.join(dataset_base_path, "images", file_name + ".png"))
            with open(
                os.path.join(dataset_base_path, "text", file_name + ".txt"), "w"
            ) as f:
                f.write(page_text)
# font_path = "./kashmiri_fonts/NotoNastaliqUrdu-Regular.ttf"
# font_path = "./Packagae(KbFonts)/Gulmarg Nataleeq_2013.ttf"
# font_path = "./Packagae(KbFonts)/Narqalam.ttf"
# font_path = "./kashmiri_fonts/AAAGoldenLotus Stg1_Ver1 Regular.ttf"
