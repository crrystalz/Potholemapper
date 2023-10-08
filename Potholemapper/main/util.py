import os
import shutil
import sys
import time

def load_anim():
    blah = "..........."
    for l in blah:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(0.2)

def create_or_empty_directory(dir_path):
    # Check if the directory exists
    if os.path.exists(dir_path):
        # If it exists, remove the directory and its contents
        try:
            shutil.rmtree(dir_path)
            print(f"Directory {dir_path} and its contents have been removed")
        except Exception as e:
            print(f"Error removing directory {dir_path}: {e}")
    
    # Recreate the directory
    try:
        os.makedirs(dir_path)
        print(f"Directory {dir_path} has been created")
    except Exception as e:
        print(f"Error creating directory {dir_path}: {e}")