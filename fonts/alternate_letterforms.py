import sys

sys.path.insert(1, "utils/")


from design_bits_system import *

from coldtype import *
from coldtype.fx.skia import phototype, spackle
from coldtype.fx.motion import filmjitter
from coldtype.warping import warp

name = Font.Cacheable("~/fonts/variable/NameSans.ttf")
supreme = Font.Cacheable("~/fonts/variable/Supreme.ttf")

work = Font.Cacheable("~/fonts/variable/WorkSans.ttf")

factor = 1


states = {
    "A": dict(wght=0.3),
    "B": dict(wght=0.9),
    "C": dict(wght=0.3),
}
at = AsciiTimeline(
    10,
    60,
    """
                                <
[A  ]       [B     ]       [C ]   
         [I  ]
""",
    states,
).shift("end", -8)


@animation((1920, 1080), render_bg=1, bg=DB_BLACK, timeline=at)
def alternates_a(f):
    main = StSt(
        "a",
        name,
        900,
        opsz=1,
        wght=at.kf("eleo")["wght"],
        fill=DB_LIGHT_GREEN,
    )

    alternate = StSt(
        "a",
        name,
        900,
        opsz=1,
        wght=at.kf("eleo")["wght"],
        features={"ss09": True},
        fill=DB_LIGHT_GREEN,
    )

    label = StSt(
        "At Name Sans",
        supreme,
        50,
        tu=-40,
        fill=DB_DARK_GREEN,
    ).align(f.a.r.inset(80), y="mny")

    group = PS(main, alternate).spread(tracking=400).align(f.a.r).translate(x=0, y=150)

    return (group, label)


@animation((1920, 1080), render_bg=1, bg=DB_BLACK, timeline=at)
def alternates_g(f):
    main = StSt(
        "g",
        name,
        900,
        opsz=1,
        wght=at.kf("eleo")["wght"],
        fill=DB_LIGHT_GREEN,
    )

    alternate = StSt(
        "g",
        name,
        900,
        opsz=1,
        wght=at.kf("eleo")["wght"],
        features={"ss08": True},
        fill=DB_LIGHT_GREEN,
    )

    label = StSt(
        "At Name Sans",
        supreme,
        50,
        tu=-40,
        fill=DB_DARK_GREEN,
    ).align(f.a.r.inset(80), y="mny")

    group = PS(main, alternate).spread(tracking=400).align(f.a.r).translate(x=0, y=150)

    return (group, label)
