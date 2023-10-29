import os
import sys
import time
import shutil
import colorama

import folium
from folium import Popup

from util import create_or_empty_directory, image_to_data_url
from geotag import find_lat_lon_of_image, geotag

from colorama import Fore
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def _detect(geotagged_images_dir, yolo_output_dir, model_path):
    print("Clearing out yolo output directory...")
    create_or_empty_directory(yolo_output_dir)
    print("Finished")
    print()
    print()

    i = 0
    for filename in os.listdir(geotagged_images_dir):
        f = os.path.join(geotagged_images_dir, filename)
        if os.path.isfile(f) and (
            filename.endswith(".png") or filename.endswith(".jpg")
        ):
            command = f"yolo task=detect mode=predict model={model_path} show=True conf=0.5 source={f} save_txt=True project={yolo_output_dir}"
            print(command)
            os.system(command)
            print(f"Succesfully processed: {filename}")

        if i == 10:
            break

        i += 1

    print("Successfully processed all images")
    print()
    print()
    return _find_pothole_frames(geotagged_images_dir, yolo_output_dir)


def _find_pothole_frames(geotagged_images_dir, yolo_output_dir):
    pothole_images = []

    # Yolo creates a "predict directory" named `predict1`, `predict2`, etc.
    # for each image that we call Yolo to detect pothole.
    for folder in os.listdir(yolo_output_dir):  # iterating through predict directories
        if folder == ".DS_Store":
            continue

        labels_dir = os.path.join(yolo_output_dir, folder, "labels")
        pothole = False
        # if one or more potholes are detected, Yolo creates a text file inside
        # the `labels` directory with the bounding boxes around potholes in the image.
        for _ in os.listdir(labels_dir):
            pothole = True

        if pothole:
            print(f"{folder} has a detected pothole(s)")
            for filename in os.listdir(os.path.join(yolo_output_dir, folder)):
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    pothole_images.append(os.path.join(geotagged_images_dir, filename))
        else:
            pass
            print(f"{folder} has no detected pothole(s)")

    return pothole_images


def main(
    dashcam_video_dir, gpx_filepath, model_path, working_dir, output_html_filepath
):
    geotagged_images_dir = geotag(dashcam_video_dir, working_dir, gpx_filepath)

    yolo_output_dir = os.path.join(working_dir, "yolo_output")
    pothole_images = _detect(
        geotagged_images_dir, yolo_output_dir, model_path
    )  # detect function (run yolo)

    map_ = folium.Map(
        location=[37.40, -122.13], zoom_start=15
    )  # renamed to map_ to avoid shadowing the built-in map function

    for geotagged_image_filepath in pothole_images:
        print(geotagged_image_filepath)
        # image = Image.open(geotagged_image_filepath)
        dec_lat, dec_lon = find_lat_lon_of_image(geotagged_image_filepath)

        # Embed the image within the popup using HTML
        image_path = os.path.basename(geotagged_image_filepath)
        data_url = image_to_data_url(geotagged_image_filepath)
        popup_content = f'<img src="{data_url}" alt="Pothole Image" width="200px">'
        popup = Popup(popup_content, max_width=300)

        folium.Marker([dec_lat, dec_lon], popup=popup).add_to(map_)

    map_.save(output_html_filepath)


dashcam_video_dir = f"F:/TeslaCam/SavedClips"
gpx_filepath = (
    f"C:/Users/rrishi/Desktop/coding/Potholemapper/pothole-data/0923-third-attempt.gpx"
)
model_path = f"C:/Users/rrishi/Desktop/coding/Potholemapper/pothole-data/yolov8x_tesladataset1.pt"
working_dir = f"working_dir"
output_html_filepath = f"results.html"

main(dashcam_video_dir, gpx_filepath, model_path, working_dir, output_html_filepath)
