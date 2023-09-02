import sys

sys.path.insert(1, "utils/")

from design_bits_system import *

from coldtype import *
from coldtype.fx.skia import phototype, potrace
from coldtype.warping import warp

mona = Font.Cacheable("~/fonts/variable/Mona-Sans.ttf")
ancho = Font.Cacheable("~/fonts/variable/AnchoGX.ttf")
skia = Font.Cacheable("~/fonts/variable/Skia.ttf")
kablammo = Font.Cacheable("~/fonts/variable/Kablammo.ttf")

factor = 1


@animation(
    (1920 * factor, 1080 * factor),
    composites=1,
    timeline=Timeline(1000, fps=60),
    bg=DB_BLACK,
    render_bg=1,
)
def wave(f):
    return (
        Glyphwise(
            "POOL PARTY",
            lambda g: Style(
                kablammo,
                300,
                fill=DB_LIGHT_GREEN,
                wght=f.adj(g.i * 4).e(
                    "ceio",
                    1,
                ),
                wdth=f.adj(g.i * 4).e(
                    "qeio",
                    1,
                ),
                MORF=f.adj(-g.i * 5).e("seio", 5),
                tu=f.e("seio", 16, rng=(-400, 100)),
                rotate=f.adj(-g.i * 3).e("qeio", 4, rng=(-20, 20)),
                baselineShift=f.adj(-g.i * 10).e("qeio", 10, rng=(-100, 100)),
                ro=1,
            ),
            multiline=True,
        )
        .align(f.a.r)
        .understroke(DB_BLACK, 20)
        .insert(0, f.last_render())
        .ch(
            phototype(
                cut=f.e("seio", 5, rng=(80, 120)),
                blur=4,
                cutw=20,
                fill=DB_LIGHT_GREEN,
            )
        )
    )


def release(passes):
    FFMPEGExport(wave, passes).prores().write()
