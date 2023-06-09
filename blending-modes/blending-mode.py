import sys

sys.path.insert(1, "utils/")

from manim import *
from utils import PixelArray, DBTitle, focus_on
from design_bits_system import *

config.background_color = DB_BLACK


def clamp(i):
    return np.clip(i, 0, 1)


# blend modes


def lighten(b, f):
    return max(b, f)


def darken(b, f):
    return min(b, f)


def multiply(b, f):
    return b * f


def screen(b, f):
    return 1 - ((1 - b) * (1 - f))


def color_burn(b, f):
    return 1 - clamp((1 - b) / (f + 0.0001))


def color_dodge(b, f):
    return clamp(b / ((1 - f) + 0.0001))


def color_dodge_css(b, f):
    if b == 0:
        return 0
    elif f == 1:
        return 1
    else:
        return min(1, b / (1 - f))


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
        lighten_matrix = self.build_matrix_comparison(
            sample_size=sample_size, operation=color_dodge
        )
        lighten_matrix_mob = PixelArray(
            lighten_matrix * 255,
            normalize=True,
            include_numbers=True,
            color_mode="GRAY",
        )

        foreground_scale = (
            PixelArray(
                np.linspace(0, 1, sample_size) * 255,
                color_mode="GRAY",
                include_numbers=True,
                normalize=True,
            )
            .arrange(DOWN, buff=0)
            .next_to(lighten_matrix_mob, LEFT, buff=1)
        )
        background_scale = PixelArray(
            np.linspace(0, 1, sample_size) * 255,
            color_mode="GRAY",
            include_numbers=True,
            normalize=True,
        ).next_to(lighten_matrix_mob, UP, buff=1)

        title = (
            Text("Lighten", font=DB_FONT, weight=SEMIBOLD)
            .set_color(DB_LIGHT_GREEN)
            .scale(1.8)
            .next_to(
                VGroup(lighten_matrix_mob, foreground_scale, background_scale),
                UP,
                buff=1,
            )
        )
        demo = VGroup(lighten_matrix_mob, foreground_scale, background_scale)

        self.play(FadeIn(demo))
        self.play(focus_on(frame, [demo, title], buff=1))

        modes = {
            "Lighten": lighten,
            "Darken": darken,
            "Multiply": multiply,
            "Screen": screen,
            "Overlay": overlay,
            "Hard Light": hard_light,
            "Soft Light": soft_light,
            "Difference": difference,
            "Subtract": subtract,
        }

        for t, mode in modes.items():
            new_title = DBTitle(t).scale(1.8).move_to(title)
            matrix_mode = self.build_matrix_comparison(sample_size, mode)
            matrix_mob = PixelArray(
                matrix_mode * 255,
                normalize=True,
                include_numbers=True,
                color_mode="GRAY",
            )
            self.play(
                FadeOut(title, shift=UP * 0.3),
                FadeIn(new_title, shift=UP * 0.3),
                Transform(lighten_matrix_mob, matrix_mob),
            )
            title = new_title
            self.wait()

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
