#include <stdio.h>

void affine_transform(unsigned char *img, size_t *img_shape, size_t *img_strides, unsigned char *dest, size_t *dest_shape, size_t *dest_strides)
{
    size_t img_height = img_shape[0];
    size_t img_width = img_shape[1];
    size_t s0 = img_strides[0];
    size_t s1 = img_strides[1];

    size_t dest_height = dest_shape[0];
    size_t dest_width = dest_shape[1];
    size_t ds0 = dest_strides[0];
    size_t ds1 = dest_strides[1];

    size_t x,y;

    for (y = 0; y < img_height; y++)
    {
        for (x = 0; x < img_width; x++)
        {
            size_t xprime = x * 2;
            size_t yprime = y * 2;

            size_t dest_pixel = ds0 * yprime + ds1 * xprime;
            size_t src_pixel = s0 * y + s1 * x;
            dest[dest_pixel] = img[src_pixel];
            dest[dest_pixel+1] = img[src_pixel+1];
            dest[dest_pixel+2] = img[src_pixel+2];
        }
    }
}