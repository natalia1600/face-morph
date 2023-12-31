import cv2
import json
import sys
import os
from utils import *
from facial_markers import corner_points


class PointSelector:
    """
    Create facial feature (x,y) marker-point datasets by manually clicking on an image.
    """

    def __init__(self, image_path: str, point_labels: dict):
        """
        Parameters
        ----------
        image_path : str
            The path to the image to select points from.
        point_labels: dict
            Set of labels to select points for.
        """

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
        self.draw_text("Press enter to continue", (10, 30))
        self.draw_text(self.active_label, (10, 70))
        self.draw_points()
        cv2.imshow(self.window_name, self.modified_image)

    def handle_click(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, " ", y)
            self.active_point = (x, y)
            self.show()

    # Write text to the provided image
    def draw_text(self, text, org):
        cv2.putText(
            self.modified_image,
            text,
            org,
            FONT,
            FONT_SCALE,
            COLOR_RED,
            THICKNESS,
            cv2.LINE_AA,
            False,
        )

    def draw_points(self):
        cv2.circle(self.modified_image, self.active_point, 6, COLOR_LIME, -1)

        for p in self.saved_points.values():
            self.modified_image = cv2.circle(self.modified_image, p, 6, COLOR_TEAL, -1)

    def set_active_label(self, label):
        self.active_label = label

    def save_points_to_json(self):
        file_name = os.path.splitext(os.path.basename(self.image_path))[0]
        output_path = os.path.join(DATA_DIR, f"{file_name}.json")
        key_markers = {}

        # Convert tuples to arrays
        for key, (x, y) in self.saved_points.items():
            key_markers[key] = [x, y]

        key_markers.update(corner_points)
        with open(output_path, "w") as outfile:
            json.dump(key_markers, outfile)

    def run(self):
        for label in self.point_labels:
            # Draw text overlays
            self.set_active_label(label)
            self.show()

            # Await 'space' keypress to lock in selected point
            wait_space()
            self.saved_points[self.active_label] = self.active_point

        print(self.saved_points)


def run_point_selector():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} IMAGE_FILEPATH")
        exit(1)

    image_path = sys.argv[1]
    selector = PointSelector(image_path, point_labels)
    selector.run()
    selector.save_points_to_json()


if __name__ == "__main__":
    run_point_selector()
