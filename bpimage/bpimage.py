import numpy as np
from ctypes import cdll

# overall vision 
# use config to choose convolve implementation in python or in c
# add setup.py for end users
# 
# todo
# set argtypes and restype
# 
# implementation iteration
# 1. pass 1d numpy array in
#        iterate the array and print
#        change a value
# 2. pass 2d numpy array in
#        iterate the array and print
#        change a value
# 3. pass 3d numpy array in
#        iterate the array and print
#        change a value
# 4. pass actual arguments img, kernel, bias
# 5. probably want to also pass destination as argument instead of trying to allocate new array in c....
# 6. once actual arguments are in, iterate every pixel and calculate window
# 7. set every pixel in destination to source value
# 7. determine how to handle boundaries? assume array is padded? or use c to extend indexes? 
# 8. actually do the convolve.. 
lib = cdll.LoadLibrary('./convolve.so')
result = lib.add(1,65)


def boxblur(img:np.ndarray, radius:int=1) -> np.ndarray: 
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
    boxkern = np.full(np.full(2,size), 1/size**2, dtype=np.float32)

    return _clip(_convolve_padded(img.astype(np.float32),_kern3d(boxkern)))

def outline(img:np.ndarray) -> np.ndarray:
    """Applies an edge detection kernel to the image. 

    Args:
        img: The image to apply the operation to. 

    Returns:
        A new ndarray containing the result of the edge detection operation
    """
    kern = np.array([[-1,-1,-1],
                     [-1, 8,-1],
                     [-1,-1,-1]], dtype=np.float32)
    return _clip(_convolve_padded(img.astype(np.float32),_kern3d(kern)))

def sharpen(img:np.ndarray) -> np.ndarray:
    """Applies a sharpening kernel to the image. 

    Args:
        img: The image to sharpen. 

    Returns:
        A new ndarray containing the result of the sharpening operation
    """
    kern = np.array([[ 0,-1, 0],
                     [-1, 5,-1],
                     [ 0,-1, 0]], dtype=np.float32)
    return _clip(_convolve_padded(img.astype(np.float32),_kern3d(kern)))

def emboss(img:np.ndarray) -> np.ndarray:
    """Applies an emboss kernel to the image. 

    Args:
        img: The image to emboss. 

    Returns:
        A new ndarray containing the result of the emboss operation
    """
    kern = np.array([[ 1, 1, 0],
                     [ 1, 0,-1],
                     [ 0,-1,-1]], dtype=np.float32)
    # kern = np.array([[ 1, 0, 1, 0, 0],
    #                  [ 0, 1, 1, 0, 0],
    #                  [ 1, 1, 0,-1,-1],
    #                  [ 0, 0,-1,-1, 0],
    #                  [ 0, 0,-1, 0,-1]], dtype=np.float32)
    return _clip(_convolve_padded(img.astype(np.float32),_kern3d(kern),bias=128.0))

def motion_blur(img:np.ndarray) -> np.ndarray:
    """Applies motion blur to the image. 

    Args:
        img: The image to blur. 

    Returns:
        A new ndarray containing the result of the motion blur operation
    """
    size = 9
    kern = np.zeros((size,size), dtype=np.float32)
    np.fill_diagonal(np.fliplr(kern), (1/size))

    return _clip(_convolve_padded(img.astype(np.float32),_kern3d(kern)))

def smooth(img:np.ndarray) -> np.ndarray:
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
    return _clip(_convolve_padded(img.astype(np.float32),_kern3d(kern)))

def _convolve_padded(img, kern,bias=0.0):
    """convolve that extends the image boundaries via padding"""
    dest = np.empty_like(img)
    krad = kern.shape[0] // 2
    kh,kw = kern.shape[:2]
    pad = np.pad(img,((krad,krad),(krad,krad),(0,0)),'edge')

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            dest[y,x] = np.sum(pad[y:y+kh,x:x+kw]*kern, axis=(0,1)) + bias

    return dest
    
def _clip(img):
    # return (img * 255.0).astype(np.uint8)
    return np.clip(img,0,255).astype(np.uint8)

def _kern3d(kern1d):
    return np.repeat(kern1d[...,None],3,axis=-1)

def _convolve_slow(img,kern):
    """naive convolve operation using loops, very slow."""
    dest = np.zeros_like(img)
    h,w = img.shape[:2]
    kh,kw = kern.shape[:2]
    kpad = kw // 2
    
    for y in range(h):
        for x in range(w):
            for ky in range(kh):
                for kx in range(kw):
                    dest[y,x] += kern[ky,kx] * img[_clamp(y+ky-kpad,h-1),_clamp(x+kx-kpad,w-1)]
    return dest

def _clamp(n,max_n):
    return max(0,min(n, max_n))

def _convolve_skip_boundary(img,kern):
    """convolve that ignores the boundaries, faster than _convolve_slow"""
    dest = np.zeros_like(img)
    h,w = img.shape[:2]
    krad = kern.shape[0] // 2

    for y in range(krad, h-krad):
        for x in range(krad, w-krad):
            dest[y,x] = np.sum(img[y-krad:y+krad+1,x-krad:x+krad+1]*kern, axis=(0,1))
            
    return dest