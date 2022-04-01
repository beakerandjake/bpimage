import ctypes
import numpy as np

# load the convovle function written in c and configure so we can invoke it.
_convolve_clib = ctypes.cdll.LoadLibrary('./convolve.so')
_convolve_clib.convolve.restype = None
_convolve_clib.convolve.argtypes = [np.ctypeslib.ndpointer(np.float32, ndim=3),
                                    ctypes.POINTER(np.ctypeslib.c_intp),
                                    ctypes.POINTER(np.ctypeslib.c_intp),
                                    np.ctypeslib.ndpointer(np.float32, ndim=2),
                                    ctypes.POINTER(np.ctypeslib.c_intp),
                                    ctypes.POINTER(np.ctypeslib.c_intp),
                                    ctypes.c_float,
                                    np.ctypeslib.ndpointer(np.float32, ndim=3)]

# overall vision
# add setup.py for end users
#
# one convolve method pass in kernel object
# validate kernel shape / img shape / depth (use decorator?) add convovle error
# handling keyboard interrupt in c?
# take images as rgb uint8, do temp math in c as float then clamp back
# explore pad vs unpad performance memory vs cpu
#


def boxblur(img: np.ndarray, radius: int = 1) -> np.ndarray:
    """Applies a box blur of the specified size to the image.

    Args:
        img: The image to blur.
        radius: number of pixels to take in each direction. a radius of zero or below does nothing

    Returns:
        A new ndarray containing the result of the blur operation
    """
    if radius < 1:
        return img

    size = (radius*2)+1
    boxkern = np.full(np.full(2, size), 1/size**2, dtype=np.float32)

    return _clip(_convolve(img.astype(np.float32), boxkern))


def outline(img: np.ndarray) -> np.ndarray:
    """Applies an edge detection kernel to the image.

    Args:
        img: The image to apply the operation to.

    Returns:
        A new ndarray containing the result of the edge detection operation
    """
    kern = np.array([[-1, -1, -1],
                     [-1, 8, -1],
                     [-1, -1, -1]], dtype=np.float32)
    return _clip(_convolve(img.astype(np.float32), kern))


def sharpen(img: np.ndarray) -> np.ndarray:
    """Applies a sharpening kernel to the image.

    Args:
        img: The image to sharpen.

    Returns:
        A new ndarray containing the result of the sharpening operation
    """
    kern = np.array([[0, -1, 0],
                     [-1, 5, -1],
                     [0, -1, 0]], dtype=np.float32)
    return _clip(_convolve(img.astype(np.float32), kern))


def emboss(img: np.ndarray) -> np.ndarray:
    """Applies an emboss kernel to the image.

    Args:
        img: The image to emboss.

    Returns:
        A new ndarray containing the result of the emboss operation
    """
    kern = np.array([[1, 1, 0],
                     [1, 0, -1],
                     [0, -1, -1]], dtype=np.float32)
    # kern = np.array([[ 1, 0, 1, 0, 0],
    #                  [ 0, 1, 1, 0, 0],
    #                  [ 1, 1, 0,-1,-1],
    #                  [ 0, 0,-1,-1, 0],
    #                  [ 0, 0,-1, 0,-1]], dtype=np.float32)
    return _clip(_convolve(img.astype(np.float32), kern, bias=128.0))


def motion_blur(img: np.ndarray) -> np.ndarray:
    """Applies motion blur to the image.

    Args:
        img: The image to blur.

    Returns:
        A new ndarray containing the result of the motion blur operation
    """
    size = 9
    kern = np.zeros((size, size), dtype=np.float32)
    np.fill_diagonal(np.fliplr(kern), (1/size))

    return _clip(_convolve(img.astype(np.float32), kern))


def smooth(img: np.ndarray) -> np.ndarray:
    """Applies a smoothing kernel to the image.

    Args:
        img: The image to smooth.

    Returns:
        A new ndarray containing the result of the smooth operation
    """
    kern = np.array([[1, 1,  1, 1, 1],
                     [1, 5,  5, 5, 1],
                     [1, 5, 44, 5, 1],
                     [1, 5,  5, 5, 1],
                     [1, 1,  1, 1, 1]], dtype=np.float32) / 100
    return _clip(_convolve(img.astype(np.float32), kern))


def _clip(img):
    return np.clip(img, 0, 255).astype(np.uint8)


def _convolve(img: np.ndarray, kern: np.ndarray, bias=0.0) -> np.ndarray:
    """Applies the kernel to the image, delegating the convolve to the c library.
    """
    # if img.ndim != 3 or img.shape[-1] != 3 or img.dtype != np.uint8:
    #     raise ValueError('Image must be RGB (0-255).')
    if kern.dtype != np.float32 or kern.ndim != 2 or kern.shape[0] != kern.shape[1] or kern.shape[0] % 2 == 0 or kern.shape[0] <= 1:
        raise ValueError(
            'Kernel must be a NxN square of floats where N is an odd number greater than one.')
    if kern.shape > img.shape[:2]:
        raise ValueError('Image must be larger than Kernel')

    dest = np.zeros_like(img)
    _convolve_clib.convolve(img, img.ctypes.strides, img.ctypes.shape, kern,
                            kern.ctypes.strides, kern.ctypes.shape, bias, dest)
    return dest
