from manim import *

BG = "#101216"
FG = "#e8eaf0"
MUT = "#a0a7b8"
ARANCIO = "#fb923c"
BLU = "#7aa2ff"
VERDE = "#34d399"
GIALLO = "#fbbf24"
ROSA = "#f472b6"

config.background_color = BG


def domanda_seno(font_size=40):
    m = MathTex(r"1.\ \text{Perché }", r"\sin\theta", r"=\dfrac{\sqrt{n}}{2}", r"\text{ ?}",
                font_size=font_size, color=FG)
    m[1].set_color(ARANCIO)
    return m


def domanda_salti(font_size=40):
    m = MathTex(r"2.\ \text{Perché i salti di }", r"\theta", r"\text{ sono }",
                r"30^\circ,15^\circ,15^\circ,30^\circ", r"\text{ se }", r"n", r"\text{ sale di }1\text{ ?}",
                font_size=font_size, color=FG)
    m[1].set_color(GIALLO)
    m[3].set_color(GIALLO)
    m[5].set_color(VERDE)
    return m
