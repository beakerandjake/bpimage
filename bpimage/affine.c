#include <stdio.h>

void affine_transform(unsigned char *img, size_t *img_shape, size_t *img_strides, float *transform, unsigned char *dest, size_t *dest_shape, size_t *dest_strides)
{
    size_t img_height = img_shape[0];
    size_t img_width = img_shape[1];
    size_t s0 = img_strides[0];
    size_t s1 = img_strides[1];

    size_t dest_height = dest_shape[0];
    size_t dest_width = dest_shape[1];
    size_t ds0 = dest_strides[0];
    size_t ds1 = dest_strides[1];

    float a0 = transform[0];
    float a1 = transform[1];
    float a2 = transform[2];
    float b0 = transform[3];
    float b1 = transform[4];
    float b2 = transform[5];
    float c0 = transform[6];
    float c1 = transform[7];
    float c2 = transform[8];

    printf("transform\n");
    printf("[%f,%f,%f]\n", a0, a1, a2);
    printf("[%f,%f,%f]\n", b0, b1, b2);
    printf("[%f,%f,%f]\n", c0, c1, c2);
    printf("5/2 = {%ld}\n", (size_t)(.5 * 5));

    float x1, y1;

    for (y1 = 0; y1 < dest_height; y1++)
    {
        for (x1 = 0; x1 < dest_width; x1++)
        {
            size_t x = x1 * a0 + y1 * b0 + c0;
            size_t y = x1 * a1 + y1 * b1 + c1;

            if ((x < 0 || x >= img_width) || (y < 0 || y >= img_height))
            {
                continue;
            }

            size_t dest_pixel = ds0 * y1 + ds1 * x1;
            size_t src_pixel = s0 * y + s1 * x;

            dest[dest_pixel] = img[src_pixel];
            dest[dest_pixel + 1] = img[src_pixel + 1];
            dest[dest_pixel + 2] = img[src_pixel + 2];
        }
    }
}