from frames import *
import json
import numpy as np
from frames import get_frame_points, get_delaunay

points_dict = {}

for name in IMAGE_NAMES:
    image_path = f"./{IMAGE_DIR}/{name}.jpg"
    with open(f"./{DATA_DIR}/{name}.json") as json_file:
        points_dict[name] = json.load(json_file)

get_frame_points(points_dict['A'], points_dict['B'])
