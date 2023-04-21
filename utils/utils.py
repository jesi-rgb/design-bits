from manim import *
from typing import Iterable
from math import floor
from design_bits_system import *


def get_1d_index(i, j, pixel_array):
    return pixel_array.shape[1] * i + j


def g2h(n):
    """Abbreviation for grayscale to hex"""
    return rgb_to_hex((n, n, n))


def focus_on(frame, mobjects, buff=1):
    """Returns a ready to play animation of the camera focusing on a given mobject"""
    if isinstance(mobjects, Iterable):
        vmobject = VGroup(*mobjects)
    elif isinstance(mobjects, Mobject) or isinstance(mobjects, VGroup):
        vmobject = mobjects
    else:
        raise TypeError(
            "Mobjects argument can either be a single mobject, a single VGroup or an iterable of mobjects (tuple, list, np.array...)"
        )

    frame_aspect_ratio = config.frame_width / config.frame_height
    mob_aspect_ratio = vmobject.width / vmobject.height

    if mob_aspect_ratio > frame_aspect_ratio:
        return frame.animate.set_width(vmobject.width + buff).move_to(vmobject)
    else:
        return frame.animate.set_height(vmobject.height + buff).move_to(vmobject)


###
### CLASSES
###


class DBTitle(Text):
    def __init__(self, text, weight=SEMIBOLD):
        super().__init__(text, weight=weight, font=DB_FONT)
        self.set_color(DB_LIGHT_GREEN)


class Pixel(VGroup):
    def __init__(
        self, n, color_mode: str, outline=True, normalize=False, include_numbers=True
    ):
        assert color_mode in ("RGB", "GRAY"), "Color modes are RGB and GRAY"

        if color_mode == "RGB":
            if not isinstance(n, Iterable):
                raise TypeError(
                    "The value passed for Pixel in RGB was not an array of R, G and B values. Make sure the input image has shape m x n x 3 or change the mode to GRAY"
                )
            color = rgb_to_hex(n / 255)
        else:
            if isinstance(n, np.int16) or n < 0:
                n = abs(n)
            color = g2h(n / 255)

        self.pixel = Square(side_length=1)
        self.pixel.set_fill(color, opacity=1)
        self.n = n

        if outline:
            self.pixel.set_stroke(WHITE, width=0.5)
        else:
            self.pixel.set_stroke(WHITE, width=0.0)

        if normalize:
            number_string = f"{n/255:.2f}"
        else:
            number_string = str(floor(n))

        if include_numbers:
            self.number = (
                Text(number_string, font=DB_MONO, weight=SEMIBOLD)
                .scale(0.7)
                .set_color(g2h(1) if abs(n) < 170 else g2h(0))
                .set_stroke(opacity=1 if include_numbers else 0)
            )

            if normalize:
                self.number.scale_to_fit_width(
                    self.pixel.width - self.pixel.width * 0.3
                )

            super().__init__(self.pixel, self.number)
        else:
            super().__init__(self.pixel)


class PixelArray(VGroup):
    def __init__(
        self,
        img: np.ndarray,
        include_numbers=False,
        color_mode="GRAY",
        normalize=False,
        buff=0,
        outline=True,
        fit_to_frame=True,
    ):
        assert color_mode in ("RGB", "GRAY"), "Color modes are RGB and GRAY"

        self.img = img
        self.color_mode = color_mode
        self.include_numbers = include_numbers
        self.normalize = normalize

        self.shape = img.shape

        self.pixels = [
            Pixel(
                p,
                outline=outline,
                color_mode=self.color_mode,
                normalize=self.normalize,
                include_numbers=self.include_numbers,
            )
            for p in img.flatten()
        ]

        super().__init__(*self.pixels)

        if len(img.shape) == 1:
            self.arrange(RIGHT, buff=buff)
        else:
            self.arrange_in_grid(img.shape[0], img.shape[1], buff=buff)

        if fit_to_frame:
            frame_aspect_ratio = config.frame_width / config.frame_height
            mob_aspect_ratio = self.width / self.height

            # this means the mob is wider than it is taller
            if mob_aspect_ratio > frame_aspect_ratio:
                self.scale_to_fit_width(config.frame_width - config.frame_width * 0.3)
            else:
                self.scale_to_fit_height(
                    config.frame_height - config.frame_height * 0.3
                )

        self.dict = {index: p for index, p in enumerate(self)}

    def __getitem__(self, value) -> VGroup:
        if isinstance(value, slice):
            return VGroup(*list(self.dict.values())[value])
        elif isinstance(value, tuple):
            i, j = value
            one_d_index = get_1d_index(i, j, self.img)
            return self.dict[one_d_index]
        else:
            return self.dict[value]

    def update_index(self, index, new_value) -> Animation:
        if isinstance(index, tuple):
            i, j = index
            one_d_index = get_1d_index(i, j, self.img)
            pixel_mob = self.dict[one_d_index]
        elif isinstance(index, int):
            pixel_mob = self.dict[index]
        else:
            raise TypeError("index must be either a tuple or an integer")

        new_pixel = VGroup(
            Pixel(
                new_value,
                color_mode=self.color_mode,
                normalize=self.normalize,
                include_numbers=self.include_numbers,
            )
            .scale_to_fit_height(pixel_mob.height)
            .move_to(pixel_mob),
        )
        animation = FadeTransform(pixel_mob, new_pixel)
        pixel_mob = new_pixel

        return animation
