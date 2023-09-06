import sys

sys.path.insert(1, "utils/")

from design_bits_system import *

from coldtype import *

factor = 10
tl = Timeline(26 * factor, fps=18 * 2)


@animation(rect=(1920, 1080), timeline=tl, bg=DB_BLACK)
def render(f):
    pe = f.e(e := "qeio", 1)
    return [
        P(f.a.r.inset(70)).fssw(-1, DB_LIGHT_GREEN, 2, 1),
        P(
            StSt(
                chr(65 + f.i // factor % 26),
                Font.MutatorSans(),
                f.e(e, r=(500, 750)),
                wdth=1 - pe,
                wght=pe,
            )
            .fssw(-1, DB_LIGHT_GREEN, 3)
            .align(f.a.r, tv=1, th=1)
            .removeOverlap(),
        ),
    ]
