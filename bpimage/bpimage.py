
from cgi import print_exception
import numpy as np


blur_kernal = np.full((3,3), 1/9)
'''
    1    [1,1,1],
    - *  [1,1,1],
    9    [1,1,1]  
'''

g_kernel = np.array([[1,2,1],[2,4,2],[1,2,1]]) / 16

def blur(img: np.ndarray):
    return _convolve(img, g_kernel)            

def _convolve(img,kernel):
    dest = np.empty_like(img)
    h,w = img.shape[:2]
    kh,kw = kernel.shape

    print(kernel.shape)
    print(h,w)

    # for y in range(h):
    #     for x in range(w):
    #         acc = 0
            
    #         for ky in range(3):
    #             for kx in range(3):
    #                 acc += kernel[ky,kx] * window[ky,kx]

    #         # r = np.sum(window * kernel, axis=(0,1))
    #         # _print_pixels(window)
    #         # print(acc)
    #         # _print_pixels(window * kernel)
    #         dest[y-1,x-1] = acc
    #         # return dest

    return dest

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