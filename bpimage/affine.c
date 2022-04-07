#include <stdio.h>

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

    float a0 = inv_transform[0];
    float a1 = inv_transform[1];
    float a2 = inv_transform[2];
    float b0 = inv_transform[3];
    float b1 = inv_transform[4];
    float b2 = inv_transform[5];
    float c0 = inv_transform[6];
    float c1 = inv_transform[7];

    size_t x1, y1, x, y, src_offset, dest_offset;

    for (y1 = 0; y1 < dest_height; y1++)
    {
        for (x1 = 0; x1 < dest_width; x1++)
        {
            x = x1 * a0 + y1 * b0 + c0;
            y = x1 * a1 + y1 * b1 + c1;

            if ((x < 0 || x >= img_width) || (y < 0 || y >= img_height))
            {
                continue;
            }

            dest_offset = ds0 * y1 + ds1 * x1;
            src_offset = s0 * y + s1 * x;

            dest[dest_offset] = img[src_offset];
            dest[++dest_offset] = img[++src_offset];
            dest[++dest_offset] = img[++src_offset];
        }
    }
}

    // printf("transform\n");
    // printf("[%f,%f,%f]\n", a0, a1, a2);
    // printf("[%f,%f,%f]\n", b0, b1, b2);
    // printf("[%f,%f,%f]\n", c0, c1, 0);
    // printf("5/2 = {%ld}\n", (size_t)(.5 * 5));

    // printf("img strides (%ld,%ld)", s0,s1);
    // printf("img shape (%ld,%ld)", img_height,img_width);
