import numpy as np
from scipy.spatial import Delaunay
from utils import *
import cv2
import json 


COLOR_RED = (0, 0, 255)


def get_delaunay_from_points_dict(points_dict):
    marker_points = np.array(list(points_dict.values()))
    return (get_delaunay(marker_points))


def get_delaunay(points_array):
    tri = Delaunay(points_array)
    return (points_array[tri.simplices])



def run_delaunay(image_path, points_array):
    window_name = "Delaunay"

    # Setup image and spawn window
    image = cv2.imread(image_path)
    
    # Get triangle coordinates
    delaunay_triangles = get_delaunay(points_array)

    # Draw each triangle to image
    for triangle in delaunay_triangles:
        triangle.reshape((-1, 1, 2))
        cv2.polylines(image, [triangle], isClosed=True, color=COLOR_RED, thickness=1)
        cv2.imshow(window_name, image)

    cv2.waitKey(0)

