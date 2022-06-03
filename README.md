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

### gaussian
Apply a gaussian blur to the image.

```bash
python3 bpimage/main.py ~/Pictures/example.png --flipv -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
:arrow_right:
![boat-sm-flipv](https://user-images.githubusercontent.com/1727349/171754207-5c7d5dff-aa2d-45ac-ad6c-8f0840f2da26.png)




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

#### Arguments:
  - times (integer): Number of times to rotate the image.

#### Example:
```bash
python3 bpimage/main.py ~/Pictures/example.png --rotate90 3 -d ~/Pictures/output.png
```
![boat-sm](https://user-images.githubusercontent.com/1727349/171754143-f9c9e477-653f-483d-957b-02be975e20f9.png)
:arrow_right:
![boat-sm-rotate90](https://user-images.githubusercontent.com/1727349/171756768-e9015165-aa84-4ead-8ba4-bb4080906f41.png)

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

![baboon-sm](https://user-images.githubusercontent.com/1727349/171954229-92ebc046-4b8e-4562-9bdd-f13d859934be.jpg)
![baboon-brightness](https://user-images.githubusercontent.com/1727349/171954234-03c00139-bfe3-4327-a50d-bc48cd937f85.jpg)
![baboon-contrast](https://user-images.githubusercontent.com/1727349/171954237-72508fee-8deb-44ea-b463-c14da4661dd6.jpg)
![baboon-gray](https://user-images.githubusercontent.com/1727349/171954242-90c253bc-6847-4bd0-8e50-edfd705bf924.jpg)
![baboon-invert](https://user-images.githubusercontent.com/1727349/171954245-63080d4b-965f-4d68-97d8-ca98f12fbad2.jpg)
![baboon-saturation](https://user-images.githubusercontent.com/1727349/171954249-f5c4f409-16e3-4951-ac11-822911c70057.jpg)
![baboon-sepia](https://user-images.githubusercontent.com/1727349/171954258-ac993cd7-43d7-4693-859a-8cd079dda49f.jpg)
![boat-boxblur](https://user-images.githubusercontent.com/1727349/171954263-f5b6c949-4f85-4807-841b-825555956620.jpg)
![boat-emboss](https://user-images.githubusercontent.com/1727349/171954267-bc741bcd-ce1d-4bcd-ad82-009434b0761c.jpg)
![boat-gaussian](https://user-images.githubusercontent.com/1727349/171954275-a02b3816-71cb-459e-b8c5-2799d4f68976.jpg)
![boat-motionblur](https://user-images.githubusercontent.com/1727349/171954279-7c463749-27ee-478d-8da9-72819455e2a1.jpg)
![boat-outline](https://user-images.githubusercontent.com/1727349/171954287-220bf86f-ea1a-4983-9b58-11048d8fe055.jpg)
![boat-sharpen](https://user-images.githubusercontent.com/1727349/171954293-47f1329f-46d9-4db1-9f37-10100cd9a6e5.jpg)
