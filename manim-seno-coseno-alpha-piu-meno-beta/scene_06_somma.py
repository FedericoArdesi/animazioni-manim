from manim import *
from palette import *

ALPHA = 25 * DEGREES
BETA = 40 * DEGREES
R = 5.2


def unit(ang):
    return np.array([np.cos(ang), np.sin(ang), 0.0])


def fit(mob, max_width):
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def ray(a, b, run_time=0.9):
    glow = Line(a, b, color=UNIT_COLOR, stroke_width=14, stroke_opacity=0.3)
    core = Line(a, b, color=UNIT_COLOR, stroke_width=6)
    return [
        ShowPassingFlash(glow, time_width=0.4, rate_func=linear, run_time=run_time),
        ShowPassingFlash(core, time_width=0.4, rate_func=linear, run_time=run_time),
    ]


def row(*mobs, buff=0.18):
    return VGroup(*mobs).arrange(RIGHT, buff=buff)


class Scene06Somma(Scene):
    def construct(self):
        self.camera.background_color = BG

        O = np.array([-5.2, -2.5, 0.0])
        P = O + R * unit(ALPHA + BETA)
        F = O + R * np.cos(BETA) * unit(ALPHA)
        G = np.array([F[0], O[1], 0.0])
        TL = np.array([O[0], P[1], 0.0])
        TR = np.array([F[0], P[1], 0.0])

        rect = VMobject(color=MUTED, stroke_width=2.5)
        rect.set_points_as_corners([O, G, TR, TL, O])
        leg_cos = Line(O, F, color=MUTED, stroke_width=2.5)
        leg_sin = Line(F, P, color=MUTED, stroke_width=2.5)
        hyp = Line(O, P, color=UNIT_COLOR, stroke_width=6)

        s = 0.3
        right = VMobject(color=MUTED, stroke_width=2.5)
        right.set_points_as_corners([
            F - s * unit(ALPHA),
            F - s * unit(ALPHA) + s * unit(ALPHA + PI / 2),
            F + s * unit(ALPHA + PI / 2),
        ])

        sec_a_o = Sector(radius=1.1, angle=ALPHA, start_angle=0, arc_center=O,
                         color=ALPHA_COLOR, fill_opacity=0.5, stroke_width=0)
        sec_b_o = Sector(radius=1.1, angle=BETA, start_angle=ALPHA, arc_center=O,
                         color=BETA_COLOR, fill_opacity=0.5, stroke_width=0)
        lab_a_o = fm(r"\alpha", font_size=40).move_to(O + 1.7 * unit(ALPHA / 2))
        lab_b_o = fm(r"\beta", font_size=40).move_to(O + 1.7 * unit(ALPHA + BETA / 2))

        sec_a_p = Sector(radius=1.0, angle=ALPHA, start_angle=PI, arc_center=P,
                         color=ALPHA_COLOR, fill_opacity=0.5, stroke_width=0)
        sec_b_p = Sector(radius=1.0, angle=BETA, start_angle=PI + ALPHA, arc_center=P,
                         color=BETA_COLOR, fill_opacity=0.5, stroke_width=0)
        lab_a_p = fm(r"\alpha", font_size=32).move_to(P + 1.6 * unit(PI + ALPHA / 2))
        lab_b_p = fm(r"\beta", font_size=32).move_to(P + 1.5 * unit(PI + ALPHA + BETA / 2))

        self.add(
            sec_a_o, sec_b_o, sec_a_p, sec_b_p,
            rect, leg_cos, leg_sin, right, hyp,
            lab_a_o, lab_b_o, lab_a_p, lab_b_p,
        )
        self.wait(0.8)

        def vlabel(parts, pos, fs=30):
            lab = fm(*parts, font_size=fs)
            lab.rotate(PI / 2)
            lab.move_to(pos)
            return lab

        # 1. Ipotenusa unitaria
        one_lab = MathTex("1", color=UNIT_COLOR, font_size=48)
        norm_hyp = np.array([-np.sin(ALPHA + BETA), np.cos(ALPHA + BETA), 0])
        one_lab.move_to((O + P) / 2 + 0.45 * norm_hyp)

        self.play(
            *ray(O, P, run_time=0.9),
            Write(one_lab, run_time=0.6),
        )
        self.wait(0.4)

        # 2. Coordinate dirette: sin(alpha + beta) e cos(alpha + beta)
        lab_left = vlabel([r"\sin", r"(", r"\alpha", r"+", r"\beta", r")"],
                          (O + TL) / 2 + LEFT * 0.55, fs=32)
        lab_top_l = fm(r"\cos", r"(", r"\alpha", r"+", r"\beta", r")", font_size=30)
        lab_top_l.move_to((TL + P) / 2 + UP * 0.45)

        self.play(*ray(O, TL, run_time=0.8), Write(lab_left, run_time=0.9))
        self.wait(0.2)
        self.play(*ray(TL, P, run_time=0.8), Write(lab_top_l, run_time=0.9))
        self.wait(0.6)

        # 3. Spiegazione dei cateti intermedi cos(beta) e sin(beta)
        norm_OF = np.array([-np.sin(ALPHA), np.cos(ALPHA), 0])
        mid_OF = (O + F) / 2
        lab_cos_b = fm(r"\cos", r"\beta", font_size=32).rotate(ALPHA)
        lab_cos_b.move_to(mid_OF + 0.35 * norm_OF)

        mid_FP = (F + P) / 2
        lab_sin_b = fm(r"\sin", r"\beta", font_size=32).rotate(ALPHA - PI / 2)
        lab_sin_b.move_to(mid_FP + 0.42 * (-unit(ALPHA)))

        self.play(*ray(O, F, run_time=0.8), FadeIn(lab_cos_b, shift=norm_OF * 0.2))
        self.wait(0.2)
        self.play(*ray(F, P, run_time=0.8), FadeIn(lab_sin_b, shift=(-unit(ALPHA)) * 0.2))
        self.wait(0.6)

        # 4. Triangolo inferiore (ipotenusa cos beta, angolo alpha)
        tri_low = Polygon(O, G, F, color=COS_COLOR, fill_opacity=0.25, stroke_width=0)
        self.play(FadeIn(tri_low), run_time=0.7)
        self.wait(0.3)

        lab_bottom = fm(r"\cos", r"\alpha", r"\cdot", r"\cos", r"\beta", font_size=30)
        lab_bottom.move_to((O + G) / 2 + DOWN * 0.45)
        lab_r_low = vlabel([r"\sin", r"\alpha", r"\cdot", r"\cos", r"\beta"],
                           (G + F) / 2 + RIGHT * 0.5, fs=28)

        self.play(*ray(O, G, run_time=0.8), Write(lab_bottom, run_time=0.9))
        self.wait(0.2)
        self.play(*ray(G, F, run_time=0.8), Write(lab_r_low, run_time=0.9))
        self.wait(0.5)

        # 5. Triangolo superiore (ipotenusa sin beta, angolo alpha)
        tri_up = Polygon(F, TR, P, color=SIN_COLOR, fill_opacity=0.25, stroke_width=0)
        self.play(FadeIn(tri_up), run_time=0.7)
        self.wait(0.3)

        sec_a_f = Sector(radius=0.9, angle=ALPHA, start_angle=PI / 2, arc_center=F,
                         color=ALPHA_COLOR, fill_opacity=0.5, stroke_width=0)
        lab_a_f = fm(r"\alpha", font_size=30).move_to(F + 1.4 * unit(PI / 2 + ALPHA / 2))
        self.play(FadeIn(sec_a_f), Write(lab_a_f), run_time=0.7)
        self.wait(0.3)

        lab_r_up = vlabel([r"\cos", r"\alpha", r"\cdot", r"\sin", r"\beta"],
                          (F + TR) / 2 + RIGHT * 0.5, fs=28)
        lab_top_r = fm(r"\sin", r"\alpha", r"\cdot", r"\sin", r"\beta", font_size=28)
        lab_top_r.move_to((P + TR) / 2 + UP * 0.45)

        self.play(*ray(F, TR, run_time=0.8), Write(lab_r_up, run_time=0.9))
        self.wait(0.2)
        self.play(*ray(P, TR, run_time=0.8), Write(lab_top_r, run_time=0.9))
        self.wait(0.6)

        self.play(FadeOut(VGroup(tri_low, tri_up)), run_time=0.6)
        self.bring_to_front(hyp)

        # 6. Formule di somma
        eq1 = MathTex("=", color=NEUTRAL, font_size=40)
        sin_lhs = fm(r"\sin", r"(", r"\alpha", r"+", r"\beta", r")", font_size=40)
        sin_t1 = fm(r"\sin", r"\alpha", r"\cos", r"\beta", font_size=40)
        sin_plus = MathTex("+", color=NEUTRAL, font_size=40)
        sin_t2 = fm(r"\cos", r"\alpha", r"\sin", r"\beta", font_size=40)
        sin_row = row(sin_lhs, eq1, sin_t1, sin_plus, sin_t2)

        eq2 = MathTex("=", color=NEUTRAL, font_size=40)
        cos_lhs = fm(r"\cos", r"(", r"\alpha", r"+", r"\beta", r")", font_size=40)
        cos_t1 = fm(r"\cos", r"\alpha", r"\cos", r"\beta", font_size=40)
        cos_minus = MathTex("-", color=NEUTRAL, font_size=40)
        cos_t2 = fm(r"\sin", r"\alpha", r"\sin", r"\beta", font_size=40)
        cos_row = row(cos_lhs, eq2, cos_t1, cos_minus, cos_t2)

        formulas = VGroup(sin_row, cos_row).arrange(DOWN, buff=1.0)
        fit(formulas, 5.4)
        formulas.move_to(np.array([3.2, 0.0, 0.0]))

        def link(mob, side_lab, a, b):
            box = SurroundingRectangle(mob, color=UNIT_COLOR, buff=0.1, stroke_width=3)
            self.play(
                Create(box),
                *ray(a, b, run_time=1.0),
                Indicate(side_lab, color=UNIT_COLOR, scale_factor=1.15, run_time=1.0),
            )
            self.wait(0.3)
            self.play(FadeOut(box), run_time=0.3)

        self.play(Write(sin_row), run_time=2.2)
        self.wait(0.4)
        link(sin_lhs, lab_left, O, TL)
        link(sin_t1, lab_r_low, G, F)
        link(sin_t2, lab_r_up, F, TR)
        self.wait(0.6)

        self.play(Write(cos_row), run_time=2.2)
        self.wait(0.4)
        link(cos_lhs, lab_top_l, TL, P)
        link(cos_t1, lab_bottom, O, G)
        link(cos_t2, lab_top_r, P, TR)
        self.wait(2.5)

        # Transizione pulita verso Scena 7
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)