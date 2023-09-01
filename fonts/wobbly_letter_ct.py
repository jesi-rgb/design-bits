import sys

sys.path.insert(1, "utils/")

from design_bits_system import *

from coldtype import *
from coldtype.fx.skia import phototype, spackle
from coldtype.fx.motion import filmjitter
from coldtype.warping import warp

recursive = Font.Cacheable("~/fonts/variable/Recursive.ttf")

factor = 1


timeline = """
[a             ]
             [b                 ]
"""
at = AsciiTimeline(8, 60, timeline).inflate()


@animation(
    (1920 * factor, 1080 * factor), composites=1, timeline=at, bg=DB_BLACK, render_bg=1
)
def wobbly_letter(f):
    c = at.current()
    return PS(
        [
            StSt(
                "B",
                Font.MutatorSans(),
                wdth=f.e("seio", 1),
                font_size=800,
                fill=DB_LIGHT_GREEN,
            ).align(f.a.r),
            StSt(
                "B",
                Font.MutatorSans(),
                wdth=f.e("seio", 1),
                font_size=800,
                fill=DB_LIGHT_GREEN,
            )
            .align(f.a.r)
            .removeOverlap()
            .outline(2)
            .ch(
                warp(
                    mult=8,
                    speed=2,
                    ya=1 + f.i * 100,
                    xa=1 + f.i * 100,
                    xs=1900,
                    ys=1900,
                )
            )
            .ch(phototype(f.a.r, cut=200, blur=0.3, cutw=20))
            .blendmode(BlendMode.Difference),
        ]
    )
