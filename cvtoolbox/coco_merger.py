import json
import os
import shutil
from pathlib import Path
from typing import Sequence

from .io import load_filenames_with_format
        


def merge_coco_datasets(
    coco_root_dir: Path,
    paths_to_merge: Sequence[Path],
) -> None:
    all_json_annotations = []
    for dataset in paths_to_merge:
        annotations = load_filenames_with_format(dataset, file_format=".json")[0]
        all_json_annotations.append(annotations)
    new_coco_categories = all_json_annotations[0]["categories"]
    new_coco_images = []
    new_coco_annotations = []
    last_image_idx = 0
    last_annotation_idx = 0
    for idx, annotation_file in enumerate(all_json_annotations):
        for image in annotation_file["images"]:
            # First handle images
            image_file_format = image["file_name"].split(".")[-1]
            new_image_filename = f"{last_image_idx}.{image_file_format}"
            shutil.copy(
                paths_to_merge[idx] / image["file_name"],
                coco_root_dir / new_image_filename,
            )
            old_image_id = image["id"]
            image["file_name"] = new_image_filename
            image["id"] = last_image_idx
            last_image_idx += 1
            new_coco_images.append(image)
            # Next handle annotations
            for annotation in annotation_file["annotations"]:
                if old_image_id == annotation["image_id"]:
                    annotation["image_id"] = image["id"]
                    annotation["id"] = last_annotation_idx
                    new_coco_annotations.append(annotation)
                    last_annotation_idx += 1
    new_coco = {}
    new_coco["annotations"] = new_coco_annotations
    new_coco["images"] = new_coco_images
    new_coco["info"] = all_json_annotations[0]["info"]
    new_coco["license"] = all_json_annotations[0]["license"]
    new_coco["categories"] = new_coco_categories
    with open(coco_root_dir / Path("annotations.json"), "w+") as json_file:
        json.dump(new_coco, json_file)