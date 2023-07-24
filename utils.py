from constants import *
import os
import json
from facial_markers import facial_marker_locations


def save_dict_to_json(data_dict, folder_name, file_name):
    folder_path = os.path.join(os.getcwd(), folder_name)

    # Create directory if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "w") as file:
        json.dump(data_dict, file)


def retrieve_json_data(folder_name, file_name):
    file_path = os.path.join(os.getcwd(), folder_name, file_name)

    with open(file_path, "r") as file:
        json_data = json.load(file)
        return json_data


point_labels = [
    f"{key}-{value}"
    for key, values in facial_marker_locations.items()
    for value in values
]


def draw_triangle(image, triangle, color):
    triangle.reshape((-1, 1, 2))
    cv2.polylines(image, [triangle], isClosed=True, color=color, thickness=1)


def wait_space():
    print("Press space to continue")
    while cv2.waitKey(0) != 32:
        continue


def preview(label, img):
    print("Previewing:", label)
    cv2.imshow(label, img)


def draw_box(img, box, color):
    start = (box[0], box[1])
    end = (box[2], box[3])
    cv2.rectangle(img, start, end, color, 2)
