import numpy as np
from scipy.spatial import Delaunay
import cv2

COLOR_RED = (0, 0, 255)

def run_delaunay(image_path, points_dict):
    window_name = "Delaunay"
    points_array = np.array(list(points_dict.values()))

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

