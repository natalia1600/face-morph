import cv2
import os

DEBUG_MODE = False

TOTAL_FRAMES = 10

IMAGE_NAMES = ["john", "paul"]

IMAGE_DIR = os.path.join(os.getcwd(), 'cropped')
DATA_DIR = os.path.join(os.getcwd(), 'data')

FONT = cv2.FONT_HERSHEY_PLAIN
FONT_SCALE = 3

COLOR_RED = (0, 0, 255)
COLOR_TEAL = (255, 255, 0)
COLOR_LIME = (0, 255, 0)
THICKNESS = 5
