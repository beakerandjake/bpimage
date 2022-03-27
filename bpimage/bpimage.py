
from calendar import c
from cgi import print_exception
import numpy as np


boxblur = np.full((3,3), 1/9)
gaussian = np.array([[1,2,1],[2,4,2],[1,2,1]]) / 16
emboss = np.array([[-2,-1,0],[-1,1,1],[0,1,2]])

def blur(img: np.ndarray):
    return _convolve(img, gaussian)            

def _convolve(img,kernel):
    dest = np.empty_like(img)
    h,w = img.shape[:2]
    kh,kw = kernel.shape
    kpad = kw // 2
    kern = kernel[::-1,::-1]
    
    # _print_pixels(img)
    # print(kernel)
    # print(kh,kw)
    # print(kpad)

    for y in range(h):
        for x in range(w):
            # print(f'img: {(y,x)}')
            acc = 0
            # iterate over kernal
            for ky in range(kh):
                for kx in range(kw):
                    # acc += kernel[kh-ky-1,kw-kx-1] * img[_clamp(ky-kpad+y,kh-1),_clamp(kx-kpad+x,kw-1)]
                    acc += kernel[kh-ky-1,kw-kx-1] * img[_clamp(y+ky-kpad,kh-1),_clamp(x+kx-kpad,kw-1)]
                    # print(f'kernel: ({kh-ky-1},{kw-kx-1}) -> window: {(ky,kx)} -> offset: {(ky-kpad+y, kx-kpad+x)} -> img: {(_clamp(y+ky-kpad,kh-1),_clamp(x+kx-kpad,kw-1))}')
            dest[y,x] = acc
            # print('---')

    return dest

def _clamp(n,max_n):
    return max(0,min(n, max_n))

def _pad(img):
    ret = np.zeros((img.shape[0]+2, img.shape[1]+2, img.shape[2]), dtype=img.dtype)
    # fill the center with the original image
    ret[1:-1,1:-1] = img
    # extend the image out to the padded rows (skipping the corners)
    ret[0, 1:-1] = img[0]
    ret[-1, 1:-1] = img[-1]
    ret[1:-1,0] = img[:,0]
    ret[1:-1,-1] = img[:,-1]
    # add the corners of the padded rows
    ret[0,0] = img[0,0]
    ret[0,-1] = img[0,-1]
    ret[-1,0] = img[-1,0]
    ret[-1,-1] = img[-1,-1]
    return ret

def _print_pixels(image):
    if image.ndim != 3:
        print(image)
    else:
        print('\n'.join(','.join(f'[{pixel[0]:>3}, {pixel[1]:>3}, {pixel[2]:>3}]' for pixel in row) for row in image), end='\n\n')