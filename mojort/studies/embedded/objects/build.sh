#!/bin/sh
set -e

mojo build mylib.mojo --emit object -o mylib.o
gcc -o main.o -c main.c
gcc *.o
