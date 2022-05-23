
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

    # clamp the values to ensure there isnt any overflow when casting from float back to uint8
    return np.clip(img @ transform.T, 0, 255).astype(np.uint8)


def brightness(img: np.ndarray, strength: float = .05) -> np.ndarray:
    """Modifies the brightness of the image.

    Args:
        img: The source 8bit RGB image with shape (h,w,3)
        strength: The amount to brighten or darken the image.
            A value of 0.0 will result in a black image, 1.0 gives the original image.

    Returns:
        A new ndarray of dtype uint8 with shape (h,w,3) containing the sepia toned image
    """
    # Since we're multiplying by a scale it's going to be likely that the uint8 values will overflow.
    # To get around this upcast the image to a larger data type, then clip back to uint8 range.
    return np.clip(img.astype(np.float32) * strength, 0, 255).astype(np.uint8)


def invert(img: np.ndarray) -> np.ndarray:
    """Create a negative of the image. 

    Args:
        img: The source 8bit RGB image with shape (h,w,3) 

    Returns:
        A new ndarray of dtype uint8 with shape (h,w,3) containing inverted image.
    """
    return 255 - img


def contrast(img: np.ndarray, strength: float = 1.75) -> np.ndarray:
    # We are expecting a 8bit rgb image.
    # When multiplying these pixel values the results will likely be greater than 255.
    # These values would wraparound, which would give weird results even with a clip at the end.
    # This is because values greater than 255 will have aready wrapped around before the clip.
    #
    # To get around this and at the cost of memory and runtime performance,
    # Upcast the image to be stored as a float. This ensures we can hold values without wrap around.
    img = img.astype(np.float32)

    # use formula described in http://www.graficaobscura.com/interp/index.html
    # lerp the image from its average pixel color (gray).
    return (((1.0 - strength) * img.mean()) + (strength * img)).clip(0, 255).astype(np.uint8)


def saturation(img: np.ndarray, strength: float = -2.5) -> np.ndarray:
    # cast the image to float to handle overflow which could happen before the clip.
    img = img.astype(np.float32)

    # use formula described in http://www.graficaobscura.com/interp/index.html
    # lerp the image from its grayscale version
    blackandwhite = grayscale2rgb(rgb2grayscale(img))
    return (((1.0 - strength) * blackandwhite) + (strength * img)).clip(0, 255).astype(np.uint8)
