from point_data import *
from cv_constants import *
from scipy.spatial import Delaunay
import json

def get_point_label_list() -> list[str]:
    points = []
    points.extend([f"corner-{x}" for x in CORNERS])
    for side in ["L", "R"]:
        points.extend([f"eye-{side}-{x}" for x in EYE ])
        points.extend([f"eyebrow-{side}-{x}" for x in EYEBROW ])
    points.extend([f"mouth-{x}" for x in MOUTH ])
    points.extend([f"nose-{x}" for x in NOSE ])
    points.extend([f"head-{x}" for x in HEAD ])
    return points

def get_delaunay(points_array):
    tri = Delaunay(points_array)
    return points_array[tri.simplices]

point_labels = get_point_label_list()
