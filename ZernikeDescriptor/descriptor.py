import mahotas
import numpy as np
import argparse
import cPickle
import glob
import cv2


class ZernikeMoments:
    def __init__(self, radius):
        self.radius = radius

    def describe(self, image):
        # return the Zernike moments for the image
        return mahotas.features.zernike_moments(image, self.radius)


ap = argparse.ArgumentParser()
ap.add_argument("-s", "--images", required=True,
                help="Path where the images are stored")
ap.add_argument("-i", "--index", required=True,
                help="Path to where the index file will be stored")
args = vars(ap.parse_args())

# Radius 21 is optimal for testing
desc = ZernikeMoments(21)
index = {}

# loop over the images
for imagePath in glob.glob(args["images"] + "/*.jpeg"):
    # parse out the image name, then load the image and
    # convert it to grayscale
    scanned_object = imagePath[imagePath.rfind("/") + 1:].replace(".jpeg", "")
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # pad the image with extra white pixels to ensure the
    # edges of the object are not up against the borders
    # of the image
    image = cv2.copyMakeBorder(image, 15, 15, 15, 15,
                               cv2.BORDER_CONSTANT, value=255)

    # invert the image and threshold it
    thresh = cv2.bitwise_not(image)
    thresh[thresh > 0] = 255
