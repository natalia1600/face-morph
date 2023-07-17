from PIL import Image
import os

# Desired dimensions
out_w = 200
out_h = 200

images_dir = "./images"
directory = os.fsencode(images_dir)
cropped_dir = os.path.join(os.getcwd(), 'cropped')
if not os.path.isdir('cropped'):
    os.makedirs(cropped_dir)

def crop(filename):
    im = Image.open(os.path.join(images_dir, filename))
    img_w, img_h = im.size

    # Set points for cropping
    left = (img_w - out_w) / 2
    top = (img_h - out_h) / 2
    right = img_w - left
    bottom = img_h - top

    # Crop image
    cropped = im.crop((left, top, right, bottom))
    cropped.save('./cropped/' + filename)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    crop(filename)
 
