# bpimage
bpimage is a simple image editing library. 

Created mainly so I could explore numpy, image processing, cli development, and extending python with c. 

Basic image transformations, color editing, and convolution filters are implemented. These can be invoked from the cli or python. 

[Examples](#commands)

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

### flipv
Flips the image across the vertical, from left to right.

```bash
python3 bpimage/main.py ~/Pictures/example.png --flipv -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
:arrow_right:
![boat-sm-flipv](https://user-images.githubusercontent.com/1727349/171754207-5c7d5dff-aa2d-45ac-ad6c-8f0840f2da26.png)

### fliph
Flips the image across the horizontal, from bottom to top.

```bash
python3 bpimage/main.py ~/Pictures/example.png --fliph -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
:arrow_right:
![boat-sm-fliph](https://user-images.githubusercontent.com/1727349/171756218-0e2cac16-8468-440f-8446-7304c5bdab58.png)

### rotate90
Rotates the image counter-clockwise 90 degrees around the center n times.

```bash
python3 bpimage/main.py ~/Pictures/example.png --rotate90 3 -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
:arrow_right:
![boat-sm-rotate90](https://user-images.githubusercontent.com/1727349/171756768-e9015165-aa84-4ead-8ba4-bb4080906f41.png)

### rotate
Rotates the image counter-clockwise by a specified angle around the center. Optionally expands the canvas size to hold the rotated image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --rotate 45 true -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
:arrow_right:
![boat-sm-rotate](https://user-images.githubusercontent.com/1727349/171946148-4ca79f9d-4585-474c-9fe6-33ad1bb43d87.png)

### scale
Re-sizes the image uniformly based on a scale factor.

```bash
python3 bpimage/main.py ~/Pictures/example.png --scale .5 -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
:arrow_right:
![boat-sm-scale](https://user-images.githubusercontent.com/1727349/171946358-4720390a-b60b-459e-b0a7-9214833f443a.png)

### shear
Shears the image in the specified dimension(s). Optionally expands the canvas size to hold the rotated image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --shear .25 0 true -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
:arrow_right:
![boat-sm-shear](https://user-images.githubusercontent.com/1727349/171946655-2f3a2060-8232-4852-871d-12b066b487fa.png)
