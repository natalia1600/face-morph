from frames import *
import json
import numpy as np
from frames import get_frame_points, get_delaunay_points
from delaunay import run_delaunay

def convert_floats_to_ints(input_dict):
    return {key: int(value) if isinstance(value, float) else value for key, value in input_dict.items()}

points_dict = {}
image_paths = []
delaunay_sets = retrieve_json_data('data', 'frame_delaunay_sets.json')
delaunay_sets_list = list(delaunay_sets.values())


for name in IMAGE_NAMES:
    image_paths.append(os.path.join(IMAGE_DIR, f"{name}.jpg"))
    with open(os.path.join(DATA_DIR, f"{name}.json")) as json_file:
        points_dict[name] = json.load(json_file)

image_a = cv2.imread(image_paths[0])
image_b = cv2.imread(image_paths[1])
weights_b = np.linspace(0, 1, TOTAL_FRAMES)

# # Assume only 2 images for now
# for delaunay_set, weight_b in zip(delaunay_sets_int.values(), weights_b):
#     weight_a = 1 - weight_b
#     added_image = cv2.addWeighted(image_a, weight_a, image_b, weight_b, 1)
    
#     # Draw each triangle to image
#     for triangle in delaunay_set:
#         # Convert floating-point coordinates to integers
#         triangle_int = [(int(x), int(y)) for x, y in triangle]
        
#         # Reshape the triangle as a NumPy array
#         triangle_array = np.array(triangle_int, np.int32).reshape((-1, 1, 2))
        
#         # Draw the triangle on the image
#         cv2.polylines(added_image, [triangle_array], isClosed=True, color=COLOR_RED, thickness=1)



#     cv2.imshow("Delaunay", added_image)
#     cv2.waitKey(0)


def compute_affine(tri1_pts, image_a, tri2_pts, image_b):
    r1 = cv2.boundingRect(tri1_pts)
    r2 = cv2.boundingRect(tri2_pts)
    tri1_cropped = []
    tri2_cropped = []
        
    for i in range(3):
        tri1_cropped.append(((tri1_pts[0][i][0] - r1[0]), (tri1_pts[0][i][1] - r1[1])))
        tri2_cropped.append(((tri2_pts[0][i][0] - r2[0]), (tri2_pts[0][i][1] - r2[1])))

    # Crop input image
    image_a_cropped = image_a[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]

    # Given a pair of triangles, find the affine transform.
    warp_mat = cv2.getAffineTransform( np.float32(tri1_cropped), np.float32(tri2_cropped) )

    # Apply the Affine Transform just found to the src image
    img2_cropped = cv2.warpAffine( image_a_cropped, warp_mat, (r2[2], r2[3]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    # Get mask by filling triangle
    mask = np.zeros((r2[3], r2[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tri2_cropped), (1.0, 1.0, 1.0), 16, 0)
    
    img2_cropped = img2_cropped * mask
        
    # Copy triangular region of the rectangular patch to the output image
    image_b[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = image_b[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ( (1.0, 1.0, 1.0) - mask )
    image_b[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = image_b[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2_cropped

    return image_b

# Assume only 2 images for now
#for delaunay_set in delaunay_sets_int.values():

for i in range(TOTAL_FRAMES - 1):
    frame1_tri_pts = delaunay_sets_list[i]
    frame2_tri_pts = delaunay_sets_list[i + 1]
    print(frame1_tri_pts)
    print('************')
    for tri1_pts, tri2_pts in zip(frame1_tri_pts, frame1_tri_pts):
        output_image = compute_affine(np.array(tri1_pts), image_a, np.array(tri2_pts), image_b)
        cv2.imshow("Delaunay", output_image)
        cv2.waitKey(0)