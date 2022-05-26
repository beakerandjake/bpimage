"""Functions for applying transformations to the image such as rotation and scaling.
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
        img: The source RGB image with shape=(h,w,3).

    Returns:
        A new ndarray with dtype=uint8 and shape=(h,w,3).

    Raises:
        ValueError: img was not RGB.
    """
    dest = np.empty(img.shape, dtype=np.uint8)

    # create matrix which flips at the origin then slides it back "in frame"
    tform = _inverse_transform(scale_x=-1, offset_x=img.shape[1]-1)
    
    return _affine_transformation(img, tform, dest)


def fliph(img: np.ndarray) -> np.ndarray:
    """Flips the image across the horizontal, from bottom to top.

    Args:
        img: The source RGB image with shape=(h,w,3).

    Returns:
        A new ndarray with dtype=uint8 and shape=(h,w,3).

    Raises:
        ValueError: img was not RGB.
    """
    dest = np.empty(img.shape, dtype=np.uint8)

    # create matrix which flips at the origin then slides it back "in frame"
    tform = _inverse_transform(scale_y=-1, offset_y=img.shape[0] - 1)

    return _affine_transformation(img, tform, dest)


def rotate90(img: np.ndarray, times: int = 1) -> np.ndarray:
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


def rotate(img: np.ndarray, angle: float = 45, expand=True) -> np.ndarray:
    """Rotates the image counter-clockwise by a specified angle around the center

    Args:
        img: The image to rotate.
        angle: The amount to rotate in degrees. 
        expand: If true, expands the dimensions of resulting image so it's large enough to hold the entire rotated image. 

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
    height, width = img.shape[:2] if expand == False else _calc_new_img_size(
        img.shape, rot)
    dest = np.zeros((height, width, 3), dtype=np.uint8)

    # matrix to move the center of the image from the origin to the center of the destination image.
    back = np.array([[1, 0, -width//2],
                     [0, 1, -height//2],
                     [0, 0, 1]], dtype=np.float32)

    # generate the final transformation matrix which moves the center of the image to 0,0, rotates
    # then moves the center of the image to the center of the destination image which has been resized
    # to accomodate the new image size due to rotation.
    tform = center @ rot @ back

    return _affine_transformation(img, tform, dest)


def scale(img: np.ndarray, scale: float) -> np.ndarray:
    """Re-sizes the image uniformly based on a scale factor

    Args:
        img: The image to scale.


    Returns:
        A new ndarray containing the result of the scale


    Args:
        img: The source RGB image with shape=(h,w,3).
        scale: Non-zero positive number multiplied by the width and height of the image
            to determine the dimensions of the resulting image.  

    Returns:
        A new ndarray with dtype=uint8 and shape=(h * scale,w * scale, 3).

    Raises:
        ValueError: img was not RGB.
        ValueError: scale was less than or equal than zero.
    """
    if(scale <= 0):
        raise ValueError('Scale must be greater than zero')

    # matrix to scale the image uniformly in the x and y dimension
    tform = _inverse_transform(scale_x=scale, scale_y=scale)

    # calculate the dimensions of the image after scaling is applied
    height, width = _calc_new_img_size(img.shape, tform)
    dest = np.empty((height, width, 3), dtype=np.uint8)

    return _affine_transformation(img, tform, dest)


def shear(img: np.ndarray, shear_x: float = 1.0, shear_y: float = 1.0, expand=True) -> np.ndarray:
    """Shears the image in the specified dimension(s)

    Args:
        img: The image to shear.
        shear_x: The amount to shear the image in the x axis
        shear_y: The amount to shear the image in the y axis
        expand: If true, expands the dimensions of resulting image so it's large enough to hold the entire skewed image. 

    Returns:
        A new ndarray containing the result of the shear
    """
    # start with a basic shear matrix
    tform = _inverse_transform(shear_x=shear_x, shear_y=shear_y)

    # calculate the new dimensions of the image based after the shear is applied
    height, width = img.shape[:2] if expand == False else _calc_new_img_size(
        img.shape, tform)
    dest = np.zeros((height, width, 3), dtype=np.uint8)

    # if applying a negative shear factor then we need to apply an
    # offset to the images final position so it remains "in frame"
    if shear_x < 0 and expand == True:
        tform = tform @ _inverse_transform(offset_x=abs(width - img.shape[1]))
    if shear_y < 0 and expand == True:
        tform = tform @ _inverse_transform(offset_y=abs(height - img.shape[0]))

    return _affine_transformation(img, tform, dest)


def _calc_new_img_size(src_shape: tuple[int, int], inv_transform: np.ndarray) -> tuple[int, int]:
    """Determines the size of the image after the transform is applied to it.

    Args:
        src_shape: A tuple containing the source images height and width respectively. 
        inv_transform: The inverse transformation matrix that will be applied to the image.  

    Returns:
        A tuple containing the destination images height and width respectively.
    """
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
    return (round(np.ptp(result[:, 0])), round(np.ptp(result[:, 1])))


def _inverse_transform(scale_x: float = 1, shear_x: float = 0, offset_x: float = 0, scale_y: float = 1, shear_y: float = 0, offset_y: float = 0) -> np.ndarray:
    """Generates an inverse transformation matrix with the given parameters.
    Inverse transformation matricies are used because the affine function does inverse mapping,
    that is calculating the source image pixel from on the destination image pixel. 
    """
    return np.linalg.inv(np.array([[scale_x, shear_x, offset_x],
                                   [shear_y, scale_y, offset_y],
                                   [0, 0, 1]], dtype=np.float32))


def _affine_transformation(src: np.ndarray, inv_transform: np.ndarray, dest: np.ndarray):
    """Applies the affine transformation to the source and writes the result to the destination.
    """
    if src.shape[-1] != 3 or dest.shape[-1] != 3:
        raise ValueError('Expected RGB Image array of shape (h,w,3).')

    bp_clib.affine_transform(src, src.ctypes.shape, src.ctypes.strides, inv_transform,
                             dest, dest.ctypes.shape, dest.ctypes.strides)
    return dest
