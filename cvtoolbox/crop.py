from PIL import Image
import numpy as np
from skimage.draw import polygon


def crop_mask_from_result(
        image: Image,
        detected_object: dict,
    ):
        # Convert the image to a NumPy array
        image_np = np.array(image)
        # Extract coordinates from detected_object
        x = detected_object["segments"]["x"]
        y = detected_object["segments"]["y"]
        x_min = round(detected_object["box"]["x1"])
        y_min = round(detected_object["box"]["y1"])
        x_max = round(detected_object["box"]["x2"])
        y_max = round(detected_object["box"]["y2"])
        # Crop the image based on bounding box
        cropped_image_np = image_np[y_min:y_max, x_min:x_max]
        # Adjust segment coordinates for cropping
        x_cropped = np.clip([xi - x_min for xi in x], 0, cropped_image_np.shape[1] - 1)
        y_cropped = np.clip([yi - y_min for yi in y], 0, cropped_image_np.shape[0] - 1)
        # Create a mask for the polygon area
        mask = np.zeros((cropped_image_np.shape[0], cropped_image_np.shape[1]), dtype=bool)
        rr, cc = polygon(y_cropped, x_cropped)
        # Clip the polygon coordinates to stay within bounds
        rr = np.clip(rr, 0, mask.shape[0] - 1)
        cc = np.clip(cc, 0, mask.shape[1] - 1)
        # Fill the mask with True values where the polygon is defined
        mask[rr, cc] = True
        # Create an output image with an alpha channel
        output_image_cropped = np.zeros((cropped_image_np.shape[0], cropped_image_np.shape[1], 4), dtype=np.uint8)
        # Set RGB values where the mask is True and set alpha to 255 (opaque)
        output_image_cropped[mask] = np.concatenate((cropped_image_np[mask], np.full((np.sum(mask), 1), 255)), axis=1)
        
        # Set background (where mask is False) to transparent (alpha 0)
        output_image_cropped[~mask] = [0, 0, 0, 0]
        
        # Convert back to PIL Image with alpha channel
        cropped_mask_image = Image.fromarray(output_image_cropped)
        
        return cropped_mask_image