import sys

sys.path.insert(1, "utils/")

from design_bits_system import *

from coldtype import *
from coldtype.fx.skia import phototype, spackle
from coldtype.fx.motion import filmjitter
from coldtype.warping import warp

mona = Font.Cacheable("~/fonts/variable/Mona-Sans.ttf")

factor = 1


@ui((1300, 1300), clip_cursor=False, render_bg=1, bg=DB_BLACK)
def cursor_interp(u):
    ri = u.r.inset(200)
    sx, sy = ri.ipos(u.c)
    print(sx, sy)

    rect_bounds = P(ri).fssw(-1, DB_LIGHT_GREEN, 2)

    reactive_text_base = (
        StSt(
            "VARI\nABLE",
            mona,
            150,
            fill=DB_LIGHT_GREEN,
            wdth=sx,
            wght=sy,
        )
        .xalign(u.r)
        .lead(30)
        .align(u.r)
        .ch(
            warp(
                ya=-1,
                speed=sx + sy * 10,
                mult=0.3 + sx * 10,
                xs=1000,
                ys=10.2 + sy * 10,
            )
        )
    )

    reactive_text_effect = (
        StSt("VARI\nABLE", mona, 150, wdth=sx, wght=sy, fill=1)
        .xalign(u.r)
        .lead(30)
        .align(u.r)
        .removeOverlap()
        .outline(1)
        .f(0.8)
        .ch(
            warp(
                ya=-1,
                speed=sx + sy * 10,
                mult=0.3 + sx * 30,
                xs=1000,
                ys=10.2 + sy * 10,
            )
        )
        .ch(phototype(u.r, cut=120, blur=1, cutw=40))
        .blendmode(BlendMode.ColorDodge)
    )

    return [rect_bounds, reactive_text_base, reactive_text_effect]
