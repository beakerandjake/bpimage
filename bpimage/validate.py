
"""Module which contains functions to perform common validation checks against images. 
This ensures that our clibs are provided data they expect. 
"""
import numpy as np

def ensure_8bit_rbg(*args: np.ndarray):
    """Checks whether each ndarray represents a valid 8-bit RGB image.

    Args:
        args: All ndarrays to validate, each arg will be validated.

    Raises:
        ValueError: An ndarray failed to validate.
    """
    for img in args:
        if img.flags.c_contiguous == False:
            raise ValueError("Image array must have a C Contiguous memory layout.")
        if img.ndim != 3:
            raise ValueError("Image array must have exactly three dimensions.")
        if img.dtype != np.uint8:
            raise ValueError("Image array must have an 8bit (0-255) color depth, this corresponds to a dtype of np.uint8.")
        if img.shape[-1] != 3:
            raise ValueError('Image array must have a color model of RGB.')
