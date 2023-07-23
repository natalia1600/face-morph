import numpy as np
from scipy.spatial import Delaunay
from utils import *
import cv2
import json 


COLOR_RED = (0, 0, 255)


def get_delaunay_from_points_dict(points_dict):
    marker_points = np.array(list(points_dict.values()))
    return (get_delaunay(marker_points))


def get_delaunay(points_array: np.ndarray):
    tri = Delaunay(points_array)
    return points_array[tri.simplices]

# Draw each triangle to image
def draw_delaunay(image, delaunay_triangles):
    for triangle in delaunay_triangles:
        print("draw_delaunay tri:", triangle)
        triangle.reshape((-1, 1, 2))
        cv2.polylines(image, [triangle], isClosed=True, color=COLOR_RED, thickness=1)

    cv2.imshow("delaunay", image)

def run_delaunay(image_path, points_array):
    # Setup image and spawn window
    image = cv2.imread(image_path)
    
    # Get triangle coordinates
    delaunay_triangles = get_delaunay(points_array)
    draw_delaunay(image, delaunay_triangles)

    cv2.waitKey(0)

