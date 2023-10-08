# 🛣️ Potholemapper
## Table of Contents
- [🛣️ Potholemapper](#️-potholemapper)
  - [Table of Contents](#table-of-contents)
  - [Goal](#goal)
  - [Inference Flowchart](#inference-flowchart)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Running the Application](#running-the-application)
    - [User Interface](#user-interface)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
  - [Links](#links)

## Goal
A website that allows anyone to upload Dashcam videos from their Tesla (eventually support for any dashcam) and then automatically detects potholes on the road using a custom-trained and tuned YOLOv8 deep learning model. Then given the corresponding ``.gpx`` file, the location of the detected potholes is found and then mapped allowing other users to see where potholes are in their routes. This database of known potholes and their locations can then be used by other organizations as well.

## Inference Flowchart
![Inferrence](https://github.com/crrystalz/Potholemapper/assets/61859932/27f20f85-1415-42fe-9ee0-d6326c657365)

## Getting Started
### Prerequisites
Before you can use this project, you need to ensure the following prerequisites are met:

* Python
* Mapillary Tools
* YOLOv8 (or any YOLO model of your choice)
## Installation
1. Clone the repository to your local machine:
```bash
git clone https://github.com/crrystalz/Potholemapper.git
``````
2. Navigate to the project directory:
```bash
cd Potholemapper/Potholemapper
```
## Usage
### Running the Application
To run the application, you should start from the app.py file in ``Potholemapper/Potholemapper/main/app.py``. This file provides a graphical user interface (GUI) for selecting the input directories and files required for pothole detection.

```bash
python app.py
```
### User Interface
The user interface allows you to do the following:

1. Select the Tesla Dashcam directory where your dashcam videos are stored.
2. Select the GPX (GPS Exchange Format) file that corresponds to your dashcam videos.
3. Select the YOLO model file for pothole detection.
4. Click the "Analyze" button to start the analysis process.
## Project Structure
The project structure is organized as follows:

* **'app.py':** The main application file with the GUI for user interaction.
* **'util.py':** Utility functions for directory creation and loading animations.
* **'main.py':** The core logic for pothole detection, geotagging, and mapping.
* **'geotag.py':** Functions for geotagging dashcam videos and frames.
*  **'README.md':** This readme file.

## Contributing
Contributions to this project are welcome! If you have ideas for improvements, bug fixes, or new features, please open an issue or submit a pull request on the GitHub repository.

## Links
Using (https://github.com/crrystalz/tesla-dashcam-geotagger/tree/main)

Using (https://gitlab.com/-/snippets/2215069)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
