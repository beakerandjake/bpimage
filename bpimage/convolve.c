#include <stdio.h>

size_t clamp(ssize_t value, ssize_t max);

// Expect image arrays have shape (y,x,3), of type float, in contigious c layout.

void fn(float *img, size_t *img_strides, size_t *img_size, float *kern, size_t *kern_strides, size_t *kern_size, float *dest)
{
    size_t height, width, s0, s1, s2;
    height = img_size[0];
    width = img_size[1];
    // convert imgage strides from byte steps to pointer increments
    s0 = img_strides[0] / sizeof(float);
    s1 = img_strides[1] / sizeof(float);
    s2 = img_strides[2] / sizeof(float);

    size_t kern_rad, kern_height, kern_width, ks0, ks1;
    kern_height = kern_size[0];
    kern_width = kern_size[1];
    kern_rad = kern_height / 2;
    // convert kernel strides from byte steps to pointer increments.
    ks0 = kern_strides[0] / sizeof(float);
    ks1 = kern_strides[1] / sizeof(float);

    printf("img shape: (%zd,%zd)\n", height, width);
    printf("strides raw: (%zd,%zd,%zd)\n", img_strides[0], img_strides[1], img_strides[2]);
    printf("strides: (%zd,%zd,%zd)\n", s0, s1, s2);

    printf("kern shape: (%zd,%zd)\n", kern_height, kern_width);
    printf("kern rad: (%zd)\n", kern_rad);
    printf("kern strides raw: (%zd,%zd,%zd)\n", kern_strides[0], kern_strides[1], kern_strides[2]);
    printf("kern strides: (%zd,%zd)\n", ks0, ks1);

    size_t y, x, ky, kx, wx, wy, pixel_offset, window_offset;
    float kval, r, g, b;

    // iterate every pixel of the image
    for (y = 0; y < height; y++)
    {
        for (x = 0; x < width; x++)
        {
            r = g = b = 0;
            pixel_offset = y * s0 + x * s1;

            // iterate every cell of the kernel
            for (ky = 0; ky < kern_height; ky++)
            {
                for (kx = 0; kx < kern_width; kx++)
                {
                    kval = kern[ks0 * ky + ks1 * kx];
                    // get the index of the pixel which corresponds to current kernel
                    wy = clamp(y + ky - kern_rad, height - 1);
                    wx = clamp(x + kx - kern_rad, width - 1);
                    window_offset = wy * s0 + wx * s1;

                    r += img[window_offset] * kval;
                    g += img[window_offset + 1] * kval;
                    b += img[window_offset + 2] * kval;
                    // printf("img:(%zd,%zd) -> kern: (%zd,%zd) = (%f) -> offset: (%zd,%zd) -> translated: (%zd,%zd)\n", y, x, ky, kx, kval, ky - kern_rad, kx - kern_rad, wy, wx);
                    // printf("img:(%zd,%zd) -> kern: (%zd,%zd) = (%f) -> translated: (%zd,%zd) = (%f,%f,%f)\n", y, x, ky, kx, kval, wy, wx, r, g, b);
                }
            }

            dest[pixel_offset] = clamp(r, 255);
            dest[pixel_offset+1] = clamp(g, 255);
            dest[pixel_offset+2] = clamp(b, 255);
        }
    }
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

// Clamps a value between zero and max
size_t clamp(ssize_t value, ssize_t max)
{
    const size_t ret = value < 0 ? 0 : value;
    return ret > max ? max : ret;
}