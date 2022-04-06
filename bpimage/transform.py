"""Function for appling transformations to the image such as rotation and scaling.
"""
from typing import Union
import numpy as np


def flipv(img: np.ndarray) -> np.ndarray:
    """Flips the image across the vertical, from left to right.

    Args:
        img: The image to flip.

    Returns:
        A flipped view of the image
    """
    return img[:, ::-1]


def fliph(img: np.ndarray) -> np.ndarray:
    """Flips the image across the horizontal, from bottom to top.

    Args:
        img: The image to flip.

    Returns:
        A flipped view of the image
    """
    return img[::-1, :]


def rotate90(img: np.ndarray, times: int = 1) -> np.ndarray:
    """Rotates the image counter-clockwise 90 degrees around the center.

    Args:
        img: The image to rotate. Negative values are ignored. 

    Returns:
        A rotated view of the image
    """
    times = max(0, times) % 4
    # No need to do anything if the number of rotations brings us back to the original image.
    if times == 0:
        return img[:]
    # Handle 180 degree rotations
    if times == 2:
        return flipv(fliph(img))
    # Handle 270 degree rotations
    if times == 3:
        return flipv(np.transpose(img, axes=(1, 0, 2)))
    # Handle just 90
    return np.transpose(flipv(img), axes=(1, 0, 2))


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


def rescale(img: np.ndarray, scale: Union[float,np.ndarray] = 2) -> np.ndarray:
    scale = np.atleast_1d(scale)

    if scale.size > 1 and scale.size != img.ndim - 1:
        raise ValueError('scale must specify one value per axis')

    print('rescale')
    return img
