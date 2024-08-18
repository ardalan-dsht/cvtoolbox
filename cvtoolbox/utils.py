from pathlib import Path

from PIL import Image

valid_file_formats = ["jpeg", "JPEG", "jpg", "JPG", "png", "PNG"]


def load_image_filenames(images_root_path: Path) -> list:
    all_filenames_in_directory = [name for name in images_root_path.iterdir()]
    image_filenames_in_directory = []
    for name in all_filenames_in_directory:
        if name.name.split(".")[-1] in valid_file_formats:
            image_filenames_in_directory.append(name)
    return image_filenames_in_directory


def load_image_files(image_filenames):
    loaded_images = [Image.open(image_path) for image_path in image_filenames]
    return loaded_images
