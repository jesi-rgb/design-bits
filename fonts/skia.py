import sys

sys.path.insert(1, "utils/")

from design_bits_system import *

from coldtype import *

skia = Font.Cacheable("~/fonts/variable/Skia.ttf")


@animation((1920, 1080), render_bg=1, bg=DB_BLACK)
def scratch(f):
    text = "yolo"
    return StSt("Skia", skia, 200)
