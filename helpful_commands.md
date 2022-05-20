gcc -fPIC -shared bpimage/*.c -o bpimage.so  && python3 bpimage/main.py ~/Pictures/baboon.png -b -d

kernprof -v -l  bpimage/main.py ~/Pictures/baboon.png -b -d