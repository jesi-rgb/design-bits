import sys

sys.path.insert(1, "utils/")

from numpy.lib.stride_tricks import sliding_window_view


from manim import *
from utils import PixelArray, focus_on
from design_bits_system import *
from blur_utils import convolve, get_blur_kernel, get_gaussian_kernel

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
            kernel_mob.animate.set_opacity(0.5),
            FadeIn(new_arr_mob),
            focus_on(frame, [img_mob, new_arr_mob], buff=2),
            FadeIn(kernel_center_mob),
        )

        sliding_windows = sliding_window_view(img_arr_pad, kernel_mob.shape)
        for i in range(img_mob.shape[0]):
            for j in range(img_mob.shape[1]):
                pad_section = sliding_windows[i, j]

                new_val = np.sum(pad_section / 255 * kernel)

                self.play(
                    kernel_mob.animate.move_to(img_mob[i, j]),
                    new_arr_mob.update_index((i, j), new_val),
                    run_time=1 / (i + 1),
                )

        self.wait()

        self.play(FadeOut(kernel_mob), FadeOut(kernel_center_mob))

        self.wait()
        self.play(
            *[p.number.animate.set_opacity(0) for p in img_mob],
            *[p.number.animate.set_opacity(0) for p in new_arr_mob],
            focus_on(frame, [img_mob, new_arr_mob], buff=390),
            run_time=3,
        )

        self.wait()


class GaussianConvolution(MovingCameraScene):
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

        kernel_size = 3
        padding = kernel_size // 2
        img_arr_pad = np.pad(
            img_arr, ((padding, padding), (padding, padding)), mode="constant"
        )

        img_mob = PixelArray(
            img_arr,
            include_numbers=True,
            color_mode="GRAY",
            fit_to_frame=False,
            normalize=True,
        )

        kernel = get_gaussian_kernel(kernel_size)
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
            kernel_mob.animate.set_opacity(0.5),
            FadeIn(new_arr_mob),
            focus_on(frame, [img_mob, new_arr_mob], buff=2),
            FadeIn(kernel_center_mob),
        )

        sliding_windows = sliding_window_view(img_arr_pad, kernel_mob.shape)
        for i in range(img_mob.shape[0]):
            for j in range(img_mob.shape[1]):
                pad_section = sliding_windows[i, j]

                new_val = np.sum(pad_section / 255 * kernel)

                self.play(
                    kernel_mob.animate.move_to(img_mob[i, j]),
                    new_arr_mob.update_index((i, j), new_val),
                )

        self.wait()

        self.play(FadeOut(kernel_mob))

        self.wait()


class CompareKernels(MovingCameraScene):
    def construct(self):
        big_kernel = get_gaussian_kernel(7)

        big_kernel_mob = PixelArray(big_kernel, include_numbers=True, normalize=True)

        self.play(FadeIn(big_kernel_mob))

        self.wait()


