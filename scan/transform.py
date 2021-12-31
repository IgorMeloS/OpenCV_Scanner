# =============================================================================
# Image transform with OpenCV
# This module takes care about image transformatios, as rotation for example
# =============================================================================

# Importing Libraries

import cv2 as cv
import numpy as np

def pairs_points(pts):
    """Pairs points function.
    This function returns an array (4,2) containing the points coordinates from a select rectangle
    Arg:
        pts: list of points in array format
    return (top left, top right, bottom left, bottom right)
    """
    rect = np.zeros((4,2), dtype='float32')

    # To ensure the good order of point we take the min and max values from the pts
    # We consider that the top left has the minimal sum
    # We consider that the bottom right has the maximal sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now we take the difference between the pairs points
    # the bottom left has the largest difference
    # the top right has the smallest difference
    diff = np.diff(pts, axis=1)
    rect[3] = pts[np.argmax(diff)]
    rect[1] = pts[np.argmin(diff)]

    return rect

def points_transform(image, pts):
    """Points transform function.
    This function transforms images considering warp perspective using OpenCV
    Arg:
        image: image to be processed
        pts: list of point (the ROI), the image will be processed according with these points
    return warped image
    """
    rect = pairs_points(pts)
    (tl, tr, bl, br) = rect

    # We decompose the region of interest into two rectangle to calculate distances between points
    # We use it to define the new image width and height

    width1 = np.sqrt(((br[0] - bl[0])**2) + ((br[1] - bl[1])**2))
    width2 = np.sqrt(((tr[0] - tl[0])**2) + ((tr[1] - tl[1])**2))

    # getting the maximal value
    nW = max(int(width1), int(width2))
    height1 = np.sqrt(((tl[0] - bl[0])**2) + ((tl[1] - bl[1])**2))
    height2 = np.sqrt(((tr[0] -br[0])**2) + ((tr[1] - br[1])**2))
    nH = max(int(height1), int(height2))
    # Defining the dimension of the new image
    # We set the arry for the pairs coordinates following this order
    # top left, top right, botton rightm, bottom left
    dst = np.array([
        [0, 0],
        [nW -1, 0],
        [nW -1, nH -1],
        [0, nH -1]], dtype='float32')
    # computing the matrix transformations
    M = cv.getPerspectiveTransform(rect, dst)
    # Transforming the image
    warped = cv.warpPerspective(image, M, (nW, nH))
    return warped
