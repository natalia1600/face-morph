# Face morph 😃

Face morphing using [Delaunay Triangulation](https://en.wikipedia.org/wiki/Delaunay_triangulation) implemented in Python using OpenCV.


## Environment

The following can be used to setup your environment to run this project using [venv](https://docs.python.org/3/library/venv.html). See the linked venv documentation for the steps required by your system.

## Usage

## Installation

Python3 required.

Install dependencies by running:
~~~
pip install -r requirements.txt
~~~


## Usage

* To run this program, run:
~~~
python3 main.py
~~~

To use images to warp into each other, upload the photos to the images directory, and update the image path variables to the new file paths.
If this is the first time the program is being run with the selected images, a point selector will appear on the screen, and ask the user to click on the facial feature specified. Once it has gone through the list of facial features, the process will need to be repeated for the rest of the images. These markers are used to map one face to another in the warping process. 

