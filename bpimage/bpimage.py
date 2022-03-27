
from calendar import c
import numpy as np
from cprof import cprof

# boxblur = np.full((9,9), 1/81, dtype=np.float32)
# gaussian = np.array([[1,2,1],[2,4,2],[1,2,1]], dtype=np.float32) / 16
# gaussian_5 = np.array([[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]], dtype=np.float32) / 256
# emboss = np.array([[-1,0,0],[0,1,0],[0,0,0]], dtype=np.float32)
# top_sobel = np.array([[1,2,1],[0,0,0],[-1,-2,-1]], dtype=np.float32)
# sharpen = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], dtype=np.float32)

@cprof('profram.prof')
def boxblur(img:np.ndarray, radius:int=1) -> np.ndarray:  
    if radius < 1:
        return img
    
    size = (radius*2)+1 
    boxkern = np.full(np.full(2,size), 1/size**2, dtype=np.float32)

    return _clip(_convolve(img.astype(np.float32), boxkern))

def _convolve(img,kernel):
    dest = np.empty_like(img)
    h,w = img.shape[:2]
    kh,kw = kernel.shape
    kpad = kw // 2
    kern = kernel[::-1,::-1]
    
    for y in range(h):
        for x in range(w):
            # print(f'img: {(y,x)} -> {img[y,x]}')
            acc = np.zeros(3, dtype=np.float32)
            for ky in range(kh):
                for kx in range(kw):
                    oy = y+ky-kpad
                    ox = x+kx-kpad
                    wy = _clamp(oy,h-1)
                    wx = _clamp(ox,w-1)
                    pix = kern[ky,kx] * img[wy,wx]
                    acc += pix
                    # print(f'kernel: ({(ky,kx)}) = {kern[ky,kx]} -> offset: {oy,ox} -> window: {(wy,wx)} -> pmod: {pix} -> acc: {acc}')
            # print(f'new pixel: {acc}')
            dest[y,x] = acc
            # print('---')

    return dest

def _clamp(n,max_n):
    return max(0,min(n, max_n))

def _clip(img):
    return np.clip(img,0,255).astype(np.uint8)