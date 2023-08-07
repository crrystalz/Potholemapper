import os
import sys
import shutil

from get_exif_data import get_labeled_exif, get_location

source_dir = f"../testing/images/"
output_dir = f"../testing/yolo_output/"

model_name = f"yolov8x_tesladataset1.pt"
model_path = f"../detection_model/{model_name}"


def print_exif_data(image):
    exif = get_labeled_exif(image)

    if exif is None:
        print("No EXIF data found")
    else:
        print("EXIF", exif)
        geo = get_location(exif)
        print("GEO", geo)


def detect(source_dir, output_dir, model_path):
    for filename in os.listdir(source_dir):
        f = os.path.join(source_dir, filename)
        if os.path.isfile(f) and (
            filename.endswith(".png") or filename.endswith(".jpg")
        ):
            command = f"yolo task=detect mode=predict model={model_path} show=True conf=0.5 source={f} save_txt=True project={output_dir}"
            print(command)
            os.system(command)
            print(f"Succesfully processed: {filename}")


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
            print(f"{folder} has a detected pothole(s)")
            for filename in os.listdir(os.path.join(output_dir, folder)):
                f = os.path.join(source_dir, filename)
                if os.path.isfile(f) and (filename.endswith(".png") or filename.endswith(".jpg")):
                    pothole_images.append(os.path.join(source_dir, filename))

        else:
            print(f"{folder} has no detected pothole(s)")

    return pothole_images

for root, dirs, files in os.walk(output_dir):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

detect(source_dir, output_dir, model_path)
pothole_images = find_pothole_frames(output_dir)
print()

print(pothole_images)

print()

for image_dir in pothole_images:
    print(image_dir)
    print_exif_data(image_dir)
