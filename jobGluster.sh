#!/bin/bash

cp /mnt/gluster/chtc/test_open_terminal.mov ./
./ffmpeg -i test_open_terminal.mov -b:v 400k -s 640x360 test_open_terminal.mp4
rm test_open_terminal.mov
