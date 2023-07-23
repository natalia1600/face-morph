import os
import json

import cv2
import numpy as np

from delaunay import draw_delaunay, get_delaunay
from cv_constants import COLOR_LIME, DATA_DIR, IMAGE_DIR
from morph import compute_affine
from utils import wait_space

def load_points_list(filepath):
    with open(filepath) as json_file:
        points_dict = json.load(json_file)
        points_list = list(points_dict.values())
        return points_list

a_points_file = os.path.join(DATA_DIR, "john.json")
b_points_file = os.path.join(DATA_DIR, "paul.json")
a_image_file = os.path.join(IMAGE_DIR, "john.jpg")
b_image_file = os.path.join(IMAGE_DIR, "paul.jpg")

print("Loading point data...")
a_points_list = load_points_list(a_points_file)
b_points_list = load_points_list(b_points_file)

print("Loading images...")
image_a = cv2.imread(a_image_file)
image_b = cv2.imread(b_image_file)

print("Getting tris...")
a_tri_array = get_delaunay(np.array(a_points_list))
b_tri_array = get_delaunay(np.array(b_points_list))

print("Warp tris from A to B")

for (n, (a_tri, b_tri)) in enumerate(zip(a_tri_array, b_tri_array)):
    print("Morphing triangle:", n)
    output_image = compute_affine(np.int64([a_tri]), image_a, np.int64([b_tri]), image_a)
    cv2.imshow("modified", output_image)

    # Press space
    while cv2.waitKey(0) != 32:
        continue





