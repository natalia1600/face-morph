from cv_constants import *
from scipy.spatial import Delaunay
import os
import json
from facial_markers import facial_marker_locations


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
    
point_labels = [
    f"{key}-{value}" 
    for key, values in facial_marker_locations.items() 
    for value in values
]

