import random

from PIL import ImageDraw, ImageFont


def visualize_bounding_box(
    image,
    all_annotations_for_image_with_label,
    colors,
):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    stroke_size = round(0.005 * width)
    font_size = round(0.02 * width)
    font = ImageFont.load_default(size=font_size)  # Load the default font
    for category, bbox in all_annotations_for_image_with_label:
        color = random.sample(colors, k=1)[0]
        # Draw the rectangle
        draw.rectangle(
            [(bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3])],
            outline=color,
            width=stroke_size,
        )
        # Draw the text
        draw.text(
            (bbox[0], bbox[1]),
            category,
            fill="white",
            font=font,
            stroke_fill=color,
            stroke_width=stroke_size,
        )
    return image
