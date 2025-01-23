import os
from glob import glob

def return_most_recent_in_folder(folder):
    # git files in holding folder
    files = glob(f"{folder}*.png")

    if not files:
        return  f"No PNG images found in {folder}"

    # sort files by creation time
    files.sort(key=os.path.getctime, reverse=True)

    # get the path of the most recent PNG file and return it
    return files[0].replace(folder, '')