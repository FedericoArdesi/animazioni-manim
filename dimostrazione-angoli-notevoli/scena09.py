import numpy as np
from common import *


class Scena09Coseno(Scene):
    """Passo 6: il coseno segue dal seno con lo specchio a 45 gradi."""

    def construct(self):
        EASE = rate_functions.ease_in_out_cubic
        SMOOTH = rate_functions.ease_in_out_sine
        POP = rate_functions.ease_out_back

        C_COS = BLU
        C_SIN = ARANCIO
        C_N = VERDE
        C_ANG = GIALLO
        FS = 31

        R = 2.6
        C = np.array([-3.4, -0.2, 0.0])
        O = C.copy()
        TH = 38 * DEGREES

        def P(ang, r=R):
            return C + r * np.array([np.cos(ang), np.sin(ang), 0.0])

        def dirz(ang):
            return np.array([np.cos(ang), np.sin(ang), 0.0])

        A = P(0)

        def crea_testo_con_ombra(latex, font_size, color):
            t_ = MathTex(latex, font_size=font_size, color=color)
            t_.set_stroke(color=BLACK, width=2.4, opacity=0.95, background=True)
            return t_

        def pos_B(ang):
            return P(ang) + 0.38 * dirz(ang) + 0.12 * UP

        def angolo_retto(V, p1, p2, s=0.22, color=FG):
            u = (p1 - V) / np.linalg.norm(p1 - V)
            v = (p2 - V) / np.linalg.norm(p2 - V)
            return VMobject(color=color, stroke_width=3).set_points_as_corners(
                [V + s * u, V + s * u + s * v, V + s * v]
            )

        def seg(p, q, color, w):
            return VMobject(color=color, stroke_width=w).set_points_as_corners([p, q])

        # P a theta e Q a 90 - theta (specchio rispetto a y = x)
        def costruisci(t):
            p = P(t)
            q = P(PI / 2 - t)
            hp = np.array([p[0], C[1], 0.0])
            hq = np.array([C[0], q[1], 0.0])
            return dict(
                rP=seg(O, p, FG, 3),
                rQ=seg(O, q, FG, 3),
                sc=seg(O, hp, C_COS, 6),
                ss=seg(hp, p, C_SIN, 6),
                qc=seg(O, hq, C_COS, 6),
                qs=seg(hq, q, C_SIN, 6),
                dP=Dot(p, radius=0.07, color=FG).set_z_index(10),
                dQ=Dot(q, radius=0.07, color=FG).set_z_index(10),
            )

        step = R / 4
        x_min, x_max = C[0] - 5 * step, C[0] + 5 * step
        y_min, y_max = C[1] - 5 * step, C[1] + 5 * step

        linee_vert = VGroup(*[Line([C[0] + k * step, y_min, 0], [C[0] + k * step, y_max, 0]) for k in range(-4, 5)])
        linee_oriz = VGroup(*[Line([x_min, C[1] + k * step, 0], [x_max, C[1] + k * step, 0]) for k in range(-4, 5)])
        griglia = VGroup(linee_vert, linee_oriz).set_stroke(color=MUT, width=1, opacity=0.18)

        asse_x = Arrow([x_min - 0.1, C[1], 0], [x_max + 0.3, C[1], 0], buff=0,
                       color=MUT, stroke_width=2, tip_length=0.18)
        asse_y = Arrow([C[0], y_min - 0.1, 0], [C[0], y_max + 0.3, 0], buff=0,
                       color=MUT, stroke_width=2, tip_length=0.18)
        lab_x = MathTex(r"x", font_size=28, color=MUT).move_to([x_max + 0.3, C[1] - 0.3, 0])
        lab_y = MathTex(r"y", font_size=28, color=MUT).move_to([C[0] + 0.3, y_max + 0.3, 0])

        cerchio = Circle(radius=R, color=MUT, stroke_width=3).move_to(C)
        dot_O = Dot(O, radius=0.07, color=FG)
        dot_A = Dot(A, radius=0.07, color=FG).set_z_index(10)
        lab_O = MathTex(r"O", font_size=36, color=FG).next_to(dot_O, DL, buff=0.12)
        lab_A = MathTex(r"A", font_size=36, color=FG).next_to(dot_A, DR, buff=0.12)
        raggio_OA = Line(O, A, color=FG, stroke_width=3)

        self.add(
            griglia, asse_x, asse_y, lab_x, lab_y,
            cerchio, dot_O, lab_O, raggio_OA, dot_A, lab_A
        )
        self.wait(0.3)

        X_L = 0.75
        # Titolo
        titolo = MathTex(r"\text{Il }", r"\cos", r"\text{ segue dal }", r"\sin",
                         font_size=38, color=FG)
        titolo[1].set_color(C_COS)
        titolo[3].set_color(C_SIN)
        titolo.move_to([0, 3.55, 0]).align_to([X_L, 0, 0], LEFT)
        self.play(Write(titolo), run_time=0.8)
        self.wait(0.2)

        # P con cos e sin
        st = costruisci(TH)
        P_ = P(TH)
        Hp = np.array([P_[0], C[1], 0.0])
        lab_P = MathTex(r"P", font_size=36, color=FG).move_to(pos_B(TH))
        arco_t = Arc(radius=0.46, start_angle=0, angle=TH, arc_center=O,
                     color=C_ANG, stroke_width=3.2)
        lab_t = MathTex(r"\theta", font_size=26, color=C_ANG).move_to(P(TH / 2, 0.80))
        marca_Hp = angolo_retto(Hp, O, P_)
        lab_cos = crea_testo_con_ombra(r"\cos\theta", 26, C_COS).move_to(
            (O + Hp) / 2 + 0.36 * DOWN
        )
        lab_sin = crea_testo_con_ombra(r"\sin\theta", 26, C_SIN).move_to(
            (Hp + P_) / 2 + 0.45 * RIGHT
        )

        self.play(
            Create(st["rP"]), FadeIn(st["dP"], scale=0.5), Write(lab_P),
            Create(arco_t), Write(lab_t),
            run_time=0.9, rate_func=SMOOTH,
        )
        self.play(
            Create(st["sc"]), Create(st["ss"]), Create(marca_Hp),
            run_time=0.9, rate_func=SMOOTH,
        )
        self.play(Write(lab_cos), Write(lab_sin), run_time=0.8)
        self.wait(0.8)

        d45 = dirz(PI / 4)
        # Lo specchio a 45 gradi scambia x e y
        specchio = DashedLine(C - 3.0 * d45, C + 3.0 * d45, color=MUT, stroke_width=2,
                              stroke_opacity=0.7, dash_length=0.1)
        lab_45 = MathTex(r"45^\circ", font_size=26, color=MUT).move_to(C + 3.0 * d45 + 0.27 * UP + 0.4 * RIGHT)

        self.play(Create(specchio), Write(lab_45), run_time=0.8, rate_func=SMOOTH)

        copia = VGroup(st["rP"], st["sc"], st["ss"], st["dP"]).copy()
        self.add(copia)
        self.play(
            Rotate(copia, angle=PI, axis=np.array([1.0, 1.0, 0.0]), about_point=C),
            run_time=1.4, rate_func=EASE,
        )
        Q_ = P(PI / 2 - TH)
        Hq = np.array([C[0], Q_[1], 0.0])

        lab_Q = MathTex(r"Q", font_size=36, color=FG).move_to(pos_B(PI / 2 - TH))
        arco_c = Arc(radius=1.15, start_angle=0, angle=PI / 2 - TH, arc_center=O,
                     color=C_ANG, stroke_width=3.2)
        lab_c = MathTex(r"90^\circ-\theta", font_size=24, color=C_ANG).move_to(P((PI / 2 - TH) / 2, 1.62))
        lab_qc = crea_testo_con_ombra(r"\cos\theta", 26, C_COS).move_to(
            (O + Hq) / 2 + 0.55 * LEFT
        )
        lab_qs = crea_testo_con_ombra(r"\sin\theta", 26, C_SIN).move_to(
            (Hq + Q_) / 2 + 0.38 * UP
        )

        self.play(Write(lab_Q), Write(lab_qc), Write(lab_qs), run_time=0.8)
        self.play(Create(arco_c), Write(lab_c), run_time=0.8)
        self.wait(0.4)

        # cos(theta) = sin(90 - theta)
        f1 = MathTex(r"\cos\theta", r"=", r"\sin(90^\circ-\theta)", font_size=38, color=FG)
        f1[0].set_color(C_COS)
        f1[2].set_color(C_SIN)
        f1.move_to([0, 2.70, 0]).align_to([X_L, 0, 0], LEFT)

        self.play(Write(f1), run_time=1.0)
        self.play(
            Indicate(copia[1], color=C_COS, scale_factor=1.05),
            Indicate(lab_qc, color=C_COS, scale_factor=1.2),
            run_time=0.9,
        )
        self.wait(0.8)

        # La figura diventa viva: segue theta
        th = ValueTracker(TH)
        live = {k: always_redraw(lambda k=k: costruisci(th.get_value())[k]) for k in st}

        self.play(
            FadeOut(VGroup(arco_t, lab_t, marca_Hp, lab_cos, lab_sin,
                           lab_qc, lab_qs, arco_c, lab_c, lab_45)),
            run_time=0.6,
        )
        self.remove(*st.values(), copia, lab_P, lab_Q)
        live_P = always_redraw(lambda: MathTex(r"P", font_size=36, color=FG).move_to(pos_B(th.get_value())))
        live_Q = always_redraw(lambda: MathTex(r"Q", font_size=36, color=FG).move_to(pos_B(PI / 2 - th.get_value())))
        self.add(*live.values(), live_P, live_Q)
        self.wait(0.2)

        larg_lab = 1.20
        larg_col = 0.96
        x_start = 0.75
        y_top = 2.10
        h_row = 0.56
        y_h = [y_top - k * h_row for k in range(5)]
        ys_row = [(y_h[i] + y_h[i + 1]) / 2 for i in range(4)]
        x_div_lab = x_start + larg_lab
        x_lab_center = x_start + larg_lab / 2
        xs_col_center = [x_div_lab + larg_col * (k + 0.5) for k in range(5)]
        xs_div = [x_div_lab + larg_col * k for k in range(6)]

        # Tabella con n, theta, 90 - theta, cos(theta)
        scheletro = VGroup(
            Rectangle(width=larg_lab + 5 * larg_col, height=4 * h_row,
                      stroke_color=MUT, stroke_width=2.0, stroke_opacity=0.6, fill_opacity=0.0)
            .move_to([(x_start + xs_div[5]) / 2, (y_h[0] + y_h[4]) / 2, 0]),
            Line([x_div_lab, y_h[0], 0], [x_div_lab, y_h[4], 0], color=MUT, stroke_width=1.6, stroke_opacity=0.6),
            *[Line([x_start, y_h[i], 0], [xs_div[5], y_h[i], 0], color=MUT, stroke_width=1.0, stroke_opacity=0.3)
              for i in (1, 2, 3)],
            *[Line([xs_div[k], y_h[0], 0], [xs_div[k], y_h[4], 0], color=MUT, stroke_width=1.2, stroke_opacity=0.35)
              for k in (1, 2, 3, 4)],
        )

        lab_rn = MathTex(r"n", font_size=31, color=C_N).move_to([x_lab_center, ys_row[0], 0])
        lab_rth = MathTex(r"\theta", font_size=31, color=C_ANG).move_to([x_lab_center, ys_row[1], 0])
        lab_rc = MathTex(r"90^\circ-\theta", font_size=24, color=C_ANG).move_to([x_lab_center, ys_row[2], 0])
        lab_rcos = MathTex(r"\cos\theta", font_size=27, color=C_COS).move_to([x_lab_center, ys_row[3], 0])

        ang_th = [0, 30, 45, 60, 90]
        VAL_N = [r"0", r"1", r"2", r"3", r"4"]
        VAL_TH = [r"0^\circ", r"30^\circ", r"45^\circ", r"60^\circ", r"90^\circ"]
        VAL_C = [r"90^\circ", r"60^\circ", r"45^\circ", r"30^\circ", r"0^\circ"]
        VAL_COS = [r"1", r"\tfrac{\sqrt3}{2}", r"\tfrac{\sqrt2}{2}", r"\tfrac12", r"0"]

        cn = [MathTex(v, font_size=29, color=C_N).move_to([xs_col_center[k], ys_row[0], 0]) for k, v in enumerate(VAL_N)]
        cth = [MathTex(v, font_size=29, color=C_ANG).move_to([xs_col_center[k], ys_row[1], 0]) for k, v in enumerate(VAL_TH)]
        cc = [MathTex(v, font_size=29, color=C_ANG).move_to([xs_col_center[k], ys_row[2], 0]) for k, v in enumerate(VAL_C)]
        ccos = [MathTex(v, font_size=28, color=C_COS).move_to([xs_col_center[k], ys_row[3], 0]) for k, v in enumerate(VAL_COS)]

        cursore = Rectangle(width=larg_col, height=4 * h_row, stroke_width=0,
                            fill_color=FG, fill_opacity=0.07)
        cursore.move_to([xs_col_center[0], (y_h[0] + y_h[4]) / 2, 0])

        self.play(Create(scheletro), run_time=0.75)
        self.play(
            LaggedStart(Write(lab_rn), Write(lab_rth), Write(lab_rc), Write(lab_rcos), lag_ratio=0.15),
            run_time=0.75,
        )
        self.wait(0.2)

        self.play(
            FadeIn(cursore),
            th.animate(rate_func=EASE, run_time=0.8).set_value(0.0),
            GrowFromCenter(cn[0], rate_func=POP, run_time=0.5),
            GrowFromCenter(cth[0], rate_func=POP, run_time=0.5),
            GrowFromCenter(cc[0], rate_func=POP, run_time=0.5),
            GrowFromCenter(ccos[0], rate_func=POP, run_time=0.5),
        )
        self.wait(0.15)

        for k in range(1, 5):
            self.play(
                th.animate(rate_func=EASE, run_time=0.7).set_value(ang_th[k] * DEGREES),
                cursore.animate(run_time=0.5).set_x(xs_col_center[k]),
                GrowFromCenter(cn[k], rate_func=POP, run_time=0.5),
                GrowFromCenter(cth[k], rate_func=POP, run_time=0.5),
                GrowFromCenter(cc[k], rate_func=POP, run_time=0.5),
                GrowFromCenter(ccos[k], rate_func=POP, run_time=0.5),
            )
            self.wait(0.15)

        self.wait(0.6)
        self.play(FadeOut(cursore), run_time=0.5)

        # Formula del coseno
        p0 = MathTex(r"\text{per }", r"90^\circ-\theta", r"\text{ il numero è }", r"4-n",
                     font_size=FS, color=FG)
        p0[1].set_color(C_ANG)
        p0[3].set_color(C_N)
        p0.move_to([0, y_h[4] - 0.38, 0]).align_to([X_L, 0, 0], LEFT)

        p1 = MathTex(r"\cos\theta", r"=", r"\dfrac{\sqrt{", r"4-n", r"}}{2}", font_size=42, color=FG)
        p1[0].set_color(C_COS)
        p1[2].set_color(C_COS)
        p1[3].set_color(C_N)
        p1[4].set_color(C_COS)
        p1.move_to([0, y_h[4] - 1.22, 0]).align_to([X_L, 0, 0], LEFT)
        box_p1 = SurroundingRectangle(p1, color=C_N, buff=0.14, stroke_width=2.5)

        self.play(
            Write(p0),
            Indicate(VGroup(*cc), color=C_ANG, scale_factor=1.08),
            run_time=1.2,
        )
        self.wait(0.3)
        self.play(Write(p1), run_time=1.2)
        self.play(Create(box_p1), run_time=0.7)
        self.wait(1.0)

        # Simmetria: i salti restano 30, 15, 15, 30
        p2 = MathTex(r"\theta\mapsto90^\circ-\theta", r"\text{ manda l'insieme in sé}",
                     font_size=FS, color=FG)
        p2[0].set_color(C_ANG)
        p2.move_to([0, y_h[4] - 2.12, 0]).align_to([X_L, 0, 0], LEFT)

        p3 = MathTex(r"\text{salti uguali: }", r"30^\circ,\,15^\circ,\,15^\circ,\,30^\circ",
                     font_size=FS, color=FG)
        p3[1].set_color(C_ANG)
        p3.move_to([0, y_h[4] - 2.62, 0]).align_to([X_L, 0, 0], LEFT)

        self.play(
            Write(p2),
            Indicate(cth[2], color=C_ANG, scale_factor=1.3),
            Indicate(cc[2], color=C_ANG, scale_factor=1.3),
            run_time=1.2,
        )
        self.wait(0.4)
        self.play(
            Write(p3),
            Indicate(VGroup(*cth), color=C_ANG, scale_factor=1.08),
            Indicate(VGroup(*cc), color=C_ANG, scale_factor=1.08),
            run_time=1.4,
        )
        self.wait(3.0)

        da_mantenere = VGroup(
            griglia, asse_x, asse_y, lab_x, lab_y,
            cerchio, dot_O, lab_O, raggio_OA, dot_A, lab_A,
        )
        sub_mantenere = set(da_mantenere.get_family())
        da_rimuovere = [m for m in self.mobjects if m not in sub_mantenere]
        self.play(*[FadeOut(m) for m in da_rimuovere], run_time=1.0)
        self.wait(0.5)