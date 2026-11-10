from manim import *
from palette import *

ALPHA = 25 * DEGREES
BETA = 40 * DEGREES
R = 5.2

SPEED = 5.0


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


class Scene05Rettangolo(Scene):
    def construct(self):
        self.camera.background_color = BG

        O = np.array([-5.2, -2.5, 0.0])
        P = O + R * unit(ALPHA + BETA)
        F = O + R * np.cos(BETA) * unit(ALPHA)
        G = np.array([F[0], O[1], 0.0])
        TL = np.array([O[0], P[1], 0.0])
        TR = np.array([F[0], P[1], 0.0])

        hyp = Line(O, P, color=UNIT_COLOR, stroke_width=6)
        leg_cos = Line(O, F, color=MUTED, stroke_width=2.5)
        leg_sin = Line(F, P, color=MUTED, stroke_width=2.5)

        s = 0.3
        right = VMobject(color=MUTED, stroke_width=2.5)
        right.set_points_as_corners([
            F - s * unit(ALPHA),
            F - s * unit(ALPHA) + s * unit(ALPHA + PI / 2),
            F + s * unit(ALPHA + PI / 2),
        ])

        sector_alpha = Sector(
            radius=1.1, angle=ALPHA, start_angle=0, arc_center=O,
            color=ALPHA_COLOR, fill_opacity=0.5, stroke_width=0,
        )
        sector_beta = Sector(
            radius=1.1, angle=BETA, start_angle=ALPHA, arc_center=O,
            color=BETA_COLOR, fill_opacity=0.5, stroke_width=0,
        )
        alpha_lab = fm(r"\alpha", font_size=40)
        alpha_lab.move_to(O + 1.7 * unit(ALPHA / 2))
        beta_lab = fm(r"\beta", font_size=40)
        beta_lab.move_to(O + 1.7 * unit(ALPHA + BETA / 2))

        drop = DashedLine(F, G, color=MUTED, stroke_width=2.5)
        dot = Dot(P, radius=0.1, color=UNIT_COLOR)
        bottom = Line(O, G, color=MUTED, stroke_width=2.5)

        axis_x = Line(O + LEFT * 0.3, O + RIGHT * (R + 0.3), color=MUTED, stroke_width=1.5)
        axis_y = Line(O + DOWN * 0.3, O + UP * (R + 0.15), color=MUTED, stroke_width=1.5)
        quarter = DashedVMobject(
            Arc(radius=R, start_angle=0, angle=PI / 2, arc_center=O,
                color=MUTED, stroke_width=2),
            num_dashes=50,
        )
        ring = Circle(radius=0.25, color=UNIT_COLOR, stroke_width=3).move_to(P)
        coords = fm(
            r"(", r"\cos", r"(", r"\alpha", r"+", r"\beta", r")",
            r",",
            r"\sin", r"(", r"\alpha", r"+", r"\beta", r")", r")",
            font_size=40,
        )
        coords.next_to(P, UP + RIGHT, buff=0.15)

        self.add(
            axis_x, axis_y, quarter,
            sector_alpha, sector_beta,
            bottom, leg_cos, leg_sin, right, drop, hyp,
            alpha_lab, beta_lab, dot, ring, coords,
        )
        self.wait(0.8)

        self.play(
            FadeOut(VGroup(axis_x, axis_y, quarter, ring, coords, dot)),
            run_time=1.0,
        )
        self.wait(0.3)

        pts = [G, F, TR, P, TL, O]
        perimetro = VMobject(color=MUTED, stroke_width=2.5)
        perimetro.set_points_as_corners(pts)
        lunghezza = sum(np.linalg.norm(b - a) for a, b in zip(pts[:-1], pts[1:]))

        self.play(FadeOut(drop), run_time=0.4)
        self.play(
            Create(perimetro, rate_func=linear),
            run_time=lunghezza / SPEED,
        )
        self.bring_to_front(hyp)
        self.wait(0.5)

        # Numerazione dei lati 1...6
        sides = [
            (O, TL, LEFT * 0.4),
            (TL, P, UP * 0.4),
            (O, G, DOWN * 0.4),
            (G, F, RIGHT * 0.4),
            (F, TR, RIGHT * 0.4),
            (P, TR, UP * 0.4),
        ]
        nums = VGroup()
        for i, (a, b, off) in enumerate(sides):
            num = MathTex(str(i + 1), color=NEUTRAL, font_size=38)
            num.move_to((a + b) / 2 + off)
            nums.add(num)
            self.play(
                *ray(a, b, run_time=0.9),
                FadeIn(num, scale=0.8, run_time=0.6),
            )
        self.wait(1.5)

        # Angoli alterni interni
        title = Tex("Angoli alterni interni", font_size=40, color=WHITE)
        fit(title, 5.4)
        title.move_to(np.array([3.2, 3.0, 0.0]))
        self.play(Write(title), run_time=1.2)

        note1 = VGroup(
            Tex("Il lato superiore e quello inferiore", font_size=30, color=NEUTRAL),
            Tex("sono paralleli: l'ipotenusa li taglia.", font_size=30, color=NEUTRAL),
        ).arrange(DOWN, buff=0.15)
        fit(note1, 5.4)
        note1.move_to(np.array([3.2, 1.6, 0.0]))
        self.play(FadeIn(note1, shift=UP * 0.2), run_time=0.8)

        self.play(*ray(TL, TR, run_time=1.4), *ray(O, G, run_time=1.4))
        self.wait(0.5)

        self.play(
            Indicate(sector_alpha, color=ALPHA_COLOR, scale_factor=1.15),
            Indicate(sector_beta, color=BETA_COLOR, scale_factor=1.15),
            run_time=1.2,
        )
        self.wait(0.5)

        sec_a = Sector(
            radius=1.0, angle=ALPHA, start_angle=PI, arc_center=P,
            color=ALPHA_COLOR, fill_opacity=0.5, stroke_width=0,
        )
        sec_b = Sector(
            radius=1.0, angle=BETA, start_angle=PI + ALPHA, arc_center=P,
            color=BETA_COLOR, fill_opacity=0.5, stroke_width=0,
        )
        lab_a = fm(r"\alpha", font_size=32)
        lab_a.move_to(P + 1.6 * unit(PI + ALPHA / 2))
        lab_b = fm(r"\beta", font_size=32)
        lab_b.move_to(P + 1.5 * unit(PI + ALPHA + BETA / 2))

        self.play(FadeIn(sec_a), run_time=0.8)
        self.play(Write(lab_a), run_time=0.5)
        self.play(FadeIn(sec_b), run_time=0.8)
        self.play(Write(lab_b), run_time=0.5)
        self.bring_to_front(hyp)
        self.wait(0.5)

        note2 = VGroup(
            Tex("In $P$ l'angolo è", font_size=30, color=NEUTRAL),
            fm(r"\alpha", r"+", r"\beta", font_size=36),
        ).arrange(RIGHT, buff=0.25)
        note2.move_to(np.array([3.2, 0.1, 0.0]))
        self.play(FadeIn(note2, shift=UP * 0.2), run_time=0.8)
        self.wait(2.5)

        # Sfumano insieme note e numeri per raccordarsi perfettamente con Scena 6
        self.play(FadeOut(VGroup(title, note1, note2, nums)), run_time=1.0)
        self.wait(0.5)