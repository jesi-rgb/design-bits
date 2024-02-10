import sys

sys.path.insert(1, "utils/")

import numpy as np
from coldtype import *
from design_bits_system import *


name = Font.Cacheable("~/fonts/variable/NameSans.ttf")


@animation((1920, 1080), timeline=Timeline(500, 60), render_bg=1, bg=DB_BLACK)
def weight_range(f):

    copies = 20
    weights = np.linspace(0, 1, copies, endpoint=True)
    opszs = np.linspace(0, 1, copies, endpoint=True)

    print(weights)

    gs = (
        PS(
            [
                StSt(
                    "g",
                    name,
                    150,
                    opsz=0.9,
                    wght=w,
                    features={"ss08": True},
                    fill=DB_LIGHT_GREEN,
                )
                for w, o in zip(weights, opszs)
            ]
        )
        .spread(tracking=1)
        .align(f.a.r)
    )

    return gs
