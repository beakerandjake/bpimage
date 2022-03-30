#include <stdio.h>

void fn(float *img, ssize_t *strides, ssize_t *dims)
{
    ssize_t y,x,img_h,img_w,stride_0,stride_1,stride_2;

    img_h = dims[0]; img_w = dims[1];
    stride_0 = strides[0] / sizeof(float);
    stride_1 = strides[1] / sizeof(float);
    stride_2 = strides[2] / sizeof(float);

    // printf("sizeof(*img): %zd\n", sizeof(img));
    // printf("img shape: (%zd,%zd)\n", img_h, img_w);
    // printf("strides: (%zd,%zd,%zd)\n", strides[0], strides[1], strides[2]);
    // printf("sizeof(float) = %zd\n", sizeof(float));
    // printf("strides converted: (%zd,%zd,%zd)\n", stride_0, stride_1, stride_2);

    // zero out red and green

    ssize_t row_offset,pixel_offset;

    for (y = 0; y < img_h; y++)
    {
        row_offset = y*stride_0;

        for (x = 0; x < img_w; x++)
        {
            pixel_offset = row_offset + x*stride_1;
            img[pixel_offset] = 0.0;
            img[pixel_offset + 1] = 0.0;
            // printf("img:(%zd,%zd), elem offset = (%zd)\n",y,x,y*stride_0 + x*stride_1);
        }
    }
}