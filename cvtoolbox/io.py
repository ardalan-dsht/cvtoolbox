import json
from pathlib import Path

import yaml
from PIL import Image

from .data import valid_file_formats


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


def load_text_filenames(texts_root_path: Path) -> list:
    all_filenames_in_directory = [name for name in texts_root_path.iterdir()]
    text_filenames_in_directory = []
    for name in all_filenames_in_directory:
        if name.suffix == ".txt":
            text_filenames_in_directory.append(name)
    return text_filenames_in_directory


def load_text_file(file_path):
    with open(file_path, "r") as text_file:
        data = [line.rstrip("\n") for line in text_file.readlines()]
    return data


def load_json_filenames(jsons_root_path: Path) -> list:
    all_filenames_in_directory = [name for name in jsons_root_path.iterdir()]
    json_filenames_in_directory = []
    for name in all_filenames_in_directory:
        if name.suffix == ".json":
            json_filenames_in_directory.append(name)
    return json_filenames_in_directory


def load_json_file(file_path):
    with open(file_path, "r") as file:
        json_file = json.load(file)
    return json_file


def load_yaml_file_into_json(file_path):
    with open(file_path, "r") as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data
