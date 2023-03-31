from itertools import combinations
import sys

sys.path.insert(1, "utils/")

from manim import *
from utils import PixelArray, focus_on
from design_bits_system import *

config.background_color = DB_BLACK


def multiply(i, j):
    return i * j


def screen(i, j):
    return 1 - ((1 - i) * (1 - j))


class MatrixComparison(MovingCameraScene):
    def construct(self):
        frame = self.camera.frame

        sample_size = 10
        mult_matrix = self.build_matrix_comparison(
            sample_size=sample_size, operation=multiply
        )
        screen_matrix = self.build_matrix_comparison(operation=screen)

        mult_matrix_mob = PixelArray(
            mult_matrix * 255, color_mode="GRAY", include_numbers=True, normalize=True
        )
        screen_matrix_mob = PixelArray(
            screen_matrix * 255, color_mode="GRAY", include_numbers=True, normalize=True
        )
        blend_scale = (
            PixelArray(
                np.linspace(1, 0, sample_size) * 255,
                color_mode="GRAY",
                include_numbers=True,
                normalize=True,
            )
            .arrange(DOWN, buff=0)
            .next_to(mult_matrix_mob, LEFT, buff=1)
        )
        base_scale = PixelArray(
            np.linspace(0, 1, sample_size) * 255,
            color_mode="GRAY",
            include_numbers=True,
            normalize=True,
        ).next_to(mult_matrix_mob, DOWN, buff=1)

        demo = VGroup(mult_matrix_mob, blend_scale, base_scale)
        self.play(FadeIn(demo))
        self.play(focus_on(frame, demo, buff=1))

        self.play(Transform(mult_matrix_mob, screen_matrix_mob))

    def build_matrix_comparison(self, sample_size=10, operation=multiply):
        base = np.linspace(1, 0, sample_size)
        blend = np.linspace(0, 1, sample_size)

        mult_matrix = []
        for i in base:
            aux_arr = []
            for j in blend:
                aux_arr.append(operation(i, j))
            mult_matrix.append(aux_arr)

        return np.array(mult_matrix)


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
