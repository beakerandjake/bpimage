#include <stdio.h>
#include <string.h>

// The memory size of a single RGB pixel (composed of 3 unsigned chars for RGB)
const size_t PIXEL_SIZE = 3 * sizeof(unsigned char);

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
void affine_transform(unsigned char *img, size_t *img_shape, size_t *img_strides, float *inv_transform, unsigned char *dest, size_t *dest_shape, size_t *dest_strides)
{
    // cache the source image dimensions and strides
    size_t img_height = img_shape[0];
    size_t img_width = img_shape[1];
    size_t s0 = img_strides[0];
    size_t s1 = img_strides[1];

    // cache the destination image dimensions and strides
    size_t dest_height = dest_shape[0];
    size_t dest_width = dest_shape[1];
    size_t ds0 = dest_strides[0];
    size_t ds1 = dest_strides[1];

    // x and y scale
    float sx = inv_transform[0];
    float sy = inv_transform[4];
    // x and y shear
    float shx = inv_transform[1];
    float shy = inv_transform[3];
    // x and y offset
    float tx = inv_transform[2];
    float ty = inv_transform[5];

    size_t x1, y1, x, y;

    // iterate each pixel in the destination image.
    for (y1 = 0; y1 < dest_height; y1++)
    {
        for (x1 = 0; x1 < dest_width; x1++)
        {
            // calculate the location of the source pixel by applying the inverse transformation matrix.
            // since x and y are integer types this will have the effect of simple rounding to the nearest neighbor.
            x = x1 * sx + y1 * shx + tx;
            y = x1 * shy + y1 * sy + ty;

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