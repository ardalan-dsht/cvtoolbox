from pathlib import Path

from PIL import Image

from .convert import convert_string_bbox_to_float
from .data import colors
from .io import (
    load_image_filenames,
    load_text_file,
    load_text_filenames,
    load_yaml_file_into_json,
)
from .visualize import visualize_bounding_box


def load_yolo_annt_file(annotation_file_path):
    data = load_text_file(annotation_file_path)
    annotations = []
    for sample in data:
        data = sample.split(" ")
        label = data[0]
        annotation_for_sample = data[1::]
        annotation_for_sample = convert_string_bbox_to_float(annotation_for_sample)
        annotations.append((label, annotation_for_sample))
    return annotations


def single_yolo_to_coco_bbox(
    yolo_bbox,
    image_width_in_px,
    image_height_in_px,
):
    x_center_relative = yolo_bbox[0]
    y_center_relative = yolo_bbox[1]
    width_relative = yolo_bbox[2]
    height_relative = yolo_bbox[3]

    x_min_relative = x_center_relative - (width_relative / 2)
    y_min_relative = y_center_relative - (height_relative / 2)

    x_min_absolute = x_min_relative * image_width_in_px
    y_min_absolute = y_min_relative * image_height_in_px
    width_absolute = image_width_in_px * width_relative
    height_absolute = image_height_in_px * height_relative

    coco_bbox = [x_min_absolute, y_min_absolute, width_absolute, height_absolute]
    return coco_bbox


def batch_yolo_to_coco_bbox(
    yolo_samples,
    width,
    height,
):
    coco_samples = []
    for category, yolo_bbox in yolo_samples:
        coco_bbox = single_yolo_to_coco_bbox(yolo_bbox, width, height)
        coco_samples.append((category, coco_bbox))
    return coco_samples


class YoloDataset:
    def __init__(self, config_file_path: Path) -> None:
        config_file = load_yaml_file_into_json(config_file_path)
        root_dir = Path(config_file["path"])
        self.categories = config_file["names"]
        # TRAIN
        train_path = (
            root_dir / config_file["train"] if "train" in config_file.keys() else None
        )
        self.train_images_paths = load_image_filenames(train_path)
        train_labels_paths = load_text_filenames(train_path)
        self.train_labels_name_to_path = {
            filename.stem: filename for filename in train_labels_paths
        }
        # VALIDATION
        valid_path = (
            root_dir / config_file["val"] if "val" in config_file.keys() else None
        )
        if valid_path is not None:
            self.valid_images_paths = load_image_filenames(valid_path)
            valid_labels_paths = load_text_filenames(valid_path)
            self.valid_labels_name_to_path = {
                filename.stem: filename for filename in valid_labels_paths
            }
        # TEST
        test_path = (
            root_dir / config_file["test"] if "test" in config_file.keys() else None
        )
        if test_path is not None:
            self.test_images_paths = load_image_filenames(test_path)
            test_labels_paths = load_text_filenames(test_path)
            self.test_labels_name_to_path = {
                filename.stem: filename for filename in test_labels_paths
            }

    def change_label_id_to_name_in_annotations(self, all_annotations_for_image):
        translated_annotations_for_image = []
        for label_id, annotation in all_annotations_for_image:
            label = self.categories[int(label_id)]
            translated_annotations_for_image.append((label, annotation))
        return translated_annotations_for_image

    def visualize_bbox(self, image_file_index, dataset_set="train"):
        if dataset_set == "train":
            selected_image_set = self.train_images_paths
            labels_filename_to_path = self.train_labels_name_to_path
        elif dataset_set == "val":
            selected_image_set = self.valid_images_paths
            labels_filename_to_path = self.valid_labels_name_to_path
        else:
            selected_image_set = self.test_images_paths
            labels_filename_to_path = self.test_labels_name_to_path
        selected_image = selected_image_set[image_file_index]
        selected_image_filename = selected_image.stem
        annotations_file_path_for_image = labels_filename_to_path[
            selected_image_filename
        ]
        all_annotations_for_image = load_yolo_annt_file(annotations_file_path_for_image)
        all_annotations_for_image_with_label = (
            self.change_label_id_to_name_in_annotations(all_annotations_for_image)
        )
        image = Image.open(selected_image)
        width, height = image.size
        annotations = batch_yolo_to_coco_bbox(
            all_annotations_for_image_with_label, width, height
        )
        image_with_bounding_boxes = visualize_bounding_box(image, annotations, colors)
        return image_with_bounding_boxes

    def visualize_polygon(self):
        pass
