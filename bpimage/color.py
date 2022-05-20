
"""Functions for modifying the colors of images.
"""
from asyncio.constants import DEBUG_STACK_DEPTH
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

    # using weighted averages defined in https://en.wikipedia.org/wiki/Grayscale#Converting_colour_to_grayscale
    return (img @ np.array([.2126, .7152, .0722])).astype(np.uint8)


def grayscale2rgb(img: np.ndarray) -> np.ndarray:
    """Converts an image in grayscale format to RGB format.
    Each single 8bit pixel of the image is expanded into RGB channels. 
    The shape of the image will be modified from (h,w) to (h,w,3).

    Args:
        img: The image to convert

    Returns:
        A new ndarray with shape (h,w,3) containing the converted image
    """
    if img.ndim != 2:
        return ValueError("Image must be grayscale.")
    # expand 2d array to 3d and fill the RGB values with the grayscale pixel value.
    return img[:, :, np.newaxis].repeat(3, axis=-1)


def sepia(img: np.ndarray) -> np.ndarray:
    """Applies a sepia tone to an RGB image  

    Args:
        img: The source image image with shape (h,w,3) 

    Returns:
        A new ndarray of dtype uint8 with shape (h,w,3) containing the sepia toned image
    """
    # using common weights defined at https://stackoverflow.com/questions/36434905
    transform = np.array([[.393, .769, .189],
                          [.349, .686, .168],
                          [.272, .534, .131]])
    # clamp the values at 255 to ensure there isnt any overflow when casting back to uint8
    return (img @ transform.T).clip(0, 255).astype(np.uint8)


def brighten(img: np.ndarray, strength: float = 8) -> np.ndarray:
    """Modifies the brightness of the image. 

    Args:
        img: The source 8bit RGB image with shape (h,w,3) 
        strength: The amount to brighten or darken the image.
            A value of 0.0 will result in a black image, 1.0 gives the original image.

    Returns:
        A new ndarray of dtype uint8 with shape (h,w,3) containing the sepia toned image
    """
    # dest = img.astype(np.int32)
    # return (dest + strength).clip(0,255).astype(np.uint8)

    # from PIL import Image, ImageEnhance

    # im = Image.fromarray(img)
    # z = ImageEnhance.Brightness(im)
    # return np.asarray(z.enhance(strength), dtype=np.uint8)

    dest = img.astype(np.float32)
    return (dest * max(0, strength)).clip(0, 255).astype(np.uint8)
