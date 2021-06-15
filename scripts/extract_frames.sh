#!/bin/bash

dirs=($(find . -type d))

for dir in "${dirs[@]:1}"; do
  echo "$dir"
  mkdir ${dir}/frames/
  for camera in {A..D}; do
    ffmpeg -i ${dir}/camera_${camera}.h264 ${dir}/frames/camera_${camera}_frame_%03d.jpeg
  done
done

