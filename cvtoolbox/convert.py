import base64
from io import BytesIO


def convert_string_bbox_to_float(bbox):
    a = float(bbox[0])
    b = float(bbox[1])
    c = float(bbox[2])
    d = float(bbox[3])
    new_bbox = [a, b, c, d]
    return new_bbox


def convert_list_of_pil_to_base64(list_of_images):
    list_of_base64 = []
    for image in list_of_images:
        im_file = BytesIO()
        image.save(im_file, format="png")
        im_bytes = im_file.getvalue()
        im_b64 = base64.b64encode(im_bytes)
        im_b64_str = im_b64.decode("utf-8")
        list_of_base64.append(im_b64_str)
    return list_of_base64
