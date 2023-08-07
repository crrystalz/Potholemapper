# 🛣️ Potholemapper

## Features
- Automatically detects potholes from Tesla Dashcam using a custom-trained and tuned YOLOv8 deep learning model
- Given a ``.gpx`` file matching the Tesla Dashcam files, geotag the dashcam files and add location metadata to the video files.

## Product Goal
A website that allows anyone to upload Dashcam videos from their Tesla (eventually support for any dashcam) and then automatically detects potholes on the road using a custom-trained and tuned YOLOv8 deep learning model. Then given the corresponding ``.gpx`` file, the location of the detected potholes is found and then mapped allowing other users to see where potholes are in their routes. This database of known potholes and their locations can then be used by other organizations as well.

## Links
Using (https://github.com/crrystalz/tesla-dashcam-geotagger/tree/main)

Referred (https://gist.github.com/snakeye/fdc372dbf11370fe29eb)
