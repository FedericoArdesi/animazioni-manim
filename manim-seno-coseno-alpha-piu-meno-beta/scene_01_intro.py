from manim import *
from palette import *


class Scene01Intro(Scene):
    def construct(self):
        self.camera.background_color = BG

        # --- Titolo: posizione finale (in alto, bianco) ---
        title_small = Tex(
            r"Formule di addizione e sottrazione \\ del seno e del coseno",
            font_size=44, color=WHITE,
        )
        title_small.to_edge(UP, buff=0.5)

        # --- Titolo: versione grande al centro, con gradiente ---
        title = title_small.copy().scale_to_fit_width(12).move_to(ORIGIN)
        title.set_color_by_gradient(ALPHA_COLOR, COS_COLOR, BETA_COLOR)

        self.play(Write(title), run_time=2.5)
        self.wait(1)

        # Il titolo sale, si rimpicciolisce e diventa bianco
        self.play(Transform(title, title_small), run_time=1.5)
        self.wait(0.5)

        # --- Formule al centro dello schermo ---
        cos_f = fm(
            r"\cos(", r"\alpha", r"\pm", r"\beta", r")", r"=",
            r"\cos", r"\alpha", r"\cdot", r"\cos", r"\beta",
            r"\mp",
            r"\sin", r"\alpha", r"\cdot", r"\sin", r"\beta",
            font_size=54,
        )
        sin_f = fm(
            r"\sin(", r"\alpha", r"\pm", r"\beta", r")", r"=",
            r"\sin", r"\alpha", r"\cdot", r"\cos", r"\beta",
            r"\pm",
            r"\cos", r"\alpha", r"\cdot", r"\sin", r"\beta",
            font_size=54,
        )
        formulas = VGroup(cos_f, sin_f).arrange(DOWN, buff=0.9).move_to(ORIGIN)

        self.play(Write(cos_f), run_time=2.5)
        self.wait(0.5)
        self.play(Write(sin_f), run_time=2.5)
        self.wait(1)

        note = Tex(
            r"Il segno superiore con il superiore, quello inferiore con l'inferiore",
            font_size=28, color=MUTED,
        ).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(VGroup(title, formulas, note)))