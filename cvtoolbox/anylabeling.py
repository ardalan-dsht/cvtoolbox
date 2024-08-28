from PIL import Image

from .data import colors
from .io import load_image_filenames, load_json_file, load_json_filenames
from .visualize import visualize_bounding_box


def single_anylabeling_to_coco_bbox(anylabeling_bbox):
    x = anylabeling_bbox[0]
    y = anylabeling_bbox[1]
    width = anylabeling_bbox[2] - anylabeling_bbox[0]
    height = anylabeling_bbox[3] - anylabeling_bbox[1]
    coco_bbox = [x, y, width, height]
    return coco_bbox


class AnylabelingDataset:
    def __init__(self, root_dir) -> None:
        self.root_dir = root_dir
        self.json_filenames = load_json_filenames(root_dir)
        self.image_filenames = load_image_filenames(root_dir)

    def visualize_bbox(self, image_index):
        image_file_path = self.image_filenames[image_index]
        image = Image.open(image_file_path)
        json_file_path = str(self.root_dir / image_file_path.stem) + ".json"
        annotations = load_json_file(json_file_path)
        shapes = annotations["shapes"]
        new_annotaitons = []
        for shape in shapes:
            if shape["shape_type"] == "rectangle":
                label = shape["label"]
                points = shape["points"]
                bbox = [*points[0], *points[1]]
                coco_bbox = single_anylabeling_to_coco_bbox(bbox)
                new_annotaitons.append((label, coco_bbox))
        image_with_bounding_boxes = visualize_bounding_box(
            image, new_annotaitons, colors
        )
        return image_with_bounding_boxes
