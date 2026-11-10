"""Palette condivisa da tutte le scene. Sfondo nero."""
from manim import *

BG = "#000000"

COS_COLOR = "#4DA3FF"    # azzurro vivo (cos)
SIN_COLOR = "#FF5A5F"    # corallo (sin)
ALPHA_COLOR = "#2EE6D6"  # turchese (alpha)
BETA_COLOR = "#FF6EC7"   # rosa/magenta (beta)
UNIT_COLOR = "#FFD84D"   # giallo caldo (ipotenusa = 1, evidenziazioni)
NEUTRAL = "#E8E8E8"      # testi e segni +, -, =
MUTED = "#8A9099"        # note, linee sottili

COLOR_MAP = {
    r"\cos": COS_COLOR,
    r"\sin": SIN_COLOR,
    r"\alpha": ALPHA_COLOR,
    r"\beta": BETA_COLOR,
}


def fm(*parts, **kwargs):
    """MathTex con i colori del progetto."""
    return MathTex(*parts, tex_to_color_map=COLOR_MAP, color=NEUTRAL, **kwargs)
