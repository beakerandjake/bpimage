"""Functions for modifying the colors of images.
"""
import numpy as np


def ensure_8bit_rgb(img: np.ndarray):
    """Raises an exception if the img is not an RGB image. 

    Args
        img: The image to validate. 

    Raises
        ValueError: The image was not an RGB image with and shape=(h,w,3).
    """
    if img.ndim != 3 and img.shape[-1] != 3:
        raise ValueError("img must be RGB with shape (h,w,3).")
