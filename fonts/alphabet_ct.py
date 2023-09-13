import sys

sys.path.insert(1, "utils/")

from design_bits_system import *

from coldtype import *
from coldtype.warping import warp

factor = 20
length = 86
tl = Timeline(length * factor, fps=60)

font = Font.Cacheable("~/fonts/variable/Mona-Sans.ttf")


video_scale = 2


@animation(
    rect=(1920 * video_scale, 1080 * video_scale),
    timeline=tl,
    composites=1,
    bg=DB_BLACK,
)
def alphabet(f):
    pe = f.e(e := "qeio", 8)
    return [
        # P(f.a.r.inset(70))
        # .fssw(-1, DB_LIGHT_GREEN, 2, 1)
        # .ch(warp(f.i * 30, f.i, mult=100)),
        P(
            StSt(
                chr(65 + f.i // 20),
                font,
                f.e(e, r=(1300, 1700)),
                wdth=1 - pe,
                wght=pe,
                ro=1,
            )
            .fssw(-1, DB_LIGHT_GREEN, 2)
            .align(f.a.r, tx=1)
        )
        .insert(0, f.last_render())
        .insert(1, P(f.a.r).f(DB_BLACK, 0.1)),
    ]


def release(passes):
    FFMPEGExport(alphabet, passes).prores().write().open()
