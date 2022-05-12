#include <stdio.h>
#include <string.h>

// The memory size of a single RGB pixel (composed of 3 unsigned chars for RGB)
const size_t PIXEL_SIZE = 3 * sizeof(unsigned char);

void affine_transform(unsigned char *img, size_t *img_shape, size_t *img_strides, float *inv_transform, unsigned char *dest, size_t *dest_shape, size_t *dest_strides)
{
    size_t img_height = img_shape[0];
    size_t img_width = img_shape[1];
    size_t s0 = img_strides[0];
    size_t s1 = img_strides[1];

    size_t dest_height = dest_shape[0];
    size_t dest_width = dest_shape[1];
    size_t ds0 = dest_strides[0];
    size_t ds1 = dest_strides[1];

    // x and y scale
    float a0 = inv_transform[0];
    float a1 = inv_transform[1];
    // x and y shear
    float b0 = inv_transform[3];
    float b1 = inv_transform[4];
    // x and y offset
    float c0 = inv_transform[2];
    float c1 = inv_transform[5];

    size_t x1, y1, x, y;

    // iterate each pixel in the destination image.
    for (y1 = 0; y1 < dest_height; y1++)
    {
        for (x1 = 0; x1 < dest_width; x1++)
        {
            // calculate the location of the source pixel by applying the inverse transformation matrix.
            // since x and y are integer types this will have the effect of simple rounding to the nearest neighbor.
            x = x1 * a0 + y1 * b0 + c0;
            y = x1 * a1 + y1 * b1 + c1;

            // skip any locations which fall outside of the source image. 
            if ((x < 0 || x >= img_width) || (y < 0 || y >= img_height))
            {
                continue;
            }

            // copy the source pixel to the destination pixel.
            memcpy(dest + ds0 * y1 + ds1 * x1, img + s0 * y + s1 * x, PIXEL_SIZE);
        }
    }
}