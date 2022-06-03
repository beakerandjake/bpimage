# bpimage
bpimage is a simple image editing library which can be used from the command line. Basic image transformations, color editing, and convolution filters are implemented.

Created mainly so I could explore numpy, image processing, cli development, and extending python with c. 

### Commands
 - [preview](#preview--p)
 - [dest](#dest--d)
 - [boxblur](#boxblur)
 - [brightness](#brightness)
 - [contrast](#contrast)
 - [emboss](#emboss)
 - [fliph](#fliph)
 - [flipv](#flipv)
 - [gaussian](#gaussian)
 - [invert](#invert)
 - [motionblur](#motionblur)
 - [outline](#outline)
 - [rgb2gray](#rgb2gray)
 - [rotate](#rotate)
 - [rotate90](#rotate90)
 - [saturation](#saturation)
 - [scale](#scale)
 - [sepia](#sepia)
 - [sharpen](#sharpen)
 - [shear](#shear)

## Dependencies
 - python (>= 3.10)
 - numpy (>= 1.22)
 - Pillow (>= 9.1.1)
    - used only for io tasks such as loading, saving and previewing images
    
## Installation

### From Source
bpimage depends on functions written in multiple c files. These files must be compiled into a shared library so they can be invoked from python.

#### Prerequisites 
You will need: 
 - A c compiler, such as gcc. 

**Linux**

```bash
# checkout project if you have not already.
git clone https://github.com/beakerandjake/bpimage.git
# change your pwd to the root of the project.
cd bpimage
# compile all source c files into a shared library.
gcc -fPIC -shared -O3 bpimage/*.c -o bpimage.so
```

This will create a bpimage.so file. This file will be loaded in python and used by the library to perform image manipulation. 

## CLI Usage 
First ensure that you have compiled the c files and that your pwd is the root of the project.
```bash
cd bpimage
```

You can print help by running the command without arguments, or with the --help option. 
```bash
python3 bpimage/main.py --help
```

The first argument expected is the source image file. Then you can specify zero one or more edits to apply to the image. Finally you need to specify an output. The output could either be saved to a new file or previewed. 

Here is an example which rotates an image 90 degrees, inverts the colors, then saves it to a new file. 

```bash
python3 bpimage/main.py ~/Pictures/example.png --rotate90 --invert -d ~/Pictures/output.png
```

## Commands

### preview (-p)
Creates a temporary file and opens the image with the systems default image viewer. Useful for testing commands and immediately seeing the result. Cannot be used with dest (-d).

```bash
python3 bpimage/main.py ~/Pictures/example.png --invert -p
```

### dest (-d)
Saves the image to the specified location. Cannot be used with preview (-p).

```bash
python3 bpimage/main.py ~/Pictures/example.png -d ~/Pictures/output.png
```


### boxblur
Blurs each pixel by averaging all surrounding pixels extending radius pixels in each direction.

#### Arguments:
  - radius (int): Number of pixels to take in each direction.

```bash
python3 bpimage/main.py ~/Pictures/example.png --boxblur 2 -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-boxblur](https://user-images.githubusercontent.com/1727349/171954263-f5b6c949-4f85-4807-841b-825555956620.jpg)

### brightness
Modifies the brightness of the image.

#### Arguments:
  - strength (float): The amount to brighten or darken the image. A value of 0.0 will result in a black image, 1.0 gives the original image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --brightness 1.5 -d ~/Pictures/output.png
```
![baboon-sm](https://user-images.githubusercontent.com/1727349/171954229-92ebc046-4b8e-4562-9bdd-f13d859934be.jpg)
![baboon-brightness](https://user-images.githubusercontent.com/1727349/171954234-03c00139-bfe3-4327-a50d-bc48cd937f85.jpg)

### contrast
Modifies the contrast of the image. 

#### Arguments:
  - strength (float): The amount to brighten or darken the image. A value of 0.0 will result in a gray image, 1.0 gives the original image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --contrast 1.8 -d ~/Pictures/output.png
```
![baboon-sm](https://user-images.githubusercontent.com/1727349/171954229-92ebc046-4b8e-4562-9bdd-f13d859934be.jpg)
![baboon-contrast](https://user-images.githubusercontent.com/1727349/171954237-72508fee-8deb-44ea-b463-c14da4661dd6.jpg)

### emboss
Applies an emboss effect to the image.

#### Arguments:
 - direction (str): One of the following supported values. 
    - 'u' Emboss from top to bottom   
    - 'd' Emboss from bottom to top
    - 'l' Emboss from left to right
    - 'r' Emboss from right to left
 - strength (float): The number of surrounding pixels to take in each direction.

```bash
python3 bpimage/main.py ~/Pictures/example.png --emboss r 1 -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-emboss](https://user-images.githubusercontent.com/1727349/171954267-bc741bcd-ce1d-4bcd-ad82-009434b0761c.jpg)

### fliph
Flips the image across the horizontal, from bottom to top.

```bash
python3 bpimage/main.py ~/Pictures/example.png --fliph -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-sm-fliph](https://user-images.githubusercontent.com/1727349/171756218-0e2cac16-8468-440f-8446-7304c5bdab58.png)

### flipv
Flips the image across the vertical, from left to right.

```bash
python3 bpimage/main.py ~/Pictures/example.png --flipv -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-sm-flipv](https://user-images.githubusercontent.com/1727349/171754207-5c7d5dff-aa2d-45ac-ad6c-8f0840f2da26.png)

### gaussian
Applies a gaussian blur to the image.

#### Arguments:
 - radius (int): The number of pixels to take in each direction.
 - sig (float): The sigma of the gaussian function. Higher values result in more blurring.

```bash
python3 bpimage/main.py ~/Pictures/example.png --gaussian 2 6.0 -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-gaussian](https://user-images.githubusercontent.com/1727349/171954275-a02b3816-71cb-459e-b8c5-2799d4f68976.jpg)

### invert
Create a negative of the image. 

```bash
python3 bpimage/main.py ~/Pictures/example.png --invert -d ~/Pictures/output.png
```
![baboon-sm](https://user-images.githubusercontent.com/1727349/171954229-92ebc046-4b8e-4562-9bdd-f13d859934be.jpg)
![baboon-invert](https://user-images.githubusercontent.com/1727349/171954245-63080d4b-965f-4d68-97d8-ca98f12fbad2.jpg)

### motionblur
Applies motion blur to the image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --motionblur -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-motionblur](https://user-images.githubusercontent.com/1727349/171954279-7c463749-27ee-478d-8da9-72819455e2a1.jpg)

### outline
Highlights edges of the image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --outline -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-outline](https://user-images.githubusercontent.com/1727349/171954287-220bf86f-ea1a-4983-9b58-11048d8fe055.jpg)

### rbg2gray
Converts an RGB image to a grayscale image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --rgb2gray -d ~/Pictures/output.png
```
![baboon-sm](https://user-images.githubusercontent.com/1727349/171954229-92ebc046-4b8e-4562-9bdd-f13d859934be.jpg)
![baboon-gray](https://user-images.githubusercontent.com/1727349/171954242-90c253bc-6847-4bd0-8e50-edfd705bf924.jpg)

### rotate
Rotates the image counter-clockwise by a specified angle around the center. Optionally expands the canvas size to hold the rotated image.

#### Arguments:
  - angle (float): The amount of degrees to rotate the image. 
  - expand (boolean): Should the canvas be expanded to hold the rotated image? 

#### Example:
```bash
python3 bpimage/main.py ~/Pictures/example.png --rotate 45 true -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-sm-rotate](https://user-images.githubusercontent.com/1727349/171946148-4ca79f9d-4585-474c-9fe6-33ad1bb43d87.png)

### rotate90
Rotates the image counter-clockwise 90 degrees around the center n times.

#### Arguments:
  - times (integer): Number of times to rotate the image.

#### Example:
```bash
python3 bpimage/main.py ~/Pictures/example.png --rotate90 3 -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-sm-rotate90](https://user-images.githubusercontent.com/1727349/171756768-e9015165-aa84-4ead-8ba4-bb4080906f41.png)

### saturation
Modify the color saturation of the image. 

#### Arguments:
  - strength (float): The amount to modify the saturation. A value of 0.0 will result in a black and white image, 1.0 gives the original image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --saturation 1.8 -d ~/Pictures/output.png
```
![baboon-sm](https://user-images.githubusercontent.com/1727349/171954229-92ebc046-4b8e-4562-9bdd-f13d859934be.jpg)
![baboon-saturation](https://user-images.githubusercontent.com/1727349/171954249-f5c4f409-16e3-4951-ac11-822911c70057.jpg)

### scale
Re-sizes the image uniformly based on a scale factor.

#### Arguments:
  - scale (float): Non-zero positive number multiplied by the width and height of the image to determine the dimensions of the resulting image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --scale .5 -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-sm-scale](https://user-images.githubusercontent.com/1727349/171946358-4720390a-b60b-459e-b0a7-9214833f443a.png)

### sepia
Applies a sepia tone to an RGB image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --sepia -d ~/Pictures/output.png
```
![baboon-sm](https://user-images.githubusercontent.com/1727349/171954229-92ebc046-4b8e-4562-9bdd-f13d859934be.jpg)
![baboon-sepia](https://user-images.githubusercontent.com/1727349/171954258-ac993cd7-43d7-4693-859a-8cd079dda49f.jpg)

### sharpen
Modify the color saturation of the image. 

#### Arguments:
  - strength (float): The amount to modify the saturation. A value of 0.0 will result in a black and white image, 1.0 gives the original image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --shear .25 0 true -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-sharpen](https://user-images.githubusercontent.com/1727349/171954293-47f1329f-46d9-4db1-9f37-10100cd9a6e5.jpg)

### shear
Shears the image in the specified dimension(s). Optionally expands the canvas size to hold the rotated image.

#### Arguments:
 - shear_x (float): The amount to shear the image in the x axis (0.0 does nothing)
 - shear_y (float): The amount to shear the image in the y axis (0.0 does nothing)
 - expand (bool): If true, expands the dimensions of resulting image so it's large enough to hold the entire skewed image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --shear .25 0 true -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
![boat-sm-shear](https://user-images.githubusercontent.com/1727349/171946655-2f3a2060-8232-4852-871d-12b066b487fa.png)
