
import numpy as np


blur_kernal = np.ones((3,3)) * 1/9
'''
    1    [1,1,1],
    - *  [1,1,1],
    9    [1,1,1]  
'''

def blur(img: np.ndarray):
    dest = np.zeros_like(img)
    h,w = img.shape[:2]

    for y in range(h):
        for x in range(w):
            window = img[max(0,y-1):min(y+2,h), max(0,x-1):min(x+2,w)]
            result = np.sum(window, axis=(0,1)) / 9
            dest[y,x] = result

            # print('x',x,'y',y,'pixel', img[y,x])
            # # print(f'slice: {max(0,y-1)}:{min(y+2,h)},{max(0,x-1)}:{min(x+2,w)}')
            # # print(window)
            # print(window)
            # print('==')
            # print(np.sum(window, axis=-1))
            # print('-----')
            # print()
    
    return dest
            

def _convolve(img,kernel):
    dest = np.zeros_like(img)
    h,w = img.shape[:2]

    for y in range(h):
        for x in range(w):
            pass

    return dest