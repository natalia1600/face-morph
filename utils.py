from cv_constants import *
from scipy.spatial import Delaunay
import os
import json

def get_delaunay(points_array):
    tri = Delaunay(points_array)
    return points_array[tri.simplices]


def save_dict_to_json(data_dict, folder_name, file_name):
    folder_path = os.path.join(os.getcwd(), folder_name)

    # Create directory if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_name)

    with open(file_path, 'w') as file:
        json.dump(data_dict, file)


def retrieve_json_data(folder_name, file_name):
    file_path = os.path.join(os.getcwd(), folder_name, file_name)

    with open(file_path, 'r') as file:
        json_data = json.load(file)
        return json_data
    

point_labels = []
point_labels_dict = retrieve_json_data('data', 'point_labels.json')
for key, values in point_labels_dict.items():
    for value in values:
        point_labels.append(f"{key}-{value}")

