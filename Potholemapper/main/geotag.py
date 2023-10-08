import os
import shutil
import subprocess
from colorama import Fore
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS
from util import create_or_empty_directory

'''
`dashcam_dir` is the Tesla's dashcam directory.

Recursively traverses the `dashcam_dir` and copies every file whose name ends with `-front.mp4` 
to `dashcam_dir`. All files are copied into `destination_dir` without creating
a folder structure that might exist inside `source_dir`.
'''
def _copy_dashcam_videos(dashcam_dir, destination_dir):
    # Validate that source_dir and destination_dir exist
    if not os.path.exists(dashcam_dir):
        raise ValueError(f"Source directory {dashcam_dir} does not exist")
    create_or_empty_directory(destination_dir)
    if not os.path.exists(destination_dir):
        raise ValueError(f"Destination directory {destination_dir} does not exist")
    
    # Walk through source_dir
    for foldername, _, filenames in os.walk(dashcam_dir):
        # Go through each file in the current folder
        for filename in filenames:
            # Check if the file ends with -front.mp4
            if filename.endswith('-front.mp4'):
                # Construct absolute path for source file
                source_file_path = os.path.join(foldername, filename)
                
                # Construct absolute path for destination file
                dest_file_path = os.path.join(destination_dir, filename)
                
                # Check if a file with the same name already exists in the destination directory
                if os.path.exists(dest_file_path):
                    print(f"File {dest_file_path} already exists. Skipping...")
                    continue
                
                # Copy file to destination_dir
                try:
                    shutil.copy2(source_file_path, dest_file_path)
                    print(f"File copied from {source_file_path} to {dest_file_path}")
                except Exception as e:
                    print(f"Error copying file from {source_file_path} to {dest_file_path}: {e}")

''' Extracts frames for videos and geotags them using the given GPX file.

It recursively finds all videos in the given directory (e.g., `/media/rrishi/TESLADRIVE`) 
whose names end with "-front.mp4". Only front video is used because the
model is trained on front videos. 

Mapilliary tools is used to extract frames from the selected videos and geotag them
using the given GPX file. It assumes Mapilliary tool is installed such that
it can be run on commandline by running `mapillary`. 

The geotagged images are stored in the given output directory.
'''
def _geotag_using_mapillary_tools(video_directory, gpx_filepath):
    subprocess.run(
        [
            "mapillary_tools",
            "video_process",
            video_directory,
            "--video_sample_interval",
            "0.5",
            "--geotag_source",
            "gpx",
            "--geotag_source_path",
            gpx_filepath,
            "--overwrite_all_EXIF_tags",
            "--offset_angle",
            "90", # front-camera
            "--device_make",
            "Tesla",
            "--video_sample_distance",
            "-1",
        ]
    )

'''
Extracts and returns the GPS location from the given image's EXIF data
as dictionary with keys "lat", "lon", "lat_ref", and "lon_ref".

Returns empty dictionary if the GPS location is not found.
'''
def _extract_exif_loc(image_filepath):  # returns image if
    image = Image.open(image_filepath)
    gps_coords = {}

    if image._getexif() == None:
        print(Fore.RED + "[+] ERR ->   {image_filepath} contains no exif data.")
    else:
        for tag, value in image._getexif().items():
            tag_name = TAGS.get(tag)
            if tag_name == "GPSInfo":
                for key, val in value.items():
                    if GPSTAGS.get(key) == "GPSLatitude":
                        gps_coords["lat"] = val

                    elif GPSTAGS.get(key) == "GPSLongitude":
                        gps_coords["lon"] = val

                    elif GPSTAGS.get(key) == "GPSLatitudeRef":
                        gps_coords["lat_ref"] = val

                    elif GPSTAGS.get(key) == "GPSLongitudeRef":
                        gps_coords["lon_ref"] = val

    return gps_coords

def _has_exif_loc(image_filepath):
    return len(_extract_exif_loc(image_filepath)) > 0

def _convert_deci(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees

def find_lat_lon_of_image(image_filepath):
    exif_loc = _extract_exif_loc(image_filepath)
    dec_lat = _convert_deci(
        float(exif_loc["lat"][0]),
        float(exif_loc["lat"][1]),
        float(exif_loc["lat"][2]),
        exif_loc["lat_ref"],
    )
    dec_lon = _convert_deci(
        float(exif_loc["lon"][0]),
        float(exif_loc["lon"][1]),
        float(exif_loc["lon"][2]),
        exif_loc["lon_ref"],
    )
    return dec_lat, dec_lon

'''
Recursively traverse the `mapillary_sampled_video_frames_dir` and copies every .jpg file that
has EXIF location data to `geotagged_frames_dir`. All files are copied into `geotagged_frames_dir` 
without creating a folder structure that exist inside `mapillary_sampled_video_frames_dir`.
'''
def _copy_geotagged_frames(mapillary_sampled_video_frames_dir, geotagged_frames_dir):
    # Validate that source_dir and destination_dir exist
    if not os.path.exists(mapillary_sampled_video_frames_dir):
        raise ValueError(f"Source directory {mapillary_sampled_video_frames_dir} does not exist")
    create_or_empty_directory(geotagged_frames_dir)
    if not os.path.exists(geotagged_frames_dir):
        raise ValueError(f"Destination directory {geotagged_frames_dir} does not exist")
    
    # Walk through source_dir
    for foldername, _, filenames in os.walk(mapillary_sampled_video_frames_dir):
        # Go through each file in the current folder
        for filename in filenames:
            # Check if the file ends with .jpg
            if filename.endswith('.jpg'):
                # Construct absolute path for source file
                source_file_path = os.path.join(foldername, filename)
                if not _has_exif_loc(source_file_path):
                    #print(Fore.RED + "[+] ERR ->   "+source_file_path + " contains no exif location data.")
                    continue
                
                # Construct absolute path for destination file
                dest_file_path = os.path.join(geotagged_frames_dir, filename)
                
                # Check if a file with the same name already exists in the destination directory
                if os.path.exists(dest_file_path):
                    print(f"File {dest_file_path} already exists. Skipping...")
                    continue
                
                # Copy file to destination_dir
                try:
                    shutil.copy2(source_file_path, dest_file_path)
                    print(f"File copied from {source_file_path} to {dest_file_path}")
                except Exception as e:
                    print(f"Error copying file from {source_file_path} to {dest_file_path}: {e}")

# Returns the directory containing geotagged frames as .jpg files
def geotag(dashcam_video_dir, working_dir, gpx_filepath):
    mapillary_sampled_video_frames = os.path.join(working_dir, 'mapillary_sampled_video_frames')
    geotagged_frames_dir = os.path.join(working_dir, 'geotagged_frames')

    _copy_dashcam_videos(dashcam_video_dir, working_dir)
    _geotag_using_mapillary_tools(working_dir, gpx_filepath)
    _copy_geotagged_frames(mapillary_sampled_video_frames, geotagged_frames_dir)
    return geotagged_frames_dir
