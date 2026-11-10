from manim import *
from palette import *


def fit(mob, max_width):
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


class Scene07Differenza(Scene):
    def construct(self):
        self.camera.background_color = BG

        # --- Titolo in alto ---
        title = Tex("Formule di sottrazione", font_size=44, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.2)
        self.wait(0.5)

        # Altezze delle righe
        Y_A, Y_B, Y_D, Y_RULES = 1.7, 0.4, -1.0, -2.7

        # =====================================================
        # Regole di parita': restano in basso per tutta la scena
        # =====================================================
        rule_cos = fm(r"\cos", r"(", r"-", r"\beta", r")", r"=", r"\cos", r"\beta",
                      font_size=40)
        rule_sin = fm(r"\sin", r"(", r"-", r"\beta", r")", r"=", r"-", r"\sin", r"\beta",
                      font_size=40)
        rules = VGroup(rule_cos, rule_sin).arrange(RIGHT, buff=1.4)
        rules_intro = Tex("Ricordiamo che", font_size=30, color=MUTED)
        rules_all = VGroup(rules_intro, rules).arrange(DOWN, buff=0.25)
        rules_all.move_to(np.array([0.0, Y_RULES, 0.0]))

        def place(mob, y):
            fit(mob, 12.0)
            mob.move_to(np.array([0.0, y, 0.0]))
            return mob

        # =====================================================
        # COSENO
        # =====================================================
        # cos(a - b) = cos(a + (-b))
        c_a = place(fm(
            r"\cos", r"(", r"\alpha", r"-", r"\beta", r")", r"=",
            r"\cos", r"(", r"\alpha", r"+", r"(", r"-", r"\beta", r")", r")",
            font_size=48,
        ), Y_A)

        # formula di somma con beta -> -beta
        c_b = place(fm(
            r"=", r"\cos", r"\alpha", r"\cdot", r"\cos", r"(", r"-", r"\beta", r")",
            r"-", r"\sin", r"\alpha", r"\cdot", r"\sin", r"(", r"-", r"\beta", r")",
            font_size=48,
        ), Y_B)

        # risultato
        c_d = place(fm(
            r"=", r"\cos", r"\alpha", r"\cdot", r"\cos", r"\beta",
            r"+", r"\sin", r"\alpha", r"\cdot", r"\sin", r"\beta",
            font_size=48,
        ), Y_D)
        c_box = SurroundingRectangle(c_d, color=UNIT_COLOR, buff=0.25, stroke_width=3)

        self.play(Write(c_a), run_time=2.2)
        self.wait(0.8)
        self.play(Write(c_b), run_time=2.5)
        self.wait(0.8)
        self.play(FadeIn(rules_all, shift=UP * 0.2), run_time=1.0)
        self.wait(1.0)
        self.play(Write(c_d), run_time=2.2)
        self.play(Create(c_box), run_time=0.8)
        self.wait(2.0)

        self.play(FadeOut(VGroup(c_a, c_b, c_d, c_box)), run_time=0.8)
        self.wait(0.3)

        # =====================================================
        # SENO
        # =====================================================
        s_a = place(fm(
            r"\sin", r"(", r"\alpha", r"-", r"\beta", r")", r"=",
            r"\sin", r"(", r"\alpha", r"+", r"(", r"-", r"\beta", r")", r")",
            font_size=48,
        ), Y_A)

        s_b = place(fm(
            r"=", r"\sin", r"\alpha", r"\cdot", r"\cos", r"(", r"-", r"\beta", r")",
            r"+", r"\cos", r"\alpha", r"\cdot", r"\sin", r"(", r"-", r"\beta", r")",
            font_size=48,
        ), Y_B)

        s_d = place(fm(
            r"=", r"\sin", r"\alpha", r"\cdot", r"\cos", r"\beta",
            r"-", r"\cos", r"\alpha", r"\cdot", r"\sin", r"\beta",
            font_size=48,
        ), Y_D)
        s_box = SurroundingRectangle(s_d, color=UNIT_COLOR, buff=0.25, stroke_width=3)

        self.play(Write(s_a), run_time=2.2)
        self.wait(0.8)
        self.play(Write(s_b), run_time=2.5)
        self.wait(1.0)
        self.play(
            Indicate(rules, color=UNIT_COLOR, scale_factor=1.1),
            run_time=1.2,
        )
        self.play(Write(s_d), run_time=2.2)
        self.play(Create(s_box), run_time=0.8)
        self.wait(2.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
