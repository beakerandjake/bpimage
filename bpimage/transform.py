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

    trans = np.array([[-1, 0, img.shape[1] - 1],
                      [0, 1, 0],
                      [0, 0, 1]], dtype=np.float32)

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

    trans = np.array([[1, 0, 0],
                      [0, -1, img.shape[0] - 1],
                      [0, 0, 1]], dtype=np.float32)

    bp_clib.affine_transform(img, img.ctypes.shape, img.ctypes.strides, trans,
                             dest, dest.ctypes.shape, dest.ctypes.strides)
    return dest


def rotate90(img: np.ndarray, times: int = 4) -> np.ndarray:
    """Rotates the image counter-clockwise 90 degrees around the center.

    Args:
        img: The image to rotate.  
        times: The number of times that the image should be rotated 90 degrees.

    Returns:
        A new ndarray of the source image rotated 90 degree n times.
    """
    times = max(0, times) % 4
    # No need to do anything if the number of rotations brings us back to the original image.
    if times == 0:
        # return copy because method specifies a new ndarray is returned.
        return img.copy()
    # Handle 180 degree rotations
    if times == 2:
        return flipv(fliph(img))
    # Handle 270 degree rotations
    if times == 3:
        return flipv(np.transpose(img, axes=(1, 0, 2)))
    # Handle just 90
    return np.transpose(flipv(img), axes=(1, 0, 2))


def rotate(img: np.ndarray, angle: float = 45) -> np.ndarray:
    """Rotates the image counter-clockwise by a specified angle around the center

    Args:
        img: The image to rotate.
        angle: The amount to rotate in degrees. 

    Returns:
        A new ndarray containing the result of the rotate
    """
    # convert angle to radians and precalculate values
    rads = math.radians(angle)
    cos = math.cos(rads)
    sin = math.sin(rads)

    # generate a rotation matrix for the specified radians
    rot = np.array([[cos, -sin, 0],
                    [sin, cos, 0],
                    [0, 0, 1]], dtype=np.float32)

    # matrix to translate the image so the center moves to the (0,0) origin point.
    center = np.array([[1, 0, img.shape[1] // 2],
                       [0, 1, img.shape[0] // 2],
                       [0, 0, 1]], dtype=np.float32)

    # calculate the size destination image based on the rotation
    height, width = _calc_new_img_size(img.shape, rot)
    dest = np.zeros((height, width, 3), dtype=np.uint8)

    # matrix to move the center of the image from the origin to the center of the destination image.
    back = np.array([[1, 0, -width//2],
                     [0, 1, -height//2],
                     [0, 0, 1]], dtype=np.float32)

    # generate the final transformation matrix which moves the center of the image to 0,0, rotates
    # then moves the center of the image to the center of the destination image which has been resized
    # to accomodate the new image size due to rotation.
    trans = center @ rot @ back

    bp_clib.affine_transform(img, img.ctypes.shape, img.ctypes.strides, trans,
                             dest, dest.ctypes.shape, dest.ctypes.strides)
    return dest


def rescale(img: np.ndarray, scale: float = 2) -> np.ndarray:
    """Re-sizes the image uniformly based on a scale factor

    Args:
        img: The image to scale.
        scale: Non-zero positive number multiplied by the width and height of the image
            to determine the dimensions of the resulting image.  

    Returns:
        A new ndarray containing the result of the scale
    """
    if(scale <= 0):
        raise ValueError('Scale must be greater than zero')

    # calculate the dimensions of the scaled image
    height = round(img.shape[0] * scale)
    width = round(img.shape[1] * scale)
    dest = np.zeros((height, width, 3), dtype=np.uint8)

    tform = _inverse_transform(scale_x=scale, scale_y=scale)
    bp_clib.affine_transform(img, img.ctypes.shape, img.ctypes.strides, tform,
                             dest, dest.ctypes.shape, dest.ctypes.strides)
    return dest


def shear(img: np.ndarray, shear_x: float = .25, shear_y: float = .25) -> np.ndarray:
    """Shears the image in the specified dimension(s)

    Args:
        img: The image to shear.
        shear_x: The amount to shear the image in the x axis
        shear_y: The amount to shear the image in the y axis  

    Returns:
        A new ndarray containing the result of the shear
    """
    # start with a basic shear matrix
    tform = _inverse_transform(shear_x=shear_x, shear_y=shear_y)

    # calculate the new dimensions of the image based after the shear is applied
    height, width = _calc_new_img_size(img.shape, tform)
    dest = np.zeros((height, width, 3), dtype=np.uint8)

    # if applying a negative shear factor then we need to apply an
    # offset to the images final position so it remains "in frame"
    if shear_x < 0:
        tform = tform @ _inverse_transform(offset_x=abs(width - img.shape[1]))
    if shear_y < 0:
        tform = tform @ _inverse_transform(offset_y=abs(height - img.shape[0]))

    bp_clib.affine_transform(img, img.ctypes.shape, img.ctypes.strides, tform,
                             dest, dest.ctypes.shape, dest.ctypes.strides)
    return dest


def _calc_new_img_size(src_shape, inv_transform):
    # get the four corners of the image
    bounds = np.array([[0, 0, 1],
                       [0, src_shape[1], 1],
                       [src_shape[0], 0, 1],
                       [src_shape[0], src_shape[1], 1]])
    # transformation matrix provided is for backwards mapping, but we need to forward map because
    # we're calculating the dimensions of the destination image, so invert the inverse to get the original transform.
    transform = np.linalg.inv(inv_transform)
    # apply the transformation matrix to each point to get the extemities of the image.
    result = bounds @ transform
    # the final dimensions will be determined by range of the extremity points.
    height = round(np.ptp(result[:, 0]))
    width = round(np.ptp(result[:, 1]))

    return (height, width)


def _inverse_transform(scale_x: float = 1, shear_x: float = 0, offset_x: float = 0, scale_y: float = 1, shear_y: float = 0, offset_y: float = 0) -> np.ndarray:
    """Generates an inverse transformation matrix with the given parameters.
    Inverse transformation matricies are used because the affine function does inverse mapping,
    that is calculating the source image pixel from on the destination image pixel. 
    """
    return np.linalg.inv(np.array([[scale_x, shear_x, offset_x],
                                   [shear_y, scale_y, offset_y],
                                   [0, 0, 1]], dtype=np.float32))
