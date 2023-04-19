import sys

sys.path.insert(1, "utils/")

from manim import *
from utils import PixelArray
from design_bits_system import *

config.background_color = DB_BLACK


class Convolution(Scene):
    def construct(self):
        kernel = np.ones((3, 3)) * 1 / 9 * 255
        print(kernel)
        kernel_mob = PixelArray(
            kernel,
            color_mode="GRAY",
            fit_to_frame=True,
            include_numbers=True,
            normalize=True,
        )

        self.add(kernel_mob)
