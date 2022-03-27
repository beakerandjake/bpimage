import numpy as np

# boxblur = np.full((9,9), 1/81, dtype=np.float32)
# gaussian = np.array([[1,2,1],[2,4,2],[1,2,1]], dtype=np.float32) / 16
# gaussian_5 = np.array([[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]], dtype=np.float32) / 256
# emboss = np.array([[-1,0,0],[0,1,0],[0,0,0]], dtype=np.float32)
# top_sobel = np.array([[1,2,1],[0,0,0],[-1,-2,-1]], dtype=np.float32)
# sharpen = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], dtype=np.float32)

def boxblur(img:np.ndarray, radius:int=1) -> np.ndarray:  
    if radius < 1:
        return img
    
    size = (radius*2)+1 
    boxkern = np.full(np.full(2,size), 1/size**2, dtype=np.float32)

    return _clip(_convolve_skip(img.astype(np.float32), boxkern))

def _convolve_simple(img,kern):
    dest = np.zeros_like(img)
    h,w = img.shape[:2]
    kh,kw = kern.shape
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

def _convolve_skip(img,kern):
    """Convolve but ignore the boundaries"""
    dest = np.zeros_like(img)
    h,w = img.shape[:2]
    kh,kw = kern.shape
    kpad = kw // 2
    
    for y in range(kpad, h-kpad):
        for x in range(kpad, w-kpad):
            for ky in range(kh):
                for kx in range(kw):
                    dest[y,x] += kern[ky,kx] * img[y+ky-kpad,x+kx-kpad]
                    # print(f'kernel: ({(ky,kx)}) = {kern[ky,kx]} -> offset: {oy,ox} -> window: {(wy,wx)} -> pmod: {pix} -> acc: {acc}'
    return dest
    

def _clip(img):
    return np.clip(img,0,255).astype(np.uint8)