import sys

sys.path.insert(1, "utils/")

from design_bits_system import *

from coldtype import *
from coldtype.fx.skia import phototype, spackle
from coldtype.fx.motion import filmjitter

at = AsciiTimeline(
    4,
    60,
    """
                                <
T      Y        P        O      G         R          A       P     H     Y        .""",
).inflate()

rs = random_series(seed=8)


@animation((1920 * 2, 1080 * 2), composites=1, timeline=at, bg=DB_BLACK, render_bg=1)
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
                    base=f.i * 2,
                )
            )
            .ups()
            .insert(0, P(f.a.r).f(1, 0.1))
            .insert(
                0, f.last_render(filmjitter(f.e("l"), speed=(30, 30), scale=(0.3, 0.4)))
            )
            .append(
                StSt(
                    c.name,
                    Font.MutatorSans(),
                    fontSize=c.e("qeio", 0, rng=(100, 1200)),
                    wdth=c.e("qeio", 0),
                    wght=rs[c.idx + 1] * 0.25,
                    ro=1,
                )
                .fssw(DB_BLACK, DB_LIGHT_GREEN, 12)
                .align(f.a.r, th=1, tv=1)
                .blendmode(BlendMode.Xor)
            )
            .ch(phototype(f.a.r, cut=110, blur=0.5, cutw=20))
        ]
    )


def release(passes):
    FFMPEGExport(intro_typography, passes).prores().write()
