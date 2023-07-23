import os
import json

import cv2
import numpy as np

from delaunay import get_delaunay, draw_delaunay
from cv_constants import DATA_DIR, IMAGE_DIR
from morph import compute_affine

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

# cv2.imshow("image A", image_a)
# cv2.waitKey(0)
# cv2.imshow("image B", image_b)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# draw_delaunay(image_a, a_tri_array)
# cv2.waitKey(0)
# draw_delaunay(image_b, b_tri_array)
# cv2.waitKey(0)

print(a_tri_array)
print(b_tri_array)

for (n, (a_tri, b_tri)) in enumerate(zip(a_tri_array, b_tri_array)):
    print("morphing triangle a to triangle: ", n)
    output_image = compute_affine(np.float32([a_tri]), image_a, np.float32([b_tri]), image_b)
    cv2.imshow("img", output_image)
    cv2.waitKey(0)



