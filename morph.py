from frames import *
import numpy as np
from PIL import Image
import math

def bound_rect(points):
    min_x = int(min([item[0] for x in points for item in x]))
    max_x = int(max([item[0] for x in points for item in x]))
    min_y = int(min([item[1] for y in points for item in y]))
    max_y = int(max([item[1] for y in points for item in y]))
    return (min_x, min_y, max_x, max_y)

def compute_affine(src_tri, src_img, dst_tri, fill_img):
    debug_img = src_img.copy()

    print("src_tri:", src_tri)
    print("dst_tri:", dst_tri)

    # Create bounding boxes around src and dst tri
    src_rect = bound_rect(src_tri)
    dst_rect = bound_rect(dst_tri)
    print("src_rect:", src_rect)
    print("dst_rect:", dst_rect)

    # DEBUG: draw bbs and tris
    draw_box(debug_img, src_rect, COLOR_LIME)
    draw_box(debug_img, dst_rect, COLOR_TEAL)
    draw_triangle(debug_img, src_tri, COLOR_LIME)
    draw_triangle(debug_img, dst_tri, COLOR_TEAL)
    preview("debug", debug_img)
    wait_space()

    src_tri_cropped = []
    dst_tri_cropped = []
    for i in range(3):
        src_tri_cropped.append(((src_tri[0][i][0] - src_rect[0]), (src_tri[0][i][1] - src_rect[1])))
        dst_tri_cropped.append(((dst_tri[0][i][0] - dst_rect[0]), (dst_tri[0][i][1] - dst_rect[1])))
    print("src_tri_cropped:", src_tri_cropped)
    print("dst_tri_cropped:", dst_tri_cropped)

    # Crop input image
    src_img_cropped = src_img[src_rect[1]:src_rect[1] + src_rect[3], src_rect[0]:src_rect[0] + src_rect[2]]

    # Given a pair of triangles, find the affine transform.
    warp_mat = cv2.getAffineTransform(np.float32(src_tri_cropped), np.float32(dst_tri_cropped))

    # Apply the Affine Transform just found to the src image
    dst_img_cropped = cv2.warpAffine(src_img_cropped, warp_mat, (dst_rect[2], dst_rect[3]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    preview("dst cropped", debug_img)
    wait_space()

    # Get mask by filling triangle
    mask = 0 * np.ones((dst_rect[3], dst_rect[2], 3), dtype = src_img.dtype)
    cv2.fillConvexPoly(mask, np.int32(dst_tri_cropped), (255, 255, 255), 16, 0)
    preview("mask", mask)
    wait_space()

    # Apply mask to cropped dst
    cropped_dst_tri_fill = cv2.bitwise_and(dst_img_cropped, mask)
    preview("tri fill", cropped_dst_tri_fill)
    wait_space()

    # Get dst image minus the warped tri
    dst_region = fill_img[dst_rect[1]:dst_rect[1]+dst_rect[3], dst_rect[0]:dst_rect[0]+dst_rect[2]]
    mask_invert = cv2.bitwise_not(mask)
    cropped_dst_no_tri_fill = cv2.bitwise_and(dst_region, mask_invert) 
    preview("tri surrounding", cropped_dst_no_tri_fill)
    wait_space()

    # Fill in the output image (rect with only triangle filled)
    fill_img[dst_rect[1]:dst_rect[1]+dst_rect[3], dst_rect[0]:dst_rect[0]+dst_rect[2]] = cropped_dst_tri_fill
    preview("out + tri", fill_img)
    wait_space()

    # Add triangle surroundings to output image
    fill_img[dst_rect[1]:dst_rect[1]+dst_rect[3], dst_rect[0]:dst_rect[0]+dst_rect[2]] += cropped_dst_no_tri_fill 
    preview("done", fill_img)
    
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
