import sys
import numpy as np

sys.path.insert(1, "utils/")

from design_bits_system import *

from coldtype import *
from coldtype.warping import warp

factor = 20
length = 26
tl = Timeline(length * factor, fps=60)

font = Font.Cacheable("~/fonts/variable/Mona-Sans.ttf")


midi = MidiTimeline(__sibling__("midi/alphabet.mid"), bpm=177, fps=60)

ar = {
    "KD": [4, 8],
    "CW": [15, 75],
    "HT": [10, 10],
    "RS": [5, 5],
    "SD": [3, 90],
    "TM": [5, 10],
}


@animation(
    rect=(1000, 1000),
    timeline=midi,
    composites=1,
    bg=DB_BLACK,
)
def alphabet(f):
    drums = f.t

    snare = drums.ki(37)
    snare_v, si = snare.adsr(ar["SD"], find=1)

    kick = drums.ki(36)

    return [
        # P(f.a.r.inset(70))
        # .fssw(-1, DB_LIGHT_GREEN, 2, 1)
        # .ch(warp(f.i * 30, f.i, mult=100)),
        P(
            StSt(
                chr(60 + si),
                font,
                400 if si % 2 == 0 else 600,
                wdth=f.e("qeio", 3),
                wght=1 - snare_v,
                ro=1,
            )
            .scale(scaleX=1, scaleY=kick.adsr(ar["KD"], rng=(0.95, 1)))
            .fssw(-1, DB_LIGHT_GREEN, 2)
            .align(f.a.r, tx=1)
        )
        .insert(0, f.last_render())
        .insert(1, P(f.a.r).f(DB_BLACK, 0.1)),
    ]


def release(passes):
    FFMPEGExport(alphabet, passes).h264().write().open()
