"""Function for appling transformations to the image such as rotation and scaling.
"""
import numpy as np


def flipv(img: np.ndarray) -> np.ndarray:
    """Flips the image across the vertical, from left to right.

    Args:
        img: The image to flip.

    Returns:
        A new ndarray containing the result of the flip
    """
    print('flipv')
    return img


def fliph(img: np.ndarray) -> np.ndarray:
    """Flips the image across the horizontal, from bottom to top.

    Args:
        img: The image to flip.

    Returns:
        A new ndarray containing the result of the flip
    """
    print('fliph')
    return img


def rotate90(img: np.ndarray, times: int = 1) -> np.ndarray:
    """Rotates the image counter-clockwise 90 degrees around the center.

    Args:
        img: The image to rotate.

    Returns:
        A new ndarray containing the result of the rotate
    """
    print('rotate90')
    return img


def rotate(img: np.ndarray, angle: float = 1) -> np.ndarray:
    """Rotates the image counter-clockwise by a specified angle around the center

    Args:
        img: The image to rotate.
        angle: The amount to rotate in degrees. 

    Returns:
        A new ndarray containing the result of the rotate
    """
    print('rotate')
    return img


def rescale(img: np.ndarray) -> np.ndarray:
    print('rescale')
    return img
