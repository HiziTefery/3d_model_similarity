import mahotas
import numpy as np
import argparse
import cPickle
import glob
import cv2
import os


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
desc = ZernikeMoments(250)
indexes = {}

# paths = glob('*/')
for dirPath in glob.glob(args["images"] + '*'):
    for imagePath in glob.glob(dirPath + "/*.jpeg"):
        # parse out the image name, then load the image and
        # convert it to grayscale
        scanned_object = imagePath[imagePath.rfind("/")].replace(".jpeg", "")
        image = cv2.imread(imagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.bitwise_not(image)
        thresh[thresh > 0] = 255

        # cv2.drawContours(out, [contours], -1, 255, -1)

        # out = np.zeros(image.shape, dtype="uint8")
        # (_, contours, _) = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
        #                                     cv2.CHAIN_APPROX_SIMPLE)
        # contours = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        # cv2.drawContours(out, [contours], -1, 255, -1)

        # (_, contours, _) = cv2.findContours(image.copy(), cv2.RETR_LIST,
        #                                     cv2.CHAIN_APPROX_SIMPLE)
        ret, thresh = cv2.threshold(image, 50, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        out = np.zeros_like(image)
        cv2.drawContours(out, contours, -1, 255, -1)
        moments = desc.describe(out)

        # cv2.imshow('image', image)
        # cv2.imshow('Output Contour', out)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        print indexes
        indexes[imagePath] = moments
f = open(args["index"], "w")
f.write(cPickle.dumps(indexes))
f.close()