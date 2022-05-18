
"""Functions for modifying the colors of images.
"""
import numpy as np


def rgb2grayscale(img: np.ndarray) -> np.ndarray:
    """Converts an RGB image to a grayscale image.
    Each RGB pixel becomes a single 8bit value representing the weighted sum of the colors. 
    Note this will modify the shape of the image from (h,w,3) to (h,w)

    Args:
        img: The image to convert

    Returns:
        A new ndarray with shape (h,w) containing the converted image
    """
    if img.ndim != 3 and img.shape[-1] != 3:
        return ValueError("Image must be RGB.")

    return (img @ np.array([.2126, .7152, .0722])).astype(np.uint8)


def grayscale2rgb(img: np.ndarray) -> np.ndarray:
    """Converts an image in grayscale format to RGB format.
    Each single 8bit pixel of the image is expanded int RGB channels. 
    The shape of the image will be modified from (h,w) to (h,w,3).

    Args:
        img: The image to convert

    Returns:
        A new ndarray with shape (h,w,3) containing the converted image
    """
    if img.ndim != 2:
        return ValueError("Image must be grayscale.")

    return img[:, :, np.newaxis].repeat(3, axis=-1)


def sepia(img: np.ndarray) -> np.ndarray:
    return img
