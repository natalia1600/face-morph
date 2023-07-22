from frames import *
import json
import numpy as np
from frames import get_frame_points, get_delaunay_points
from delaunay import run_delaunay
import point_selector


points_dict = {}
image_paths = []

for name in IMAGE_NAMES:
    image_paths.append(os.path.join(IMAGE_DIR, f"{name}.jpg"))
    with open(os.path.join(DATA_DIR, f"{name}.json")) as json_file:
        points_dict[name] = json.load(json_file)

# Assume only 2 images for now
image1 = cv2.imread(image_paths[0])
image2 = cv2.imread(image_paths[1])

added_image = cv2.addWeighted(image1,0.4,image2,0.1,0)
cv2.imwrite('combined.png', added_image)
cv2.imshow('combined.png', added_image)
cv2.waitKey(0)



# iterator_image_names = iter(IMAGE_NAMES)

# for image_name in iterator_image_names:
#     next_image_name = next(iterator_image_names, None)  # Get the next image name or None if there are no more elements
#     if next_image_name is None:
#         break  # Stop the loop if there are no more images

#     dict_frames = get_frame_points(points_dict[image_name], points_dict[next_image_name])
#     frame_delaunay_sets = get_delaunay_points(dict_frames)


# for image_path in image_paths:
#     run_delaunay(image_path, )