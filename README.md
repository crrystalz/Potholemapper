# 🛣️ Potholemapper

## Features
- Automatically detects potholes from Tesla Dashcam using a custom-trained and tuned YOLOv8 deep learning model
- Given a ``.gpx`` file matching the Tesla Dashcam files, geotag the dashcam files and add location metadata to the video files.

## Inference Flowchart
![Inferrence](https://github.com/crrystalz/Potholemapper/assets/61859932/27f20f85-1415-42fe-9ee0-d6326c657365)

## Goal
A website that allows anyone to upload Dashcam videos from their Tesla (eventually support for any dashcam) and then automatically detects potholes on the road using a custom-trained and tuned YOLOv8 deep learning model. Then given the corresponding ``.gpx`` file, the location of the detected potholes is found and then mapped allowing other users to see where potholes are in their routes. This database of known potholes and their locations can then be used by other organizations as well.

## Links
Using (https://github.com/crrystalz/tesla-dashcam-geotagger/tree/main)

Using (https://gitlab.com/-/snippets/2215069)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
