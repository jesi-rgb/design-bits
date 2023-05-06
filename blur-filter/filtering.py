import sys

sys.path.insert(1, "utils/")

import numpy as np
from scipy.ndimage import maximum_filter, minimum_filter
from skimage.filters import unsharp_mask
import cv2 as cv

from PIL import Image

from blur_utils import convolve, get_gaussian_kernel, get_sharpen_kernel


def sharpen_image(img):
    return cv.filter2D(img, -1, get_sharpen_kernel())


if __name__ == "__main__":
    img = cv.imread("assets/blossom.png", 0)

    blur_img = cv.GaussianBlur(img, (17, 17), 0)
    sharpened_image = unsharp_mask(img, radius=5, amount=1) * 255
    min_image = minimum_filter(img, 9)
    max_image = maximum_filter(img, 9)

    cv.imwrite("assets/blossom_gray.png", img)
    cv.imwrite("assets/blossom_blur.png", blur_img)
    cv.imwrite("assets/blossom_sharpen.png", sharpened_image)
    cv.imwrite("assets/blossom_max.png", max_image)
    cv.imwrite("assets/blossom_min.png", min_image)
