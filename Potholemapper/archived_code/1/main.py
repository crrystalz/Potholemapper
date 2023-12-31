import os
import sys
import time
import shutil
import colorama
import folium

from colorama import Fore
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

from gmap_downloader import GoogleMapDownloader, GoogleMapsLayers

image_raw_dir = f"../testing/images_mapillary/"
image_geotagged_dir = f"../testing/images_proccessed/"

output_dir = f"../testing/yolo_output/"

model_name = f"yolov8x_tesladataset1.pt"
model_path = f"../detection_model/{model_name}"


def convert_deci(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees


def load_anim():
    blah = "..........."
    for l in blah:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(0.2)


def exif_loc_to_lat_lon(gps_coords):
    dec_lat = convert_deci(
        float(gps_coords["lat"][0]),
        float(gps_coords["lat"][1]),
        float(gps_coords["lat"][2]),
        gps_coords["lat_ref"],
    )
    dec_lon = convert_deci(
        float(gps_coords["lon"][0]),
        float(gps_coords["lon"][1]),
        float(gps_coords["lon"][2]),
        gps_coords["lon_ref"],
    )

    return dec_lat, dec_lon


def check_and_get_exif_loc(image):  # returns image if
    gps_coords = {}

    if image._getexif() == None:
        print(Fore.RED + "[+] ERR ->   {file} contains no exif data.")

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
            else:
                print(Fore.WHITE + f"{tag_name} - {value}")

        if gps_coords:
            return True, gps_coords

    return False, []


def gmaps(filename):
    print(image_geotagged_dir, filename)
    image_file = os.path.join(image_geotagged_dir, filename)
    image = Image.open(image_file)
    x, y = check_and_get_exif_loc(image)
    if x:
        gps_coords = y

        dec_lat, dec_lon = exif_loc_to_lat_lon(gps_coords)

        gmaps = f"https://maps.google.com/?q={dec_lat},{dec_lon}"
        
        print(Fore.RED + "\n" + gmaps + Fore.WHITE)
        return gmaps


def find_files_with_exif(image_raw_dir, image_geotagged_dir):
    print("Clearing out geotagged image directory...")
    for root, dirs, files in os.walk(image_geotagged_dir):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    print("Finished")
    print()
    print()

    print("Moving Files...")

    added = 0
    total = 0
    for filename in os.listdir(image_raw_dir):
        if filename[0] == ".":
            continue

        print(filename)

        file = os.path.join(image_raw_dir, filename)
        image = Image.open(file)

        print(Fore.CYAN + f"[+] Scrapping File - {file}")
        load_anim()
        print("\n")

        x, y = check_and_get_exif_loc(image)
        if x:
            gps_coords = y

            shutil.copy2(file, image_geotagged_dir)

            print(Fore.GREEN + f"[+] File {filename} has GPS data")
            print(Fore.RED + "\n" + gmaps(filename) + Fore.WHITE)

            added += 1

        else:
            print(Fore.RED + f"[-] File {filename} has no GPS data")
            print()

        total += 1

    print(f"Added {added} out of {total} files")
    print()
    print()


def detect(image_geotagged_dir, output_dir, model_path):
    print("Clearing out yolo output directory...")

    for root, dirs, files in os.walk(output_dir):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    print("Finished")
    print()
    print()

    for filename in os.listdir(image_geotagged_dir):
        f = os.path.join(image_geotagged_dir, filename)
        if os.path.isfile(f) and (
            filename.endswith(".png") or filename.endswith(".jpg")
        ):
            command = f"yolo task=detect mode=predict model={model_path} show=True conf=0.5 source={f} save_txt=True project={output_dir}"
            print(command)
            os.system(command)
            print(f"Succesfully processed: {filename}")

    print("Successfully processed all images")
    print()
    print()


def find_pothole_frames(output_dir):
    pothole_images = []

    for folder in os.listdir(output_dir):  # iterating through predict directories
        if folder == ".DS_Store":
            continue

        labels_dir = os.path.join(output_dir, folder, "labels")
        pothole = False
        for _ in os.listdir(labels_dir):
            pothole = True

        if pothole:
            # print(f"{folder} has a detected pothole(s)")
            for filename in os.listdir(os.path.join(output_dir, folder)):
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    pothole_images.append([os.path.join(output_dir, folder, filename), os.path.join(image_geotagged_dir, filename), filename]) #1 is annoted image dir, 2 is geotagged image dir, 3 is filename

        else:
            pass
            # print(f"{folder} has no detected pothole(s)")

    return pothole_images


def create_html(pothole_images):
    print("Creating HTML file...")

    html = open("/main_output/pothole_img_gmap_table.html", "w+")
    html.write("<html>\n")
    html.write("<body>\n")
    html.write("<table>\n")

    for [annotated_image_dir, geotagged_image_dir, filename] in pothole_images:
        gmaps_link = gmaps(filename)

        image = Image.open(geotagged_image_dir)
        x, y = check_and_get_exif_loc(image)
        if x:
            gps_coords = y
        
        dec_lat, dec_lon = exif_loc_to_lat_lon(gps_coords)

        print(dec_lat, dec_lon)

        gmd = GoogleMapDownloader(dec_lat, dec_lon, 22, GoogleMapsLayers.SATELLITE)

        print("The tile coorindates are {}".format(gmd.getXY()))

        try:
            # Get the high resolution image
            img = gmd.generateImage()
        except IOError:
            print("Could not generate the image - try adjusting the zoom level and checking your coordinates")
        else:
            # Save the image to disk
            img.save("high_resolution_image.png")
            print("The map has successfully been created")



        html.write("<tr>\n")
        html.write(
            f"<td><img src='{annotated_image_dir}' width='500' height='500'></td>\n"
        )
        html.write(
            f"<td><embed src='{img}' width='500' height='500'></td>\n"
        )
        html.write(
            f"<td><embed src='{gmaps_link}' width='500' height='500'></td>\n"
        )
        html.write("</tr>\n")

    html.write("</table>\n")
    html.write("</body>\n")
    html.write("</html>\n")
    html.close()

    print("Finished")
    print()
    print()

def main(image_raw_dir, image_geotagged_dir, output_dir, model_path):
    find_files_with_exif(image_raw_dir, image_geotagged_dir)  # find files in mapillary directory that have exif data nad move to processed directory

    detect(image_geotagged_dir, output_dir, model_path)  # detect function (run yolo)

    map = folium.Map(location = [37.40, -122.13], zoom_start = 15)

    pothole_images = find_pothole_frames(
        output_dir
    )  # get list of images that were detected to have potholes

    for annoted_image_dir, geotagged_image_dir, filename in pothole_images:
        print(filename)
        gmaps_link = gmaps(filename) # prints and returns gmaps link

        image = Image.open(geotagged_image_dir)
        x, y = check_and_get_exif_loc(image)
        if x:
            gps_coords = y
        
            dec_lat, dec_lon = exif_loc_to_lat_lon(gps_coords)

            folium.Marker([dec_lat, dec_lon], popup='Point').add_to(map)

    map.save("map.html")

    # create_html(pothole_images)  # create html file with table of detected pothole image and gmaps location

main(image_raw_dir, image_geotagged_dir, output_dir, model_path)