from pycocotools.coco import COCO
from ultralytics.data.converter import convert_coco

from .data import colors
from .io import *
from .visualize import visualize_bounding_box


def convert_coco_to_yolo_for_object_detection(coco_path, yolo_path):
    convert_coco(
        coco_path,
        yolo_path,
        use_keypoints=False,
        use_segments=False,
        cls91to80=False,
    )


class CocoDataset:
    def __init__(self, image_files_root_path, annotations_file_path):
        self.image_files_root_path = image_files_root_path
        self.coco = COCO(annotations_file_path)
        self.category_id_to_name = {}
        annotations = load_json_file(annotations_file_path)
        for category in annotations["categories"]:
            self.category_id_to_name[category["id"]] = category["name"]

    def visualize_bbox(self, image_id):
        coco_image = self.coco.loadImgs(image_id)[0]
        image_file_path = self.image_files_root_path / coco_image["file_name"]
        image = Image.open(image_file_path)
        annotations = []
        pycocotools_annotation_ids = self.coco.getAnnIds(imgIds=image_id)
        pycocotools_annotations = self.coco.loadAnns(pycocotools_annotation_ids)
        for ann in pycocotools_annotations:
            bbox = ann["bbox"]
            category = self.coco.loadCats(ann["category_id"])[0]["name"]
            annotations.append((category, bbox))
        image_with_bounding_boxes = visualize_bounding_box(image, annotations, colors)
        return image_with_bounding_boxes
