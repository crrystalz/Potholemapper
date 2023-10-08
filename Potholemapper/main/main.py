import os
import sys
import time
import shutil
import colorama
import folium

from util import create_or_empty_directory
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

    for filename in os.listdir(geotagged_images_dir):
        f = os.path.join(geotagged_images_dir, filename)
        if os.path.isfile(f) and (
            filename.endswith(".png") or filename.endswith(".jpg")
        ):
            command = f"yolo task=detect mode=predict model={model_path} show=True conf=0.5 source={f} save_txt=True project={yolo_output_dir}"
            print(command)
            os.system(command)
            print(f"Succesfully processed: {filename}")

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
            # print(f"{folder} has no detected pothole(s)")

    return pothole_images


def main(
    dashcam_video_dir, gpx_filepath, model_path, working_dir, output_html_filepath
):
    geotagged_images_dir = geotag(dashcam_video_dir, working_dir, gpx_filepath)

    yolo_output_dir = os.path.join(working_dir, "yolo_output")
    pothole_images = _detect(
        geotagged_images_dir, yolo_output_dir, model_path
    )  # detect function (run yolo)

    map = folium.Map(location=[37.40, -122.13], zoom_start=15)

    for geotagged_image_filepath in pothole_images:
        print(geotagged_image_filepath)
        # image = Image.open(geotagged_image_filepath)
        dec_lat, dec_lon = find_lat_lon_of_image(geotagged_image_filepath)
        folium.Marker([dec_lat, dec_lon], popup="Point").add_to(map)

    map.save(output_html_filepath)

    # create_html(pothole_images)  # create html file with table of detected pothole image and gmaps location


model_path = "/home/saswat/pothole-data/yolov8x_tesladataset1.pt"
dashcam_video_dir = "/media/saswat/TESLADRIVE/TeslaCam/SavedClips"
working_dir = "raw_videos"
gpx_filepath = "/home/saswat/pothole-data/0923-third-attempt.gpx"

# main(dashcam_video_dir, gpx_filepath, model_path, working_dir, "results.html")
