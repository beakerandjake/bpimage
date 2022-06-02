# bpimage
bpimage is a simple image editing library. 

Created mainly so I could explore numpy, image processing, cli development, and extending python with c. 

Basic image transformations, color editing, and convolution filters are implemented. These can be invoked from the cli or python. 

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