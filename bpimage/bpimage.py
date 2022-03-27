import numpy as np

# boxblur = np.full((9,9), 1/81, dtype=np.float32)
# gaussian = np.array([[1,2,1],[2,4,2],[1,2,1]], dtype=np.float32) / 16
# gaussian_5 = np.array([[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]], dtype=np.float32) / 256
emboss = np.array([[-2,-1,0],[-1,1,1],[0,1,2]], dtype=np.float32)
edge = np.array([[0,1,0],[1,-4,1],[0,1,0]], dtype=np.float32)
edge2 = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32)
sharpen = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], dtype=np.float32)
# top_sobel = np.array([[1,2,1],[0,0,0],[-1,-2,-1]], dtype=np.float32)
# sharpen = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], dtype=np.float32)

def boxblur(img:np.ndarray, radius:int=1) -> np.ndarray:  
    if radius < 1:
        return img
    
    size = (radius*2)+1 
    boxkern = np.full(np.full(2,size), 1/size**2, dtype=np.float32)

    return _clip(_convolve_skip_boundary(img.astype(np.float32),_kern3d(edge2)))

def _convolve_slow(img,kern):
    """naive convolve operation using loops, very slow."""
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

def _convolve_skip_boundary(img,kern):
    """convolve that ignores the boundaries, faster than _convolve_slow"""
    dest = np.zeros_like(img)
    h,w = img.shape[:2]
    krad = kern.shape[0] // 2

    for y in range(krad, h-krad):
        for x in range(krad, w-krad):
            dest[y,x] = np.sum(img[y-krad:y+krad+1,x-krad:x+krad+1]*kern, axis=(0,1))
            
    return dest
    
def _clip(img):
    # return (img * 255.0).astype(np.uint8)
    return np.clip(img,0,255).astype(np.uint8)

def _kern3d(kern1d):
    return np.repeat(kern1d[...,None],3,axis=-1)