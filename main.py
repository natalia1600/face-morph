import os
import json

import cv2
import numpy as np
import time

from delaunay import delaunay_points_index_map, draw_delaunay, get_delaunay, get_delaunay_points_from_indices
from cv_constants import COLOR_LIME, DATA_DIR, IMAGE_DIR
from morph import compute_affine
from utils import wait_space

# maybe we should stick to dict since we need to map the
# triangles using the point labels?
def load_points_list(filepath):
    with open(filepath) as json_file:
        points_dict = json.load(json_file)
        points_list = list(points_dict.values())
        return points_list

def load_points_dict(filepath):
    with open(filepath) as json_file:
        points_dict = json.load(json_file)
        return points_dict
    

a_points_file = os.path.join(DATA_DIR, "john.json")
b_points_file = os.path.join(DATA_DIR, "paul.json")
a_image_file = os.path.join(IMAGE_DIR, "john.jpg")
b_image_file = os.path.join(IMAGE_DIR, "paul.jpg")

print("Loading point data...")
a_points_list = load_points_list(a_points_file)
b_points_list = load_points_list(b_points_file)


print("Loading point dict...")
a_points_dict = load_points_dict(a_points_file)
b_points_dict = load_points_dict(b_points_file)

print("Loading images...")
image_a = cv2.imread(a_image_file)
image_b = cv2.imread(b_image_file)

print("Getting tris...")
a_tri_array = get_delaunay(np.array(a_points_list))
a_tri_indices = delaunay_points_index_map(a_tri_array.tolist(), a_points_list)
b_tri_array = get_delaunay_points_from_indices(a_tri_indices, b_points_list)

print(a_tri_array.shape)
print(b_tri_array.shape)
print(len(a_points_list))
print(len(b_points_list))
# exit(1)

print("Warp tris from A to B...")
src_image = image_a.copy()
dst_image = image_a.copy()

for (n, (a_tri, b_tri)) in enumerate(zip(a_tri_array, b_tri_array)):
    print("Morphing triangle:", n)
    src = src_image.copy()
    output_image = compute_affine(np.int64([a_tri]), src, np.int64([b_tri]), dst_image)

cv2.imshow("modified", dst_image)
cv2.waitKey(0)


