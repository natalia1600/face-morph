import numpy as np
from utils import *
import os

TOTAL_FRAMES = 10

def get_frames(midway_points):
    # dict_frames: {0: {label_a: [x_a, y_a], label_b: [x_b, y_b], ...}, ...}
    dict_frames = {}
    for n in range(TOTAL_FRAMES):
        dict_frames[n] = {}
        for label in midway_points:
            dict_frames[n][label] = midway_points[label][n]
    print(dict_frames)
    return dict_frames

def get_midway_points_by_label(points_dict_a, points_dict_b):
    midway_points = {}
    for coord_a, coord_b, label in zip(points_dict_a.values(), points_dict_b.values(), point_labels):
        midway_points[label] = midway_coords(coord_a, coord_b)
    midway_points = {k:v.tolist() for k,v in midway_points.items()}
    return midway_points

def midway_coords(coord_a, coord_b):
    x_a, y_a = coord_a
    x_b, y_b = coord_b

    x_values = list(np.linspace(x_a, x_b, TOTAL_FRAMES))
    y_values = list(np.linspace(y_a, y_b, TOTAL_FRAMES))
    
    # Combine x and y values
    new_coordinates = np.column_stack((x_values, y_values))
    return new_coordinates

def save_frames_to_json(dict_frames):
    with open('./data/frames.json', 'w') as fp:
        json.dump(dict_frames, fp)

midway_points = get_midway_points_by_label(points_dict['A'], points_dict['B'])
dict_frames = get_frames(midway_points)
save_frames_to_json(dict_frames)