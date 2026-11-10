from manim import *
from palette import *

FS = 46  # corpo delle formule


def fit(mob, max_width):
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def make_row(fn, s_in, s_mid, t1, t2):
    """Una formula come riga di pezzi separati.
    Indici: 0 lhs-sinistra, 1 segno nella parentesi, 2 lhs-destra,
            3 uguale, 4 primo termine, 5 segno in mezzo, 6 secondo termine."""
    lhs_a = fm(fn, r"(", r"\alpha", font_size=FS)
    sg_in = MathTex(s_in, color=NEUTRAL, font_size=FS)
    lhs_b = fm(r"\beta", r")", font_size=FS)
    eq = MathTex("=", color=NEUTRAL, font_size=FS)
    term1 = fm(*t1, font_size=FS)
    sg_mid = MathTex(s_mid, color=NEUTRAL, font_size=FS)
    term2 = fm(*t2, font_size=FS)
    return VGroup(lhs_a, sg_in, lhs_b, eq, term1, sg_mid, term2).arrange(RIGHT, buff=0.15)


def sign_box(sign):
    return SurroundingRectangle(
        sign, color=UNIT_COLOR, buff=0.12, stroke_width=3, corner_radius=0.1,
    )


class Scene08Riepilogo(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Tex("Riepilogo", font_size=44, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.0)

        # =====================================================
        # Le quattro formule una sopra l'altra
        # =====================================================
        COSCOS = [r"\cos", r"\alpha", r"\cos", r"\beta"]
        SINSIN = [r"\sin", r"\alpha", r"\sin", r"\beta"]
        SINCOS = [r"\sin", r"\alpha", r"\cos", r"\beta"]
        COSSIN = [r"\cos", r"\alpha", r"\sin", r"\beta"]

        rows = [
            make_row(r"\cos", "+", "-", COSCOS, SINSIN),
            make_row(r"\cos", "-", "+", COSCOS, SINSIN),
            make_row(r"\sin", "+", "+", SINCOS, COSSIN),
            make_row(r"\sin", "-", "-", SINCOS, COSSIN),
        ]
        group = VGroup(*rows).arrange(DOWN, buff=0.55)

        # allinea i segni di uguale
        ref = rows[0][3].get_x()
        for r in rows:
            r.shift(RIGHT * (ref - r[3].get_x()))

        # un po' piu' di aria tra coseno e seno
        VGroup(rows[2], rows[3]).shift(DOWN * 0.4)

        fit(group, 9.0)
        group.move_to(np.array([-1.6, -0.2, 0.0]))

        for r in rows:
            self.play(Write(r), run_time=2.0)
            self.wait(0.4)
        self.wait(1.0)

        # =====================================================
        # Riquadri gialli sui segni
        # coseno: segni opposti; seno: segni uguali
        # =====================================================
        cos_boxes = VGroup(
            sign_box(rows[0][1]), sign_box(rows[0][5]),
            sign_box(rows[1][1]), sign_box(rows[1][5]),
        )
        sin_boxes = VGroup(
            sign_box(rows[2][1]), sign_box(rows[2][5]),
            sign_box(rows[3][1]), sign_box(rows[3][5]),
        )

        lab_cos = Tex("segni opposti", font_size=34, color=UNIT_COLOR)
        lab_cos.next_to(VGroup(rows[0], rows[1]), RIGHT, buff=0.6)
        lab_sin = Tex("segni uguali", font_size=34, color=UNIT_COLOR)
        lab_sin.next_to(VGroup(rows[2], rows[3]), RIGHT, buff=0.6)

        self.play(LaggedStart(*[Create(b) for b in cos_boxes], lag_ratio=0.25), run_time=1.8)
        self.play(FadeIn(lab_cos, shift=LEFT * 0.2), run_time=0.7)
        self.wait(1.5)
        self.play(LaggedStart(*[Create(b) for b in sin_boxes], lag_ratio=0.25), run_time=1.8)
        self.play(FadeIn(lab_sin, shift=LEFT * 0.2), run_time=0.7)
        self.wait(2.0)

        self.play(
            FadeOut(VGroup(group, cos_boxes, sin_boxes, lab_cos, lab_sin)),
            run_time=1.0,
        )
        self.wait(0.3)

        # =====================================================
        # Forma compatta con ± e ∓ cerchiati
        # =====================================================
        cos_c = make_row(r"\cos", r"\pm", r"\mp", COSCOS, SINSIN)
        sin_c = make_row(r"\sin", r"\pm", r"\pm", SINCOS, COSSIN)
        compact = VGroup(cos_c, sin_c).arrange(DOWN, buff=1.0)
        ref = cos_c[3].get_x()
        sin_c.shift(RIGHT * (ref - sin_c[3].get_x()))
        fit(compact, 11.0)
        compact.move_to(np.array([0.0, 0.2, 0.0]))

        def ring(sign):
            return Circle(radius=0.4, color=UNIT_COLOR, stroke_width=3).move_to(sign)

        rings = VGroup(
            ring(cos_c[1]), ring(cos_c[5]),
            ring(sin_c[1]), ring(sin_c[5]),
        )

        self.play(Write(cos_c), run_time=2.2)
        self.wait(0.4)
        self.play(Write(sin_c), run_time=2.2)
        self.wait(0.8)
        self.play(LaggedStart(*[Create(c) for c in rings], lag_ratio=0.3), run_time=1.8)
        self.wait(1.0)
        self.play(FadeOut(c) for c in rings)

        note = Tex(
            r"Valide per qualsiasi coppia di angoli $\alpha$ e $\beta$",
            font_size=30, color=MUTED,
        ).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.2)
