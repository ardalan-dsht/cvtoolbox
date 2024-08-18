from dataclasses import dataclass

@dataclass
class CocoBoundingBox:
    """
    These are absolute pixel values for boudingbox.
    """
    x_min: int
    y_min: int
    height: int
    width: int