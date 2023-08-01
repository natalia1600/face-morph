import os
import json

import cv2
import numpy as np
import time

from delaunay import delaunay_points_index_map, draw_delaunay, get_delaunay, get_delaunay_points_from_indices, get_interpolated_delaunay_tris, get_interpolated_marker_points
from constants import COLOR_LIME, DATA_DIR, IMAGE_DIR
from morph import compute_affine, bound_rect, bound_rect2
from utils import wait_space

import imageio


total_frames = 30


# maybe we should stick to dict since we need to map the
# triangles using the point labels?
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
john_image = cv2.imread(a_image_file)
paul_image = cv2.imread(b_image_file)

print("Getting tris...")
a_tri_array = get_delaunay(np.array(a_points_list))
a_tri_indices = delaunay_points_index_map(a_tri_array.tolist(), a_points_list)
b_tri_array = get_delaunay_points_from_indices(a_tri_indices, b_points_list)

print("Getting interpolated marker points...")
marker_points_list = get_interpolated_marker_points(a_points_list, b_points_list, total_frames)

print("Get all tris...")
tris = []
for points_list in marker_points_list:
    tris.append(get_delaunay_points_from_indices(a_tri_indices, points_list))


print("Warp tris from A to B...")


def morph_midway_face(a_tri_array, b_tri_array, src_image, dst_image):
    for (n, (a_tri, b_tri)) in enumerate(zip(a_tri_array, b_tri_array)):
        print("Morphing triangle:", n)
        src = src_image.copy()
        compute_affine(np.int64([a_tri]), src, np.int64([b_tri]), dst_image)


def morph_frames(src_image, tris):
    frames = []
    a_tris = tris[0]    

    for curr_frame in range(1, len(tris)):
        dst_image = np.zeros((1000, 1000, 3), dtype = np.uint8)
        b_tris = tris[curr_frame]
        
        for (n, (a_tri, b_tri)) in enumerate(zip(a_tris, b_tris)):
            print("Morphing triangle:", n)
            compute_affine(np.int64([a_tri]), src_image, 
                           np.int64([b_tri]), dst_image)
        
        frames.append(dst_image)
    return frames


john_frames = morph_frames(john_image, tris)
tris.reverse()
paul_frames = morph_frames(paul_image, tris)
paul_frames.reverse()

# for frame in john_frames:
#     cv2.imshow("frame", frame)
#     cv2.waitKey(0)

# for frame in paul_frames:
#     cv2.imshow("frame", frame)
#     cv2.waitKey(0)


overlayed_frames = []
for alpha, j_frame, p_frame in zip(
    np.linspace(1, 0, total_frames), john_frames, paul_frames):

    beta = (1.0 - alpha)
    dst = cv2.addWeighted(j_frame, alpha, p_frame, beta, 0.0)
    overlayed_frames.append(dst)

for frame in overlayed_frames:
    cv2.imshow("frame", frame)
    cv2.waitKey(0)

imageio.mimsave('./morph.gif', overlayed_frames)

# morph_midway_face(a_tri_array, b_tri_array, src_image)
