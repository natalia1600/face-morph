import cv2
import numpy as np
from scipy.spatial import Delaunay
from utils import *
from constants import COLOR_RED


def get_interpolated_delaunay_tris(a_tri_array, b_tri_array, num_frames):
    points = []
    for a_tri, b_tri in zip(a_tri_array, b_tri_array):
        points.append(np.linspace(a_tri, b_tri, num_frames))
    print("POINTS", points)
    points_reshaped = np.reshape(points, (10, -1, 3, 2))
    return points_reshaped


def get_interpolated_marker_points(a_points_list, b_points_list, num_frames):
    interpolated_marker_points = []
    for a_point, b_point in zip(a_points_list, b_points_list):
        x_values = list(np.linspace(a_point[0], b_point[0], num_frames))
        y_values = list(np.linspace(a_point[1], b_point[1], num_frames))
        # Combine x and y values into array representing the coordinates
        new_coordinates = np.column_stack((x_values, y_values))
        interpolated_marker_points.append(new_coordinates)
    interpolated_marker_point_array = np.array([[x[frame] 
                                                 for x in interpolated_marker_points] 
                                                 for frame in range(num_frames)])
    return interpolated_marker_point_array

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
