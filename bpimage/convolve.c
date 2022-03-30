#include <stdio.h>

void fn(float *img, ssize_t *strides, ssize_t *dims)
{
    ssize_t y,x,z,img_h,img_w,stride_0,stride_1,stride_2;

    img_h = dims[0]; img_w = dims[1];
    stride_0 = strides[0] / sizeof(float);
    stride_1 = strides[1] / sizeof(float);
    stride_2 = strides[2] / sizeof(float);

    printf("sizeof(*img): %zd\n", sizeof(img));
    printf("img shape: (%zd,%zd)\n", img_h, img_w);
    printf("strides: (%zd,%zd,%zd)\n", strides[0], strides[1], strides[2]);
    printf("sizeof(float) = %zd\n", sizeof(float));
    printf("strides converted: (%zd,%zd)\n", stride_0, stride_1);

    for (y = 0; y < img_h; y++)
    {
        for (x = 0; x < img_w; x++)
        {
            float pixel[3];
            pixel[0] = img[y*stride_0 + x*stride_1 + 0*stride_2];
            pixel[1] = img[y*stride_0 + x*stride_1 + 1*stride_2];
            pixel[2] = img[y*stride_0 + x*stride_1 + 2*stride_2];
            printf("img:(%zd,%zd), elem offset = (%zd), pixel = (%f,%f,%f)\n",y,x,y*stride_0 + x*stride_1,pixel[0],pixel[1],pixel[2]);
        }
    }
}