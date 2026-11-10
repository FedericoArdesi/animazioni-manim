import numpy as np
from common import *


class Scena01Tesi(Scene):
    """Titolo, tabella dei valori notevoli e formule di seno e coseno con n."""

    def construct(self):
        # Titolo d'apertura
        titolo = Tex("Seno e coseno degli angoli notevoli", font_size=60)
        titolo.set_color_by_gradient(ARANCIO, ROSA, BLU)
        sotto = Tex("dimostrazione illustrata", font_size=34, color=MUT)
        sotto.next_to(titolo, DOWN, buff=0.45)
        self.play(Write(titolo), run_time=2.5)
        self.play(FadeIn(sotto, shift=UP * 0.2), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(titolo, sotto), run_time=1)

        # Tabella dei valori notevoli: dati, misure, griglia
        angoli = [0, 30, 45, 60, 90]
        sin_v = [0, 1, 2, 3, 4]
        cos_v = [4, 3, 2, 1, 0]

        DX = 1.25
        DY = 0.9
        G = 0.3
        SPESSORE = 3

        LARG = 0.12
        ALT = 0.183
        SW = SPESSORE * 0.0087

        xs = [(i - 2) * DX for i in range(5)]
        Y_SIN, Y_COS = DY / 2, -DY / 2

        y_top = Y_SIN + ALT + G + SW
        y_v = Y_COS - ALT - G + SW
        y_frac = y_v - 2 * SW - G
        Y_ANG = y_top + SW + G + 0.8 * ALT
        Y_DUE = y_frac - SW - G - ALT

        x_t = xs[0] - LARG - G
        x_v = x_t - 0.15
        x_r = xs[-1] + LARG + G
        gancio_a = [x_v - 0.3, y_v + 0.4, 0]
        gancio_b = [x_v - 0.2, y_v + 0.5, 0]
        x_b0 = gancio_a[0] - 0.1

        sin_m = VGroup(*[MathTex(str(v)).move_to([x, Y_SIN, 0]) for v, x in zip(sin_v, xs)])
        cos_m = VGroup(*[MathTex(str(v)).move_to([x, Y_COS, 0]) for v, x in zip(cos_v, xs)])

        def angolo(a, x):
            cifre = MathTex(str(a)).scale(0.8).move_to([x, Y_ANG, 0])
            completo = MathTex(rf"{a}^\circ").scale(0.8).move_to([x, Y_ANG, 0])
            completo.align_to(cifre, LEFT)
            return completo
        angoli_m = VGroup(*[angolo(a, x) for a, x in zip(angoli, xs)])

        x_lab = np.array([gancio_a[0] - SW - G, 0, 0])
        lab_sin = MathTex(r"\sin").next_to(x_lab + UP * Y_SIN, LEFT, buff=0)
        lab_cos = MathTex(r"\cos").next_to(x_lab + UP * Y_COS, LEFT, buff=0)
        lab_sin.align_to(sin_m[0], DOWN)
        lab_cos.align_to(cos_m[0], DOWN)

        opzioni = {}
        if hasattr(LineJointType, "ROUND"):
            opzioni["joint_type"] = LineJointType.ROUND
        # Radice e linea di frazione disegnate a mano
        radice = VMobject(stroke_width=SPESSORE, **opzioni).set_points_as_corners([
            gancio_a,
            gancio_b,
            [x_v, y_v, 0],
            [x_t, y_top, 0],
            [x_r, y_top, 0],
        ])
        frazione = Line([x_b0, y_frac, 0], [x_r, y_frac, 0], stroke_width=SPESSORE)
        due = MathTex("2").move_to([(x_b0 + x_r) / 2, Y_DUE, 0])

        tutto = VGroup(angoli_m, sin_m, cos_m, radice, lab_sin, lab_cos,
                       frazione, due)
        tutto.move_to(ORIGIN)

        gruppo_angoli = AnimationGroup(*[Write(m) for m in angoli_m], lag_ratio=0.15)
        gruppo_label  = AnimationGroup(Write(lab_sin), Write(lab_cos), lag_ratio=0.2)
        gruppo_sin    = AnimationGroup(*[Write(m) for m in sin_m], lag_ratio=0.15)
        gruppo_cos    = AnimationGroup(*[Write(m) for m in cos_m], lag_ratio=0.15)
        gruppo_form   = AnimationGroup(Create(radice), Create(frazione), Write(due), lag_ratio=0.2)

        self.play(
            LaggedStart(
                gruppo_angoli,
                gruppo_label,
                gruppo_sin,
                gruppo_cos,
                gruppo_form,
                lag_ratio=0.35
            ),
            run_time=3.5
        )
        self.wait(1.5)

        # La tabella si rimpicciolisce in alto a sinistra
        SCALE = 0.55
        self.play(
            tutto.animate.scale(SCALE).to_corner(UL, buff=0.8).shift(DOWN*0.5),
            run_time=1.6,
        )
        self.wait(0.5)

        self.play(
            sin_m.animate.set_color(VERDE),
            lab_sin.animate.set_color(ARANCIO),
            run_time=1.2,
        )

        # Formula del seno e legenda n <-> angolo
        F_sin = MathTex(
            r"\sin\theta = \frac{\sqrt{",
            r"n",
            r"}}{2}",
            font_size=48,
        )
        F_sin[0].set_color(ARANCIO)
        F_sin[1].set_color(VERDE)
        F_sin[2].set_color(ARANCIO)

        relazione_n_angolo = MathTex(
            r"\begin{array}{c|ccccc}"
            r"n & 0 & 1 & 2 & 3 & 4 \\ \hline"
            r"\theta & 0^\circ & 30^\circ & 45^\circ & 60^\circ & 90^\circ"
            r"\end{array}",
            font_size=30,
            color=MUT,
        )
        relazione_n_angolo[0][:7].set_color(VERDE)

        relazione_n_angolo.to_corner(UR, buff=1.1).shift(DOWN*0.8)
        F_sin.move_to([-3.4, -1.25, 0])

        self.play(Write(relazione_n_angolo), run_time=1.7)
        self.wait(0.3)
        self.play(Write(F_sin), run_time=1.5)
        self.wait(1)

        self.play(lab_cos.animate.set_color(BLU), run_time=0.8)

        center_col = -2.8
        dx_dil = 1.12
        xs_new = [center_col + (k - 2) * dx_dil for k in range(5)]

        # Nel coseno gli stessi numeri compaiono come 4 - n
        def quattro_meno(k, x_pos, y_pos):
            p4 = MathTex(r"4", color=BLU).scale(SCALE)
            p_meno = MathTex(r"-", color=BLU).scale(SCALE)
            pk = MathTex(str(k), color=VERDE).scale(SCALE)
            return VGroup(p4, p_meno, pk).arrange(RIGHT, buff=0.06).move_to([x_pos, y_pos, 0])

        y_cos_curr = cos_m[0].get_center()[1]
        y_sin_curr = sin_m[0].get_center()[1]
        cos_targets = [quattro_meno(k, xs_new[k], y_cos_curr) for k in range(5)]

        PAD = 0.50
        x_roof_left = cos_targets[0].get_left()[0] - PAD
        x_roof_right = cos_targets[-1].get_right()[0] + PAD

        y_roof = radice.get_top()[1]
        y_vert = radice.get_bottom()[1]
        y_frac_curr = frazione.get_y()

        x_v_n = x_roof_left - 0.15 * SCALE
        gancio_a_n = [x_v_n - 0.3 * SCALE, y_vert + 0.4 * SCALE, 0]
        gancio_b_n = [x_v_n - 0.2 * SCALE, y_vert + 0.5 * SCALE, 0]
        x_frac_start = gancio_a_n[0] - 0.1 * SCALE
        x_lab_curr = gancio_a_n[0] - (SW + G) * SCALE

        radice_target = VMobject(stroke_width=radice.stroke_width, **opzioni).set_points_as_corners([
            gancio_a_n,
            gancio_b_n,
            [x_v_n, y_vert, 0],
            [x_roof_left, y_roof, 0],
            [x_roof_right, y_roof, 0],
        ])
        frazione_target = Line(
            [x_frac_start, y_frac_curr, 0],
            [x_roof_right, y_frac_curr, 0],
            stroke_width=frazione.stroke_width,
        )
        due_target = due.copy().move_to([
            (x_frac_start + x_roof_right) / 2,
            due.get_y(),
            0,
        ])
        lab_sin_target = lab_sin.copy().next_to([x_lab_curr, y_sin_curr, 0], LEFT, buff=0)
        lab_cos_target = lab_cos.copy().next_to([x_lab_curr, y_cos_curr, 0], LEFT, buff=0)
        lab_sin_target.align_to(sin_m[0], DOWN)
        lab_cos_target.align_to(cos_m[0], DOWN)

        dxs = [x_n - s.get_center()[0] for x_n, s in zip(xs_new, sin_m)]

        self.play(
            Transform(radice, radice_target),
            Transform(frazione, frazione_target),
            Transform(due, due_target),
            Transform(lab_sin, lab_sin_target),
            Transform(lab_cos, lab_cos_target),
            LaggedStart(
                *[m.animate.set_x(x_n) for m, x_n in zip(sin_m, xs_new)],
                lag_ratio=0.04,
            ),
            LaggedStart(
                *[m.animate.set_x(x_n) for m, x_n in zip(cos_m, xs_new)],
                lag_ratio=0.04,
            ),
            LaggedStart(
                *[m.animate.shift(dx * RIGHT) for m, dx in zip(angoli_m, dxs)],
                lag_ratio=0.04,
            ),
            run_time=0.85,
        )

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        Transform(m, tgt[0]),
                        TransformFromCopy(s, tgt[2], path_arc=-0.25),
                        FadeIn(tgt[1], scale=0.5),
                    )
                    for m, s, tgt in zip(cos_m, sin_m, cos_targets)
                ],
                lag_ratio=0.25,
            ),
            run_time=1.1,
        )

        self.wait(0.6)

        # Formula del coseno
        F_cos = MathTex(
            r"\cos\theta = \frac{\sqrt{",
            r"4-",
            r"n",
            r"}}{2}",
            font_size=48,
        )
        F_cos[0].set_color(BLU)
        F_cos[1].set_color(BLU)
        F_cos[2].set_color(VERDE)
        F_cos[3].set_color(BLU)

        F_cos.move_to([3.4, -1.25, 0])

        self.play(Write(F_cos), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(*self.mobjects))
        self.wait(1)