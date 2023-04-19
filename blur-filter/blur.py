import sys

from numpy.lib.stride_tricks import sliding_window_view

sys.path.insert(1, "utils/")

from manim import *
from utils import PixelArray, floor, focus_on
from design_bits_system import *
from blur_utils import convolve_mob, get_blur_kernel, get_image

config.background_color = DB_BLACK


class Kernel(Scene):
    def construct(self):
        kernel = get_blur_kernel(3)
        kernel_mob = PixelArray(
            kernel,
            color_mode="GRAY",
            fit_to_frame=True,
            include_numbers=True,
            normalize=True,
        )

        self.add(kernel_mob)


class Convolution(MovingCameraScene):
    def construct(self):
        frame = self.camera.frame
        img_arr = np.array(
            [
                [0, 0, 255, 0, 0],
                [0, 200, 255, 200, 0],
                [0, 200, 255, 200, 0],
                [0, 200, 255, 200, 0],
                [0, 0, 255, 0, 0],
            ]
        )

        img_arr_pad = np.pad(img_arr, ((1, 1), (1, 1)), mode="constant")

        print("begin")

        img_mob = PixelArray(
            img_arr,
            include_numbers=True,
            color_mode="GRAY",
            fit_to_frame=False,
            normalize=True,
        )

        kernel = get_blur_kernel(3)
        kernel_mob = PixelArray(
            kernel,
            color_mode="GRAY",
            include_numbers=True,
            fit_to_frame=False,
            normalize=True,
        ).next_to(img_mob, RIGHT)

        kernel_center_mob = (
            SurroundingRectangle(kernel_mob[0])
            .set_color(DB_YELLOW)
            .add_updater(lambda mob: mob.move_to(kernel_mob))
        )

        self.play(LaggedStartMap(FadeIn, img_mob))

        self.play(focus_on(frame, [img_mob, kernel_mob]), FadeIn(kernel_mob))

        self.wait()

        aux_rect = Rectangle(width=kernel_mob.width, height=kernel_mob.height).move_to(
            img_mob[0]
        )
        self.play(
            kernel_mob.animate.move_to(img_mob[0]), focus_on(frame, [aux_rect, img_mob])
        )

        self.wait()

        new_arr = np.zeros(img_mob.shape)
        new_arr_mob = PixelArray(
            new_arr,
            color_mode="GRAY",
            include_numbers=True,
            fit_to_frame=False,
            normalize=True,
        ).next_to(img_mob, RIGHT, buff=2)

        self.play(
            *[r.animate.set_opacity(0.5) for r in kernel_mob],
            FadeIn(new_arr_mob),
            focus_on(frame, [img_mob, new_arr_mob], buff=2),
            FadeIn(kernel_center_mob)
        )

        print("before sliding windows")
        sliding_windows = sliding_window_view(img_arr_pad, kernel_mob.shape)
        for i in range(img_mob.shape[0]):
            for j in range(img_mob.shape[1]):
                pad_section = sliding_windows[i, j]

                new_val = np.sum(pad_section / 255 * kernel)

                print(new_val)

                self.play(
                    kernel_mob.animate.move_to(img_mob[i, j]),
                    new_arr_mob.update_index((i, j), new_val),
                )

        self.wait()

        self.play(FadeOut(kernel_mob))

        self.wait()
