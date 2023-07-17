from delaunay import run_delaunay
import json

IMAGE_NAMES = ["A", "B"]

IMAGE_DIR = "./cropped"
DATA_DIR = "./data"

for name in IMAGE_NAMES:
    image_path = f"./{IMAGE_DIR}/{name}.jpg"

    points_dict = {}
    with open(f"./{DATA_DIR}/{name}.json") as json_file:
        points_dict = json.load(json_file)

    run_delaunay(image_path, points_dict)

