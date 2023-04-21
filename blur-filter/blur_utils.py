import numpy as np
import scipy.stats as st
from manim import *
import cv2 as cv

from utils import PixelArray


def convolve_mob(img: np.ndarray, kernel: np.ndarray) -> PixelArray:
    convolved_arr = cv.filter2D(img, cv.CV_8U, kernel)
    return ImageMobject(convolved_arr)


def get_blur_kernel(shape: int = 3) -> np.ndarray:
    return np.ones((shape, shape)) * (1 / (shape**2)) * 255


def get_gaussian_kernel(size=3, sig=1):
    """Returns a 2D Gaussian kernel."""

    x = np.linspace(-(size / 2) / sig, (size / 2) / sig, size + 1)
    kern1d = np.diff(st.norm.cdf(x))
    kern2d = np.outer(kern1d, kern1d)
    return (kern2d / kern2d.sum()) * 255


def get_image(path: str) -> np.ndarray:
    return ImageMobject(path, image_mode="L").get_pixel_array()[:, :, 0]
