"""Module responsible for loading, saving and displaying images.
Hides the implementation details of these operations so backing libraries
can be switched out with ease. Provides standardized exceptions which simplify error handling.
"""
import numpy as np
from PIL import Image, ImageShow, UnidentifiedImageError

def open(path:str) -> np.ndarray:
    """Attempts to load an image file and returns an ndarray

    Args:
        path: filepath to the image

    Returns:
        An ndarray of shape (w,h,3) containing the image data

    Raises:
        ImageOpenError: raised when something goes wrong loading the image 
    """
    try:
        with Image.open(path) as img:
            return np.array(img)
    except IsADirectoryError as e: 
        raise ImageOpenError(f'Cannot open \'{path}\': Expected image but provided directory') from e
    except FileNotFoundError as e:
        raise ImageOpenError(f'Cannot open \'{path}\': No such file or directory') from e
    except UnidentifiedImageError as e:
        raise ImageOpenError(f'Cannot open \'{path}\': Failed to open image, is this a valid image file?') from e
    except Exception as e:
        raise ImageOpenError(f'Unexpected error opening \'{path}\': {str(e)}') from e

def save(img:np.ndarray, path:str):
    """Attempts to save an ndarray of image data as an image with the given file name. 

    Args:
        img: the ndarray of image data to save
        path: the filename to save the image as

    Returns:
        None

    Raises:
        ImageSaveError: Raised when something goes wrong saving the image 
    """
    try:
        Image.fromarray(img).save(path)
    except ValueError as e:
        raise ImageSaveError(f'Cannot save \'{path}\': could not determine output image format') from e
    except OSError as e:
        raise ImageSaveError(f'Failed to save \'{path}\': {e.strerror}') from e

def show(img):
    """Attempts to save an ndarray of image data as an image with the given file name. 

    Args:
        img: the ndarray of image data to save
        path: the filename to save the image as

    Returns:
        None

    Raises:
        ImageSaveError: Raised when something goes wrong saving the image 
    """
    try:
        if not ImageShow.show(Image.fromarray(img)):
            raise ImageShowError("Failed to show image")
    except Exception as e:
        raise ImageShowError(f"Unexpected error showing image: {str(e)}") from e


class ImageOpenError(Exception):
    """Raised when something went wrong opening an image file"""
    pass

class ImageSaveError(Exception):
    """Raised when something went wrong saving an image file"""
    pass

class ImageShowError(Exception):
    """Raised when something went wrong displaying an image file"""
    pass