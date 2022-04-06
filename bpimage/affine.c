#include <stdio.h>

void affine_transform(unsigned char *img, size_t *img_shape, size_t *img_strides)
{
    size_t img_height = img_shape[0];
    size_t img_width = img_shape[1];
    size_t s0 = img_strides[0];
    size_t s1 = img_strides[1];

    printf("img shape: (%ld, %ld)\n", img_height, img_width);
    printf("img strides: (%ld, %ld)\n", s0, s1);
}