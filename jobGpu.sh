#!/bin/bash

hostname
date
nvidia-smi

nvcc jobGPU.cu -o jobGPU.cuda
./jobGPU.cuda
