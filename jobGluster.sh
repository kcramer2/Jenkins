#!/bin/bash

cp /mnt/gluster/chtc/submitTesting/test_open_terminal.mov ./
./ffmpeg -i test_open_terminal.mov -b:v 400k -s 640x360 gluster.mp4
rm test_open_terminal.mov
