#include <stdio.h>
#include <string.h>
#include "common.h"


void brighten(unsigned char *img, size_t *img_shape, size_t *img_strides, float amount, unsigned char *dest)
{
    // cache the source image dimensions and strides (we expect dest matches this)
    size_t img_height = img_shape[0];
    size_t img_width = img_shape[1];
    size_t s0 = img_strides[0];
    size_t s1 = img_strides[1];

    printf("img shape: (%ld,%ld)\n", img_height, img_width);
    printf("img strides: (%ld,%ld)\n", s0, s1);
    printf("amount: %f\n", amount);

    size_t y, x, pixel_offset;

    // iterate every pixel of the image
    for (y = 0; y < img_height; y++)
    {
        for (x = 0; x < img_width; x++)
        {
            // set the pixel on the destination image. 
            pixel_offset = y * s0 + x * s1;
            dest[pixel_offset] = clamp(img[pixel_offset] * amount);
            dest[pixel_offset] = clamp(img[++pixel_offset] * amount);
            dest[pixel_offset] = clamp(img[++pixel_offset] * amount);
        }
    }
}