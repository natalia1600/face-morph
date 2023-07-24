import numpy as np
from utils import *
from constants import *
from delaunay import get_delaunay_from_points_dict


def get_delaunay_points(dict_frames):
    """
    Computes the Delaunay points for each frame in a dictionary of frames,
    and saves to data directory to JSON.

    Args:
        dict_frames (dict): Dictionary of frames where the keys are frame
                            numbers and the values are dictionaries of key
                            points (points_dicts).

    Returns:
        dict: A dictionary of Delaunay point where the keys are frame numbers
              and values are Delaunay point sets.
    """
    frames_to_delaunay_points = {}

    for frame, points_dict in dict_frames.items():
        frames_to_delaunay_points[frame] = get_delaunay_from_points_dict(points_dict)
    formatted_frames_to_delaunay_points = {
        k: v.tolist() for k, v in frames_to_delaunay_points.items()
    }

    return formatted_frames_to_delaunay_points


def get_frame_points(points_dict_a, points_dict_b):
    """
    Computes the key points of each frame by interpolating between two sets
    of points. Saves resulting dictionary as json.

    Args:
        `points_dict_a` (dict): A dictionary of key points for the first image.\n
        `points_dict_b` (dict): A dictionary of key points for the second image.

    Returns:
        dict: A dictionary of frames where the keys are frame numbers and the
              values are dictionaries of interpolated points.
    """
    midway_points = get_midway_points_by_label(points_dict_a, points_dict_b)
    dict_frames = {
        n: {label: midway_points[label][n] for label in midway_points}
        for n in range(TOTAL_FRAMES)
    }

    # Save frames to a JSON file in the data folder named frame_points.json
    save_dict_to_json(dict_frames, "data", "frame_points.json")
    return dict_frames


def get_midway_points_by_label(points_dict_a, points_dict_b):
    """
    Computes the midway points between two sets of points for each label.

    Args:
        points_dict_a (dict): A dictionary of points for the first set.
        points_dict_b (dict): A dictionary of points for the second set.

    Returns:
        dict: A dictionary of midway points where the keys are point labels and
              the values are lists of coordinates.
    """
    midway_points = {}
    for coord_a, coord_b, label in zip(
        points_dict_a.values(), points_dict_b.values(), points_dict_a.keys()
    ):
        # Compute the midway coordinates for each label
        midway_points[label] = midway_coords(coord_a, coord_b)

    # Convert the dictionary values to lists of coordinates for
    # serialization to JSON
    midway_points = {k: v.tolist() for k, v in midway_points.items()}
    return midway_points


def midway_coords(coord_a, coord_b):
    """
    Computes the coordinates at each midway point between two sets of
    coordinates.

    Args:
        coord_a (list): Coordinates of the first point.
        coord_b (list): Coordinates of the second point.

    Returns:
        np.array: Array of coordinates at each midway point.
    """
    x_a, y_a = coord_a
    x_b, y_b = coord_b

    x_values = list(np.linspace(x_a, x_b, TOTAL_FRAMES))
    y_values = list(np.linspace(y_a, y_b, TOTAL_FRAMES))

    # Combine x and y values into array representing the coordinates
    new_coordinates = np.column_stack((x_values, y_values))
    return new_coordinates
