import sys

sys.path.insert(1, "utils/")

import numpy as np
from design_bits_system import *

from coldtype import *
from coldtype.fx.skia import phototype, spackle
from coldtype.fx.motion import filmjitter
from coldtype.warping import warp


text = "TYPOGRAPHY."
chars = [c + " " * 6 for c in text]
timeline = str.join("", chars)


at = AsciiTimeline(multiplier=16, fps=60, ascii=timeline).inflate()

rs = random_series(seed=8)

factor = 2


@animation(
    (1920 * factor, 1080 * factor), composites=1, timeline=at, bg=DB_BLACK, render_bg=1
)
def intro_typography(f):
    c = at.current()

    return PS(
        [
            P(f.a.r)
            .ch(
                spackle(
                    xs=0.15,
                    ys=0.15,
                    cut=64,
                    fill=Color.from_html(DB_BLACK),
                    base=f.i,
                )
            )
            .ups()
            .insert(0, f.last_render())
            .layer(
                lambda p: p.ch(
                    warp(
                        speed=9,
                        ys=c.e(
                            "qeio",
                            1,
                            rng=(400, 800),
                        ),
                        xs=c.e(
                            "qeio",
                            1,
                            rng=(400, 800),
                        ),
                    )
                ),
                lambda p: p.ch(
                    phototype(
                        f.a.r, cut=c.e("qeio", 0, rng=(100, 280)), blur=0.0, cutw=10
                    ),
                ),
            )
            .append(
                StSt(
                    c.name,
                    Font.MutatorSans(),
                    fontSize=c.e("qeio", 0, rng=(-2, 1700)),
                    wdth=c.e("qeio", 0),
                    wght=c.e("ceio", 0),
                    ro=1,
                )
                .f(DB_LIGHT_GREEN, c.e("seio", 0, rng=(0.1, 0.0)))
                .ssw(DB_LIGHT_GREEN, 12)
                .align(f.a.r, th=1, tv=1)
                .blendmode(BlendMode.ColorDodge)
            )
            .layer(
                lambda p: p.ch(
                    warp(
                        speed=9,
                        ys=c.e(
                            "qeio",
                            1,
                            rng=(400, 800),
                        ),
                        xs=c.e(
                            "qeio",
                            1,
                            rng=(400, 800),
                        ),
                    )
                ),
                lambda p: p.ch(
                    phototype(
                        f.a.r, cut=c.e("qeio", 0, rng=(100, 180)), blur=0.0, cutw=10
                    ),
                ),
            ),
            Glyphwise(
                "TYPOGRAPHY",
                lambda g: Style(
                    Font.MutatorSans(),
                    fontSize=400,
                    wdth=f.adj(-g.i * 30).e("ceio", 1, rng=(0.2, 0.4)),
                    wght=f.adj(g.i * 30).e("ceio", 1, rngh=(0.2, 0.4)),
                    ro=1,
                ),
            )
            .f(DB_LIGHT_GREEN)
            .ssw(DB_LIGHT_GREEN, 12)
            .align(f.a.r, th=1, tv=1)
            .blendmode(BlendMode.Xor)
            .layer(
                lambda p: p.ch(
                    warp(
                        speed=9,
                        ys=c.e(
                            "qeio",
                            1,
                            rng=(400, 800),
                        ),
                        xs=c.e(
                            "qeio",
                            1,
                            rng=(400, 800),
                        ),
                    )
                ),
                lambda p: p.ch(
                    phototype(
                        f.a.r, cut=c.e("qeio", 0, rng=(100, 180)), blur=0.0, cutw=10
                    ),
                ),
            )
            .translate(0, -400),
            Glyphwise(
                "MODERN",
                lambda g: Style(
                    Font.MutatorSans(),
                    500,
                    wdth=1,
                    wght=f.adj(-g.i * 17).e("qeio", 2, rng=(0, 1)),
                    fill=DB_LIGHT_GREEN,
                ),
            )
            .align(f.a.r)
            .translate(0, 400)
            .layer(lambda p: p.ch(warp(speed=1)).removeOverlap().outline(1)),
            Glyphwise(
                "MODERN",
                lambda g: Style(
                    Font.MutatorSans(),
                    500,
                    wdth=1,
                    wght=f.adj(-g.i * 17).e("qeio", 2, rng=(0, 1)),
                    fill=DB_LIGHT_GREEN,
                ),
            )
            .align(f.a.r)
            .translate(0, 400)
            .layer(
                lambda p: p.ch(warp(speed=2))
                .removeOverlap()
                .outline(1)
                .f(DB_LIGHT_GREEN, 0.4)
            ),
        ]
    )


def release(passes):
    FFMPEGExport(intro_typography, passes).prores().write()
