import sys
import os

from PIL import Image


def crop_and_save(dir, filename, w, h):
    im = Image.open(os.path.join(dir, filename))
    img_w, img_h = im.size

    # Set points for cropping
    left = (img_w - w) / 2
    top = (img_h - h) / 2
    right = img_w - left
    bottom = img_h - top

    # Crop image
    cropped = im.crop((left, top, right, bottom))
    cropped.save(os.path.join("./cropped/", filename))


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} IMAGE_DIR WIDTH HEIGHT")
        exit(1)

    # Get args
    image_dir = sys.argv[1]
    out_w = int(sys.argv[2])
    out_h = int(sys.argv[3])

    # Create output dir
    directory = os.fsencode(image_dir)
    cropped_dir = os.path.join(os.getcwd(), "cropped")
    if not os.path.isdir("cropped"):
        os.makedirs(cropped_dir)

    # Crop all
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        crop_and_save(image_dir, filename, out_w, out_h)


if __name__ == "__main__":
    main()
