from frames import *
import numpy as np
from PIL import Image
import math
# weights_b = np.linspace(0, 1, TOTAL_FRAMES)

# print("weights_b:", weights_b)

# # Assume only 2 images for now
# for delaunay_set, weight_b in zip(delaunay_sets_int.values(), weights_b):
#     weight_a = 1 - weight_b
#     added_image = cv2.addWeighted(src_img, weight_a, fill_img, weight_b, 1)
    
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

def bound_rect(points):
    min_x = int(min([item[0] for x in points for item in x]))
    max_x = int(max([item[0] for x in points for item in x]))

    min_y = int(min([item[1] for y in points for item in y]))
    max_y = int(max([item[1] for y in points for item in y]))

    return (min_x, min_y, max_x, max_y)


def compute_affine(src_tri, src_img, dst_tri, fill_img):
    print("src_tri:", src_tri)
    print("dst_tri:", dst_tri)
    src_rect = bound_rect(src_tri)
    dst_rect = bound_rect(dst_tri)
    print("src_rect:", src_rect)
    print("dst_rect:", dst_rect)
    src_tri_cropped = []
    dst_tri_cropped = []
    for i in range(3):
        src_tri_cropped.append(((src_tri[0][i][0] - src_rect[0]), (src_tri[0][i][1] - src_rect[1])))
        dst_tri_cropped.append(((dst_tri[0][i][0] - dst_rect[0]), (dst_tri[0][i][1] - dst_rect[1])))
    
    print("src cropped:", src_tri_cropped)
    print("dst cropped:", dst_tri_cropped)

    # Crop input image
    print("src_img:", src_img.shape)
    print("src_rect:", src_rect)
    print("++++++++++++++++++++++")
    print(src_rect[1])
    print(src_rect[1] + src_rect[3])
    print("++++++++++++++++++++++")
    print("++++++++++++++++++++++")
    print(src_rect[0])
    print(src_rect[0] + src_rect[2])
    print("++++++++++++++++++++++")
    src_img_cropped = src_img[src_rect[1]:src_rect[1] + src_rect[3], src_rect[0]:src_rect[0] + src_rect[2]]
    print("src_img_cropped:", src_img_cropped.shape)
    cv2.imshow("src_img_cropped:", src_img_cropped.shape)
    cv2.waitKey(0)
    print("*****************************")

    # Given a pair of triangles, find the affine transform.
    warp_mat = cv2.getAffineTransform(np.float32(src_tri_cropped), np.float32(dst_tri_cropped))

    # Apply the Affine Transform just found to the src image
    dst_img_cropped = cv2.warpAffine(src_img_cropped, warp_mat, (dst_rect[2], dst_rect[3]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    print("src_img_cropped:", src_img_cropped.shape)
    cv2.imshow("dst_img_cropped", dst_img_cropped)
    cv2.waitKey(0)

    # Get mask by filling triangle
    print("dst_img_cropped:", dst_img_cropped.shape)
    mask = np.zeros((dst_rect[3], dst_rect[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(dst_tri_cropped), (1.0, 1.0, 1.0), 16, 0)
    print("dst_img_cropped: ", dst_img_cropped.shape)
    print("mask: ", mask.shape)
    dst_img_cropped = dst_img_cropped * mask
    print("*****************************")
    print("dst_img_cropped: ", dst_img_cropped.shape)
    cv2.imshow("dst cropped", dst_img_cropped)
    cv2.waitKey(0)
    print("*****************************")

    # Copy triangular region of the rectangular patch to the output image
    print("mask:", mask)
    tri_region = fill_img[dst_rect[1]:dst_rect[1]+dst_rect[3], dst_rect[0]:dst_rect[0]+dst_rect[2]] * ((1.0, 1.0, 1.0) - mask)
    fill_img[dst_rect[1]:dst_rect[1]+dst_rect[3], dst_rect[0]:dst_rect[0]+dst_rect[2]] = tri_region
    print("tri_region: ", tri_region)

    unknown = fill_img[dst_rect[1]:dst_rect[1]+dst_rect[3], dst_rect[0]:dst_rect[0]+dst_rect[2]] + dst_img_cropped
    fill_img[dst_rect[1]:dst_rect[1]+dst_rect[3], dst_rect[0]:dst_rect[0]+dst_rect[2]] = unknown
    print('tri_region: ', tri_region.shape)
    print("fill_img:", fill_img.shape)
    return fill_img



# morphed = compute_affine(a_tris, src_img, b_tris, fill_img)

# Assume only 2 images for now
#for delaunay_set in delaunay_sets_int.values():
# image_src = src_img
# for i in range(TOTAL_FRAMES - 1):
#     frame1_tri_pts = delaunay_sets_list[i]
#     frame2_tri_pts = delaunay_sets_list[i + 1]
#     for src_tri, dst_tri in zip(frame1_tri_pts, frame2_tri_pts):
#         output_image = compute_affine(np.float32([src_tri]), image_src, np.float32([dst_tri]), src_img)
#         image_src = src_img
#         src_img = output_image
#     cv2.imshow("Delaunay", output_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
