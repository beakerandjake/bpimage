#include <stdio.h>

void fn(float *img, ssize_t *strides, ssize_t *dims)
{
    ssize_t y,x,img_h,img_w,stride_0,stride_1;

    img_h = dims[0]; img_w = dims[1];
    stride_0 = strides[0] / sizeof(float);
    stride_1 = strides[1] / sizeof(float);

    printf("sizeof(*img): %zd\n", sizeof(img));
    printf("img shape: (%zd,%zd)\n", img_h, img_w);
    printf("strides: (%zd,%zd)\n", strides[0], strides[1]);
    printf("sizeof(float) = %zd\n", sizeof(float));
    printf("strides converted: (%zd,%zd)\n", stride_0, stride_1);

    for (y = 0; y < img_h; y++)
    {
        for (x = 0; x < img_w; x++)
        {
            printf("img:(%zd,%zd), byte offset = (%zd), value = %f\n",y,x,y*stride_0 + x*stride_1, img[y*stride_0 + x*stride_1]);
        }
    }
}