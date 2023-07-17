import cv2
import json
import sys
import os

from point_data import *

FONT = cv2.FONT_HERSHEY_PLAIN
FONT_SCALE = 1

COLOR_RED = (0, 0, 255)
COLOR_TEAL = (255, 255, 0)
COLOR_LIME = (0, 255, 0)
THICKNESS = 1

def get_point_label_list() -> list[str]:
    points = []
    for side in ["L", "R"]:
        points.extend([f"eye-{side}-{x}" for x in EYE ])
        points.extend([f"eyebrow-{side}-{x}" for x in EYEBROW ])
    points.extend([f"mouth-{x}" for x in MOUTH ])
    points.extend([f"nose-{x}" for x in NOSE ])
    points.extend([f"head-{x}" for x in HEAD ])
    return points

class PointSelector:
    def __init__(self, image_path: str, point_labels: dict):
        self.window_name = "Point Selector"

        # Setup state
        self.active_point = (0, 0)
        self.saved_points = {}
        self.active_label = ""
        self.point_labels = point_labels

        # Setup image and spawn window
        self.image_path = image_path
        self.original_image = cv2.imread(image_path)
        self.modified_image = self.original_image.copy()
        self.show()

        # Register callbacks
        cv2.setMouseCallback(self.window_name, self.handle_click)


    def __del__(self):
        print("PointSelector teardown") 
        cv2.destroyAllWindows()


    def reset(self):
        self.modified_image = self.original_image.copy()


    def show(self):
        print("redrawing frame")
        self.reset()
        self.draw_text("Press enter to continue", (5, 20))
        self.draw_text(self.active_label, (5, 60))
        self.draw_points()
        cv2.imshow(self.window_name, self.modified_image)


    def handle_click(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, ' ', y)
            self.active_point = (x, y)
            self.show()
    

    # Write text to the provided image
    def draw_text(self, text, org):
        cv2.putText(self.modified_image, text, org, FONT, FONT_SCALE, COLOR_RED, THICKNESS, cv2.LINE_AA, False)


    def draw_points(self):
        cv2.circle(self.modified_image, self.active_point, 2, COLOR_LIME, -1)

        for p in self.saved_points.values():
            self.modified_image = cv2.circle(self.modified_image, p, 2, COLOR_TEAL, -1)


    def set_active_label(self, label):
        self.active_label = label

    
    def save_points_to_json(self):
        file_name = os.path.splitext(self.image_path)[0]
        output_path = f"{file_name}.json"
        output_dict = {}

        # Convert tuples to arrays
        for (key, (x, y)) in self.saved_points.items():
            output_dict[key] = [x, y]

        with open(output_path, "w") as outfile:
            json.dump(output_dict, outfile)

    def run(self):
        for label in self.point_labels:
            # Draw text overlays
            self.set_active_label(label)
            self.show()

            # Await 'enter' keypress to lock in selected point
            cv2.waitKey(0)
            self.saved_points[self.active_label] = self.active_point

        print(self.saved_points)


# TODO: Get corners from image resolution

def run():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} IMAGE_FILEPATH")
        exit(1)

    image_path = sys.argv[1]
    point_labels = get_point_label_list()

    selector = PointSelector(image_path, point_labels)
    selector.run()
    selector.save_points_to_json()


# Start main 
run()