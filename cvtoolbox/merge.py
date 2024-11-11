from PIL import Image
import numpy as np


def add_png_image_to_background_image(png_image:Image, background:Image):
    # Calculate the height for the PNG image (3/4 of the background height)
    png_height = int(background.height * 3/4)

    # Resize the PNG image to fit within the specified height while maintaining aspect ratio
    png_image.thumbnail((background.width, png_height), Image.LANCZOS)

    # Create a new background image in RGB mode
    background_rgb = background.convert("RGB")

    # Convert images to NumPy arrays for manipulation
    bg_array = np.array(background_rgb)
    png_array = np.array(png_image)

    # Create an output array initialized with the background
    output_array = bg_array.copy()

    # Define the position where the PNG will be placed (at the bottom of the background)
    y_offset = bg_array.shape[0] - png_array.shape[0]

    # Calculate horizontal centering offset for the PNG image
    x_offset = (bg_array.shape[1] - png_array.shape[1]) // 2

    # Blend only in the area where the PNG image is placed
    for y in range(png_array.shape[0]):
        for x in range(png_array.shape[1]):
            # Get the alpha value from the PNG image
            alpha = png_array[y, x][3] / 255.0  # Normalize to [0, 1]
            # Blend pixel values based on alpha only for the area where PNG is placed
            output_array[y + y_offset, x + x_offset] = (
                (1 - alpha) * bg_array[y + y_offset, x + x_offset] + alpha * png_array[y, x][:3]
            )
    # Convert the output array back to a PIL image
    output_image = Image.fromarray(output_array, 'RGB')
    return output_image