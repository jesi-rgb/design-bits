import sys

sys.path.insert(1, "utils/")

from design_bits_system import *

from coldtype import *
from coldtype.warping import warp

factor = 20
tl = Timeline(26 * factor, fps=60)


@animation(rect=(1920, 1080), timeline=tl, composites=1, bg=DB_BLACK)
def render(f):
    pe = f.e(e := "qeio", 2)
    return [
        P(f.a.r.inset(70))
        .fssw(-1, DB_LIGHT_GREEN, 2, 1)
        .ch(warp(f.i * 30, f.i, mult=100)),
        P(
            StSt(
                chr(65 + f.i // factor % 26),
                Font.MutatorSans(),
                f.e(e, r=(500, 750)),
                wdth=1 - pe,
                wght=pe,
                ro=1,
            )
            .fssw(-1, DB_LIGHT_GREEN, 3)
            .align(f.a.r, tx=1)
            .insert(0, f.last_render())
            .insert(1, P(f.a.r).f(DB_BLACK, 0.05))
        ),
    ]
