"""Function for appling transformations to the image such as rotation and scaling.
"""
import ctypes
import math
import numpy as np

# load the affine function written in c and configure so we can invoke it.
bp_clib = ctypes.cdll.LoadLibrary('./bpimage.so')
bp_clib.affine_transform.restype = None
bp_clib.affine_transform.argtypes = [np.ctypeslib.ndpointer(np.uint8, ndim=3),
                                     ctypes.POINTER(np.ctypeslib.c_intp),
                                     ctypes.POINTER(np.ctypeslib.c_intp),
                                     np.ctypeslib.ndpointer(
                                         np.float32, ndim=2),
                                     np.ctypeslib.ndpointer(np.uint8, ndim=3),
                                     ctypes.POINTER(np.ctypeslib.c_intp),
                                     ctypes.POINTER(np.ctypeslib.c_intp)]


def flipv(img: np.ndarray) -> np.ndarray:
    """Flips the image across the vertical, from left to right.

    Args:
        img: The image to flip.

    Returns:
        A new ndarray containing the result of the flip
    """
    dest = np.zeros(img.shape, dtype=np.uint8)

    trans = np.array([[-1,0,img.shape[1] - 1],
                      [0,1,0],
                      [0,0,1]], dtype=np.float32)

    bp_clib.affine_transform(img, img.ctypes.shape, img.ctypes.strides, trans,
                             dest, dest.ctypes.shape, dest.ctypes.strides)
    return dest


def fliph(img: np.ndarray) -> np.ndarray:
    """Flips the image across the horizontal, from bottom to top.

    Args:
        img: The image to flip.

    Returns:
        A new ndarray containing the result of the flip
    """
    dest = np.zeros(img.shape, dtype=np.uint8)

    trans = np.array([[1,0,0],
                      [0,-1,img.shape[0] - 1],
                      [0,0,1]], dtype=np.float32)

    bp_clib.affine_transform(img, img.ctypes.shape, img.ctypes.strides, trans,
                             dest, dest.ctypes.shape, dest.ctypes.strides)
    return dest


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


def rotate(img: np.ndarray, angle: float = 180) -> np.ndarray:
    """Rotates the image counter-clockwise by a specified angle around the center

    Args:
        img: The image to rotate.
        angle: The amount to rotate in degrees. 

    Returns:
        A new ndarray containing the result of the rotate
    """
    dest = np.zeros(img.shape, dtype=np.uint8)

    # get center coordinates of image so we can roate around it
    cx = img.shape[1] // 2
    cy = img.shape[0] // 2

    # convert angle to rads and precalculate values
    angle = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)

    # calculate an affine transformation that rotates from the center
    trans = np.array([[cos, sin,  cx * sin - cy * cos + cx],
                      [-sin,  cos, -cx * cos - cy * sin + cy],
                      [0, 0, 1]], dtype=np.float32)

    bp_clib.affine_transform(img, img.ctypes.shape, img.ctypes.strides, trans,
                             dest, dest.ctypes.shape, dest.ctypes.strides)
    return dest


def rescale(img: np.ndarray, scale: float = 1.25) -> np.ndarray:
    if(scale <= 0):
        raise ValueError('Scale must be greater than zero')

    height = round(img.shape[0] * scale)
    width = round(img.shape[1] * scale)
    dest = np.zeros((height, width, 3), dtype=np.uint8)

    tform = _inverse_transform(scale_x=scale, scale_y=scale)
    bp_clib.affine_transform(img, img.ctypes.shape, img.ctypes.strides, tform,
                             dest, dest.ctypes.shape, dest.ctypes.strides)
    return dest


def _inverse_transform(scale_x: float = 1, skew_x: float = 0, offset_x: float = 0, scale_y: float = 1, skew_y: float = 0, offset_y: float = 0) -> np.ndarray:
    """Generates an inverse transformation matrix with the given parameters."""
    return np.linalg.inv(np.array([[scale_x, skew_x, offset_x],
                                   [skew_y, scale_y, offset_y],
                                   [0, 0, 1]], dtype=np.float32))
