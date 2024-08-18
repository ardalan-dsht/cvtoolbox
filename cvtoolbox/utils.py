import json
from pathlib import Path

from PIL import Image

valid_file_formats = [".jpeg", ".JPEG", ".jpg", ".JPG", ".png", ".PNG"]


def load_image_filenames(images_root_path: Path) -> list:
    all_filenames_in_directory = [name for name in images_root_path.iterdir()]
    image_filenames_in_directory = []
    for name in all_filenames_in_directory:
        if name.suffix in valid_file_formats:
            image_filenames_in_directory.append(name)
    return image_filenames_in_directory


def load_image_files(image_filenames):
    loaded_images = [Image.open(image_path) for image_path in image_filenames]
    return loaded_images


def load_json_file(file_path):
    with open(file_path, "r") as file:
        json_file = json.load(file)
    return json_file
