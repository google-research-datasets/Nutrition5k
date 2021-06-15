#!/bin/bash

dirs=($(find . -type d))
for dir in "${dirs[@]:1}"; do
  echo "$dir"
  mkdir ${dir}/frames_sampled$1/
  for camera in {A..D}; do
    ffmpeg -i ${dir}/camera_${camera}.h264 -vf "select=not(mod(n\,$1))" -vsync vfr ${dir}/frames_sampled$1/camera_${camera}_frame_%03d.jpeg
  done
done

