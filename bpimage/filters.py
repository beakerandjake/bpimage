"""Functions for filtering images by applying kernels to each pixel using convolution
"""
import ctypes
import numpy as np

# load the convovle function written in c and configure so we can invoke it.
_convolve_clib = ctypes.cdll.LoadLibrary('./bpimage.so')
_convolve_clib.convolve.restype = None
_convolve_clib.convolve.argtypes = [np.ctypeslib.ndpointer(np.uint8, ndim=3),
                                    np.ctypeslib.ndpointer(np.float32, ndim=2),
                                    np.ctypeslib.ndpointer(np.uint8, ndim=3),
                                    ctypes.c_float,
                                    ctypes.POINTER(np.ctypeslib.c_intp),
                                    ctypes.POINTER(np.ctypeslib.c_intp)]


def gaussian_blur(img: np.ndarray, radius: int = 1, sig: float = 1.) -> np.ndarray:
    """Applies a gaussian blur to the image.

    Args:
        img: The image to blur.
        radius: The number of pixels to take in each direction. A radius of zero or below does nothing.
        sig: The sigma of the gaussian function

    Returns:
        A new ndarray containing the result of the gaussian blur operation
    """
    if radius < 1:
        return img

    # generate the gaussian kernel
    # https://stackoverflow.com/questions/29731726/how-to-calculate-a-gaussian-kernel-matrix-efficiently-in-numpy
    size = (radius * 2) + 1
    ax = np.linspace(-(size - 1) / 2., (size - 1) /
                     2., size, dtype=np.float32)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kern = np.outer(gauss, gauss)
    kern = kern / np.sum(kern)

    return _convolve(img, kern)


def boxblur(img: np.ndarray, radius: int = 1) -> np.ndarray:
    """Blurs each pixel by averaging all surrounding pixels extending radius pixels in each direction.

    Args:
        img: The source RGB image with shape=(h,w,3).
        radius: Number of pixels to take in each direction.

    Returns:
        A new ndarray with dtype=uint8 and shape=(h,w,3).

    Raises:
        ValueError: img was not RGB.
        ValueError: radius was less than one.
    """
    if radius < 1:
        raise ValueError('Radius must be positive.')

    # create a kernel with the desired radius.
    size = (radius*2)+1
    kern = np.full(np.full(2, size), 1/size**2, dtype=np.float32)

    return _convolve(img, kern)


def outline(img: np.ndarray) -> np.ndarray:
    """Highlights edges of the image. 

    Args:
        img: The source RGB image with shape=(h,w,3).

    Returns:
        A new ndarray with dtype=uint8 and shape=(h,w,3).

    Raises:
        ValueError: img was not RGB.
    """
    kern = np.array([[-1, -1, -1],
                     [-1, 8, -1],
                     [-1, -1, -1]], dtype=np.float32)
    return _convolve(img, kern)


def sharpen(img: np.ndarray, strength: float = 5.0) -> np.ndarray:
    """Sharpens the image.

    Args:
        img: The source RGB image with shape=(h,w,3).
        strength: The strength of the sharpen affect (higher values may result in artifacts). 

    Returns:
        A new ndarray with dtype=uint8 and shape=(h,w,3).

    Raises:
        ValueError: img was not RGB.
        ValueError: The strength was negative.
    """
    if strength < 0:
        raise ValueError('Strength must be positive.')

    # build a sharpening kernel with the specified strength.
    # use formula defined in: https://en.wikipedia.org/wiki/Unsharp_masking#Digital_unsharp_masking

    a = np.array([[0, 0, 0],
                  [0, 1, 0],
                  [0, 0, 0]], dtype=np.float32)

    b = np.array([[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]], dtype=np.float32) / 5

    kern = a + ((a - b) * strength)

    return _convolve(img, kern)


def emboss(img: np.ndarray, direction: str, strength: int = 1) -> np.ndarray:
    """Applies an emboss effect to the image.

    Args:
        img: The source RGB image with shape=(h,w,3).
        direction: One of the following supported values.
            'u' 
                Emboss from top to bottom   
            'd'
                Emboss from bottom to top
            'l'
                Emboss from left to right
            'r'
                Emboss from right to left
        strength: The number of surrounding pixels to take in each direction.  

    Returns:
        A new ndarray with dtype=uint8 and shape=(h,w,3).
    
    Raises:
        ValueError: Provided an invalid direction. 
        ValueError: Provided a strength less than one. 
    """
    return _convolve(img, _get_emboss_kern(direction, strength=strength), bias=128.0)


def _get_emboss_kern(direction, strength):
    """Returns an emboss kernel which highlights in a given direction, with a strength to control the depth of the shadows.
    """
    if strength < 1:
        raise ValueError("Strength must greater than or equal to one.")

    # generate a kernel with 'strength' number of pixels surrounding the center. 
    length = (strength * 2) + 1
    center = length // 2
    kern = np.zeros((length, length), dtype=np.float32)

    # top to bottom
    if direction == 'u':
        kern[0:center, center] = 1
        kern[center+1:, center] = -1
    # bottom to top
    elif direction == 'd':
        kern[0:center, center] = -1
        kern[center+1:, center] = 1
    # left to right
    elif direction == 'l':
        kern[center, :center] = 1
        kern[center, center+1:] = -1
    # right to left
    elif direction == 'r':
        kern[center, :center] = -1
        kern[center, center+1:] = 1
    else:
        raise ValueError(f'Unknown emboss direction: \'{direction}\'')

    return kern


def motion_blur(img: np.ndarray) -> np.ndarray:
    """Applies motion blur to the image.

    Args:
        img: The source RGB image with shape=(h,w,3).

    Returns:
        A new ndarray with dtype=uint8 and shape=(h,w,3).

    Raises:
        ValueError: img was not RGB.
    """
    # create a kernel with ones on a diagonal going from right to left.
    size = 9
    kern = np.zeros((size, size), dtype=np.float32)
    np.fill_diagonal(np.fliplr(kern), (1/size))

    return _convolve(img, kern)


def _convolve(img: np.ndarray, kern: np.ndarray, bias=0.0) -> np.ndarray:
    """Applies the kernel to the image, delegating the convolve to the c library.
    """
    if img.shape[-1] != 3:
        raise ValueError('Expected RGB Image array of shape (h,w,3).')
    if kern.dtype != np.float32 or kern.ndim != 2 or kern.shape[0] != kern.shape[1] or kern.shape[0] % 2 == 0 or kern.shape[0] <= 1:
        raise ValueError(
            'Kernel must be a NxN square of floats where N is an odd number greater than one.')
    if kern.shape > img.shape[:2]:
        raise ValueError('Image must be larger than Kernel')

    # pad source image for easy bounds handling at the expense of memory
    # also ensures the new array will also be laid out in memory how the convolve method expects
    krad = kern.shape[0] // 2
    img_padded = np.ascontiguousarray(
        np.pad(img, ((krad, krad), (krad, krad), (0, 0)), 'edge'))

    # even though we padded the image for the convolve, the destination image will have the same shape as the unpadded source.
    dest = np.empty(img.shape, dtype=np.uint8)

    # invoke our c function to apply the convolution.
    _convolve_clib.convolve(img_padded, kern, dest, bias,
                            img.ctypes.shape, kern.ctypes.shape)
    return dest
