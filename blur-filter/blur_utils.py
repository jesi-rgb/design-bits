import numpy as np
from manim import *
import cv2 as cv

from utils import PixelArray


def convolve_mob(img: np.ndarray, kernel: np.ndarray) -> PixelArray:
    convolved_arr = cv.filter2D(img, cv.CV_8U, kernel)
    return ImageMobject(convolved_arr)


def get_blur_kernel(shape: int = 3) -> np.ndarray:
    return np.ones((shape, shape)) * (1 / (shape**2)) * 255


def get_image(path: str) -> np.ndarray:
    return ImageMobject(path, image_mode="L").get_pixel_array()[:, :, 0]
