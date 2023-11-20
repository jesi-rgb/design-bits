import sys


sys.path.insert(1, "utils/")

from manim import *
from utils import *
from design_bits_system import *
import pandas as pd

config.background_color = DB_BLACK

sheet_id = "1I8vFf0MiK4RKKeipSoDnDISm5wk9-Re6tgxE9NXCkTM"
sheet_name = "Sheet1"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"


def map_range(v, a, b, c, d):
    return (v - a) / (b - a) * (d - c) + c


class FontTimeline(MovingCameraScene):
    def construct(self):
        frame = self.camera.frame

        data = pd.read_csv(url).iloc[:, :2].to_dict(orient="list")

        length = 60
        buff_from_line = 0.5

        line = Line(LEFT * length, RIGHT * length, color=DB_LIGHT_GREEN).set_stroke(
            width=1
        )

        font_data_mob = VGroup(
            *[
                VGroup(
                    Text(f, weight=MEDIUM, font=f, color=DB_LIGHT_GREEN).scale(0.4),
                    Text(
                        str(d), color=DB_LIGHT_GREEN, font=DB_MONO, weight=LIGHT
                    ).scale(0.3),
                )
                .arrange(UP if i % 2 != 0 else DOWN, buff=0.1)
                .move_to(
                    line.point_from_proportion(
                        map_range(
                            d,
                            np.min(data["Date"]) - 10,
                            np.max(data["Date"]) + 10,
                            0,
                            1,
                        )
                    )
                )
                .shift(UP * buff_from_line if i % 2 == 0 else DOWN * buff_from_line)
                for i, (f, d) in enumerate(zip(data["Font"], data["Date"]))
            ]
        )
        font_data_mob[15].shift(DOWN * 0.3)
        ticks = VGroup(
            *[
                Line(ORIGIN, UP * 0.2, color=DB_LIGHT_GREEN)
                .set_stroke(width=0.6)
                .move_to(
                    line.point_from_proportion(
                        map_range(
                            d,
                            np.min(data["Date"]) - 10,
                            np.max(data["Date"]) + 10,
                            0,
                            1,
                        )
                    )
                )
                for d in data["Date"]
            ]
        )

        self.play(focus_on(frame, ticks[0], buff=10))
        self.play(FadeIn(font_data_mob, ticks, line))
        self.wait(2)

        for i in [1, 2, 3, 5, 10, -2]:
            self.play(
                focus_on(
                    frame,
                    ticks[i],
                    buff=10,
                ),
                run_time=6,
            )

        self.wait(3)


class CharacterTable(MovingCameraScene):
    def construct(self):
        frame = self.camera.frame
        letters = [[c, str(ord(c))] for c in "abcdefghijklmnopqrstuvwxyz"]
        symbols = [[c, str(ord(c))] for c in ".,:;-?!*^[]{}#¢%"]

        caps = [[c, str(ord(c))] for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        nums = [[c, str(ord(c))] for c in "0123456789"]
        chars_table = Table(
            letters,
            element_to_mobject=DBTitle,
        )
        nums_table = Table(
            nums,
            element_to_mobject=DBTitle,
        )
        caps_table = Table(
            caps,
            element_to_mobject=DBTitle,
        )
        symbols_table = Table(
            symbols,
            element_to_mobject=DBTitle,
        )

        tables = VGroup(nums_table, symbols_table, caps_table, chars_table).arrange(
            RIGHT, aligned_edge=UP
        )
        self.play(focus_on(frame, tables, buff=-20.2))
        self.play(FadeIn(tables))
