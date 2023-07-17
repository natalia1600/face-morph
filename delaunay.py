import numpy as np
from scipy.spatial import Delaunay
import cv2

COLOR_RED = (0, 0, 255)

class Delaunay:
    def __init__(self, image_path, points_dict):
        self.window_name = "Delaunay"
        self.points_array = np.array(points_dict.values())

        # Setup image and spawn window
        self.image = cv2.imread(image_path)
        
        # Get triangle coordinates
        self.delaunay_triangles = self.get_delaunay()
        self.show()


    def get_delaunay(self):
        tri = Delaunay(self.points_array)
        delaunay_triangles = self.points_array[tri.simplices]
        return delaunay_triangles


    def show(self):
        for triangle in self.delaunay_triangles:
            triangle.reshape((-1, 1, 2))
            cv2.polylines(self.image, [triangle], isClosed=True, color=COLOR_RED, thickness=1)
            cv2.imshow(self.window_name, self.image)