import sys
from coldtype.fx.skia import phototype

from coldtype.warping import warp

sys.path.insert(1, "utils/")

from design_bits_system import *

from coldtype import *

skia = Font.Cacheable("~/fonts/variable/Skia.ttf")

text = "SKIA"


@animation(
    (1920, 1080), timeline=Timeline(500, 60), composites=1, render_bg=1, bg=DB_BLACK
)
def scratch(f):
    yolo = (
        Glyphwise(
            text,
            lambda g: Style(
                skia,
                600,
                wght=f.e("eeio", 1),
                wdth=f.e("eeio", 2),
                tu=f.e("eeio", 2, rng=(-200, 0)),
                baselineShift=f.adj(-g.i * 50).e("qeio", 1, rng=(-100, 100)),
                ro=1,
            ),
        )
        .f(DB_LIGHT_GREEN)
        .ssw(DB_BLACK, f.e("eeio", 1, rng=(0, 20)))
        .align(f.a.r)
        .reversePens()
        # .ch(phototype(cut=130, blur=0.3, cutw=30, fill=DB_LIGHT_GREEN))
    )
    return [yolo]
