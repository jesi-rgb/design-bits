import sys

sys.path.insert(1, "utils/")

from manim import *
from utils import PixelArray
from design_bits_system import *

config.background_color = DB_BLACK


class MatrixComparison(Scene):
    def construct(self):
        base = np.linspace(0, 1, 100)
        blend = np.linspace(0, 1, 100)


class PixelByPixelComparison(Scene):
    def construct(self):
        sample_size = 10
        base = np.ones(sample_size)
        blend = np.random.random(sample_size)
        mult_blend = base * blend

        base_mob = PixelArray(
            base * 255, color_mode="GRAY", normalize=True, include_numbers=True
        )
        blend_mob = PixelArray(blend * 255, color_mode="GRAY", include_numbers=True)
        mult_mob = PixelArray(mult_blend * 255, color_mode="GRAY", include_numbers=True)

        operation = VGroup(base_mob, blend_mob, mult_mob).arrange(DOWN)

        self.add(operation)
