#include <stdio.h>
#include "common.h"

#define COLOR_DEPTH 3

/*
Applies a convolution kernel to the image and writes the result to the destination image.

@param img_padded: A version of the source image padded on all sides by the kernel.
Expected to have shape of (img height + kern height -1, img width + kern width - 1, 3).
Expected to be in contigious row major layout.

@param kern: The convolution kernel to apply to the image.
Expected to be a contigious 2 dimensional array in row major order with shape (N,N) where N is an odd number > 1

@param dest: The destination image to write the results to.
Expected to have the same shape as the original unpadded image. (img height, img width, 3)
Expected to be in contigious row major layout.

@param bias: A constant value that is added to the result for each pixel after convolution is calculated.
@param dest_shape: The shape of the image in format (height, width)
@param kern_shape: The shape of the kernel in format (height, width)
*/
void convolve(unsigned char *img_padded, float *kern, unsigned char *dest, float bias, size_t *dest_shape, size_t *kern_shape)
{   
    // cache shapes 
    size_t height = dest_shape[0];
    size_t width = dest_shape[1];
    size_t kheight = kern_shape[0];
    size_t kwidth = kern_shape[1];

    // calculate strides based on shapes
    size_t s1 = COLOR_DEPTH * sizeof(unsigned char);
    size_t s0 = s1 * width;
    size_t ps0 = (width + kwidth - 1) * s1;

    size_t y, x, ky, kx, wy, pixel_offset, window_offset;
    float kval, r, g, b;

    // iterate every pixel of the padded image
    for (y = 0; y < height; y++)
    {
        for (x = 0; x < width; x++)
        {
            r = g = b = 0;
     
            // iterate every element of the kernel
            for (ky = 0; ky < kheight; ky++)
            {
                wy = (y + ky) * ps0;
                for (kx = 0; kx < kwidth; kx++)
                {
                    // get the kernel element. 
                    kval = kern[kwidth * ky + kx];

                    // multiple the kernel element by the pixel and add to accumulated values
                    window_offset = wy + (x+kx) * s1;
                    r += img_padded[window_offset] * kval;
                    g += img_padded[++window_offset] * kval;
                    b += img_padded[++window_offset] * kval;
                }
            }

            // set the pixel on the destination image. 
            pixel_offset = y * s0 + x * s1;
            dest[pixel_offset] = clamp(r + bias);
            dest[++pixel_offset] = clamp(g + bias);
            dest[++pixel_offset] = clamp(b + bias);
        }
    }
}