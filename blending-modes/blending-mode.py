import sys

sys.path.insert(1, "utils/")

from manim import *
from utils import PixelArray, focus_on
from design_bits_system import *

config.background_color = DB_BLACK


def clamp(i):
    return np.clip(i, 0, 1)


# blend modes
def multiply(b, f):
    return b * f


def screen(b, f):
    return 1 - ((1 - b) * (1 - f))


def lighten(i, j):
    return i if i > j else j


def darken(b, f):
    return b if b < f else f


def color_burn(b, f):
    return 1 - clamp((1 - b) / (f + 0.0001))


def color_dodge(b, f):
    return clamp(b / ((1 - f) + 0.0001))


def overlay(b, f):
    return 2 * b * f if b < 0.5 else 1 - 2 * (1 - b) * (1 - f)


def hard_light(b, f):
    return 2 * b * f if f < 0.5 else 1 - 2 * (1 - b) * (1 - f)


def soft_light(b, f):
    step1 = 1 - (f * 2)
    step2 = b * b
    step3 = step1 * step2
    step4 = 2 * f * b

    return clamp(step3 + step4)


def difference(b, f):
    return abs(f - b)


def subtract(b, f):
    return max(f - b, 0)


class MatrixComparison(MovingCameraScene):
    def construct(self):
        frame = self.camera.frame

        sample_size = 11
        mult_matrix = self.build_matrix_comparison(
            sample_size=sample_size, operation=subtract
        )
        screen_matrix = self.build_matrix_comparison(
            sample_size=sample_size, operation=screen
        )

        mult_matrix_mob = PixelArray(
            mult_matrix * 255, color_mode="GRAY", include_numbers=True, normalize=True
        )

        screen_matrix_mob = PixelArray(
            screen_matrix * 255, color_mode="GRAY", include_numbers=True, normalize=True
        )

        foreground_scale = (
            PixelArray(
                np.linspace(0, 1, sample_size) * 255,
                color_mode="GRAY",
                include_numbers=True,
                normalize=True,
            )
            .arrange(DOWN, buff=0)
            .next_to(mult_matrix_mob, LEFT, buff=1)
        )
        background_scale = PixelArray(
            np.linspace(0, 1, sample_size) * 255,
            color_mode="GRAY",
            include_numbers=True,
            normalize=True,
        ).next_to(mult_matrix_mob, UP, buff=1)

        mult_title = (
            Text("Multiply", font=DB_FONT, weight=SEMIBOLD)
            .set_color(DB_LIGHT_GREEN)
            .scale(1.8)
            .next_to(VGroup(mult_matrix_mob, foreground_scale), UP, buff=1)
        )
        screen_title = (
            Text("Screen", font=DB_FONT, weight=SEMIBOLD)
            .set_color(DB_LIGHT_GREEN)
            .scale(1.8)
            .next_to(VGroup(mult_matrix_mob, foreground_scale), UP, buff=1)
        )
        demo = VGroup(mult_matrix_mob, foreground_scale, background_scale)
        self.play(
            FadeIn(
                demo,
            )
        )
        self.play(focus_on(frame, [demo, mult_title], buff=1))

        # self.play(
        #     Transform(mult_matrix_mob, screen_matrix_mob),
        #     FadeTransform(mult_title, screen_title),
        # )

    def build_matrix_comparison(self, sample_size=11, operation=multiply):
        base = np.linspace(0, 1, sample_size)
        blend = base.copy()

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
