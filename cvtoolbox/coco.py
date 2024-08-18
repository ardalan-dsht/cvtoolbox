import gradio as gr
from pycocotools import COCO

from .utils import *


class CocoDataset:
    def __init__(self, image_files_root_path, annotations_file_path):
        self.image_files_root_path = image_files_root_path
        self.coco = COCO(annotations_file_path)
        self.category_id_to_name = {}
        annotations = load_json_file(annotations_file_path)
        for category in annotations["categories"]:
            self.category_id_to_name[category["id"]] = category["name"]

    def visualize(self):
        def show_image(image_id):
            image_file_info = self.coco.loadImgs(image_id)[0]
            image_file_path = self.image_files_root_path / image_file_info["filename"]
            image = Image.open(image_file_path)
            all_annotation_ids_for_image = self.coco.getAnnIds(image_id)
            all_annotations_for_image = self.coco.loadAnns(all_annotation_ids_for_image)
            annotations_for_image = []
            for annotation in all_annotations_for_image:
                bbox = annotation["bbox"]
                category_id = annotation["category_id"]
                category = self.category_id_to_name[category_id]
                annotation = (bbox, category)
                annotations_for_image.append(annotation)
            return image, annotations_for_image

        with gr.Blocks() as demo:
            with gr.Row():
                gradio_image = gr.AnnotatedImage(label="Annotations", show_legend=True)
            with gr.Row():
                selected_image_index = gr.Textbox()
            with gr.Row():
                button = gr.Button("Show")
            button.click(show_image, inputs=selected_image_index, outputs=gradio_image)
