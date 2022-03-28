import numpy as np

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
    kern = np.array([[ 0, 1, 0],
                     [ 1, 0,-1],
                     [ 0,-1, 0]], dtype=np.float32)
    return _clip(_convolve_padded(img.astype(np.float32),_kern3d(kern),bias=128.0))



def boxblur(img:np.ndarray, radius:int=1) -> np.ndarray:  
    if radius < 1:
        return img

    size = (radius*2)+1 
    boxkern = np.full(np.full(2,size), 1/size**2, dtype=np.float32)

    return _clip(_convolve_padded(img.astype(np.float32),_kern3d(boxkern)))

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
                    # print(f'kernel: ({(ky,kx)}) = {kern[ky,kx]} -> offset: {oy,ox} -> window: {(wy,wx)} -> pmod: {pix} -> acc: {acc}'
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