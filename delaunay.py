import cv2
import numpy as np
from scipy.spatial import Delaunay

from utils import *
from constants import COLOR_RED


def get_delaunay_from_points_dict(points_dict):
    marker_points = np.array(list(points_dict.values()))
    return get_delaunay(marker_points)


def get_delaunay(points_array: np.ndarray):
    tri = Delaunay(points_array, incremental=True)
    return points_array[tri.simplices]


def get_delaunay_points_from_indices(index_list, points_list):
    delaunay_points = []

    # Iterate over list of point indices where each entry is [a_i, b_i, c_i]
    for triangle_index_list in index_list:
        delaunay_point = []

        # Iterate over each index in index list for a triangle
        for index in triangle_index_list:
            point = points_list[index]
            delaunay_point.append(point)
        delaunay_points.append(delaunay_point)
    return np.array(delaunay_points)


def delaunay_points_index_map(delaunay_points_list, points_list):
    """
    Takes in delaunay triangle coordinates and corresponding
    key facial marker coordinates, returns dict = {delaunay_points_index_hash:delaunay_points}
    """

    delaunay_vertex_index_list = []

    for delaunay_points in delaunay_points_list:
        delaunay_point_index_list = []
        for delaunay_point in delaunay_points:
            # Create list of each delauny vertex points' index in a_points_list
            coord_index = points_list.index(delaunay_point)
            delaunay_point_index_list.append(coord_index)

        # Sort the 3 item list of indexes, convert to tuple
        # Get hash of sorted_delaunay_point_index_tuple, add to delaunay_points_map as key
        # with delaunay vertex point set as value
        delaunay_vertex_index_list.append(delaunay_point_index_list)
    return delaunay_vertex_index_list


# Draw each triangle to image
def draw_delaunay(image, delaunay_triangles):
    for triangle in delaunay_triangles:
        triangle.reshape((-1, 1, 2))
        triangle = np.int32(triangle)
        cv2.polylines(image, [triangle], isClosed=True, color=COLOR_RED, thickness=1)

    cv2.imshow("delaunay", image)


def run_delaunay(image_path, points_array):
    # Setup image and spawn window
    image = cv2.imread(image_path)

    # Get triangle coordinates
    delaunay_triangles = get_delaunay(points_array)
    draw_delaunay(image, delaunay_triangles)

    cv2.waitKey(0)
