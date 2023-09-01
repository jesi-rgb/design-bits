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
    return [
        P(ri).fssw(-1, DB_LIGHT_GREEN, 2),
        (
            StSt(
                "Hello\nthere",
                mona,
                150,
                fill=DB_LIGHT_GREEN,
                wdth=sx,
                wght=sy,
            )
            .xalign(u.r)
            .lead(30)
            .align(u.r)
        ),
    ]
