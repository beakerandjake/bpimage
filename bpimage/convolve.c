#include <stdio.h>

// Expect image arrays have shape (y,x,3), of type float, in contigious c layout.

#define COLOR_DEPTH 3

void fn(float *img, size_t *img_strides, size_t *img_size, float *kern, size_t *kern_strides, size_t *kern_size)
{
    size_t height = img_size[0];
    size_t width = img_size[1];
    // convert strides from byte steps to "pointer increments"
    size_t s0 = img_strides[0] / sizeof(float);
    size_t s1 = img_strides[1] / sizeof(float);
    size_t s2 = img_strides[2] / sizeof(float);

    printf("img shape: (%zd,%zd)\n", height, width);
    printf("strides raw: (%zd,%zd,%zd)\n", img_strides[0], img_strides[1], img_strides[2]);
    printf("strides: (%zd,%zd,%zd)\n", s0, s1, s2);

    size_t kern_height = kern_size[0];
    size_t kern_width = kern_size[1];
    size_t ks0 = kern_strides[0] / sizeof(float);
    size_t ks1 = kern_strides[1] / sizeof(float);

    printf("kern shape: (%zd,%zd)\n", kern_height, kern_width);
    printf("kern strides raw: (%zd,%zd,%zd)\n", kern_strides[0], kern_strides[1], kern_strides[2]);
    printf("kern strides: (%zd,%zd)\n", ks0, ks1);


    // // zero out red and green

    // ssize_t row_offset,pixel_offset;

    // for (y = 0; y < img_h; y++)
    // {
    //     row_offset = y*stride_0;

    //     for (x = 0; x < img_w; x++)
    //     {
    //         pixel_offset = row_offset + x*stride_1;
    //         img[pixel_offset] = 0.0;
    //         img[++pixel_offset] = 0.0;
    //         // printf("img:(%zd,%zd), elem offset = (%zd)\n",y,x,y*stride_0 + x*stride_1);
    //     }
    // }
}