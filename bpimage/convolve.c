#include <stdio.h>

#define COLOR_DEPTH 3

float clamp(float value);

// Expect image arrays have shape (y,x,3), of type float, in contigious c layout.

void convolve(unsigned char *img, size_t *img_size, float *kern, size_t *kern_size, float bias, unsigned char *dest)
{
    size_t height, width, s0, s1;
    height = img_size[0];
    width = img_size[1];
    // calculate image strides based on image dimensions
    s1 = COLOR_DEPTH * sizeof(unsigned char);
    s0 = s1 * width;
    
    size_t kern_rad, kern_height, kern_width, ks0, ks1;
    kern_height = kern_size[0];
    kern_width = kern_size[1];
    kern_rad = (kern_height - 1) / 2;
    // convert kernel strides from byte steps to pointer increments.
    ks1 = 1;
    ks0 = kern_width * 1;

    printf("kern shape: (%zd,%zd)\n", kern_height, kern_width);
    printf("kern rad: (%zd)\n", kern_rad);
    printf("kern strides: (%zd,%zd)\n", ks0, ks1);
    printf("sizeof(float): (%zd)\n", sizeof(float));

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
                wy = y + ky - kern_rad;
                
                for (kx = 0; kx < kern_width; kx++)
                {
                    kval = kern[ks0 * ky + ks1 * kx];
                    wx = x + kx - kern_rad;

                    if ((wy >= 0 && wy < height) && (wx >= 0 && wx < width))
                    {
                        window_offset = wy * s0 + wx * s1;
                        r += img[window_offset] * kval;
                        g += img[window_offset + 1] * kval;
                        b += img[window_offset + 2] * kval;
                    }
                }
            }

            dest[pixel_offset] = clamp(r + bias);
            dest[pixel_offset + 1] = clamp(g + bias);
            dest[pixel_offset + 2] = clamp(b + bias);
        }
    }
}

// Clamps a value between zero and 255
float clamp(float value)
{
    const float ret = value < 0 ? 0 : value;
    return ret > 255 ? 255 : ret;
}

// printf("img shape: (%zd,%zd)\n", height, width);
// printf("strides raw: (%zd,%zd,%zd)\n", img_strides[0], img_strides[1], img_strides[2]);
// printf("strides: (%zd,%zd,%zd)\n", s0, s1, s2);

// printf("kern shape: (%zd,%zd)\n", kern_height, kern_width);
// printf("kern rad: (%zd)\n", kern_rad);
// printf("kern strides raw: (%zd,%zd,%zd)\n", kern_strides[0], kern_strides[1], kern_strides[2]);
// printf("kern strides: (%zd,%zd)\n", ks0, ks1);