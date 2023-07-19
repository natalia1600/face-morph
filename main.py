from delaunay import run_delaunay, get_delaunay
import json
import numpy as np

IMAGE_NAMES = ["A", "B"]

IMAGE_DIR = "./cropped"
DATA_DIR = "./data"

points_dict = {}
for name in IMAGE_NAMES:
    image_path = f"./{IMAGE_DIR}/{name}.jpg"
    with open(f"./{DATA_DIR}/{name}.json") as json_file:
        points_dict[name] = json.load(json_file)