class BoxFilterExample(MovingCameraScene):
    def construct(self):

        np.random.seed(12)
        frame = self.camera.frame

        dims = 15
        img_array = np.zeros((dims, dims), dtype=np.uint8)
        img_array[:, dims // 2] = 127
        img_array[dims // 2, :] = 127

        img_mob = PixelArray(img_array, outline=False, include_numbers=True)

        self.play(FadeIn(img_mob))
        self.wait()

        target_pixel = img_mob[dims // 2, dims // 2]
        neighbourhood_target = (
            Square()
            .scale_to_fit_width(img_mob[0:3].width)
            .set_color(DB_LIGHT_GREEN)
            .set_stroke(width=0.8)
            .move_to(img_mob)
        )

        self.play(
            focus_on(frame, target_pixel, buff=3),
            target_pixel.pixel.animate.set_fill(DB_YELLOW),
            target_pixel.number.animate.set_fill(DB_BLACK),
            FadeIn(neighbourhood_target),
            run_time=3,
        )

        neighbours = [
            (dims // 2 - 1, dims // 2 - 1),
            (dims // 2, dims // 2 - 1),
            (dims // 2 + 1, dims // 2 - 1),
            (dims // 2 + 1, dims // 2),
            (dims // 2 + 1, dims // 2 + 1),
            (dims // 2, dims // 2 + 1),
            (dims // 2 - 1, dims // 2 + 1),
            (dims // 2 - 1, dims // 2),
            (dims // 2, dims // 2),
        ]

        self.wait()

        self.play(
            LaggedStart(
                *[
                    Indicate(img_mob[n], scale_factor=1.09, color=DB_YELLOW)
                    for n in neighbours
                ],
                lag_ratio=0.1,
            )
        )

        self.wait()

        self.play(frame.animate.shift(RIGHT * 1.5))

        all_numbers = (
            VGroup(*[img_mob[n].number.copy() for n in neighbours])
            .set_color(WHITE)
            .arrange(DOWN, aligned_edge=RIGHT, buff=0.1)
            .next_to(img_mob, RIGHT, buff=1)
            .shift(UP * 0.2)
        )
        line = (
            Line(LEFT * 0.9, ORIGIN)
            .set_stroke(width=0.9, color=DB_LIGHT_GREEN)
            .next_to(all_numbers, DOWN, aligned_edge=RIGHT, buff=0.1)
        )
        plus_sign = (
            Text("+", font=DB_MONO)
            .scale(0.3)
            .next_to(line, UP, aligned_edge=LEFT, buff=0.1)
        )

        all_n_sum = sum([int(n.text) for n in all_numbers])
        all_n_sum_mob = (
            Text(
                str(all_n_sum),
                font=DB_MONO,
                weight=SEMIBOLD,
            )
            .scale(0.3)
            .next_to(line, DOWN, buff=0.1, aligned_edge=RIGHT)
        )

        self.play(*[FadeIn(n) for n in all_numbers])

        self.wait()

        self.play(
            LaggedStart(
                Write(line), Write(plus_sign), FadeIn(all_n_sum_mob), lag_ratio=0.1
            )
        )

        self.wait()

        self.play(
            LaggedStartMap(FadeOut, all_numbers),
            FadeOut(line, shift=LEFT * 0.3),
            FadeOut(plus_sign),
        )

        self.play(
            all_n_sum_mob.animate.next_to(img_mob, RIGHT, coor_mask=[0, 1, 0]).shift(
                UP * 0.3
            ),
        )

        division = (
            Text(
                "÷  9",
                font=DB_MONO,
                weight=SEMIBOLD,
            )
            .scale(0.3)
            .next_to(all_n_sum_mob, DOWN, buff=0.1, aligned_edge=RIGHT)
        )

        line.next_to(division, DOWN, aligned_edge=RIGHT, buff=0.1)

        all_n_avg_round = int(np.around(all_n_sum / 9))
        all_n_avg = (
            Text(
                str(all_n_avg_round),
                font=DB_MONO,
                weight=SEMIBOLD,
            )
            .scale(0.3)
            .next_to(line, DOWN, buff=0.1, aligned_edge=RIGHT)
        )

        self.play(FadeIn(division), Write(line), FadeIn(all_n_avg))

        self.wait()

        self.play(img_mob.update_index((dims // 2, dims // 2), all_n_avg_round))

        blurred_array = convolve(img_array, get_blur_kernel(3))
        blur_mob = PixelArray(blurred_array, include_numbers=True)

        self.wait()

        self.play(FadeOut(neighbourhood_target))

        self.wait()

        self.play(
            FadeOut(all_n_avg, division, line, all_n_sum_mob),
            focus_on(frame, blur_mob),
            run_time=3,
        )

        self.wait()

        self.play(
            LaggedStart(
                *[FadeTransform(i, b) for i, b in zip(img_mob, blur_mob)],
                lag_ratio=0.005,
            ),
            run_time=3,
        )

        self.wait()
