import numpy as np
from common import *


class Scena06Corde(Scene):
    """Passo 4: le cinque corde con sola geometria elementare."""

    def construct(self):
        EASE = rate_functions.ease_in_out_cubic
        SMOOTH = rate_functions.ease_in_out_sine
        POP = rate_functions.ease_out_back

        C_AB = BLU
        C_EQ = ARANCIO
        FS = 31

        R = 2.6
        C = np.array([-3.4, -0.2, 0.0])
        O = C.copy()

        def P(ang, r=R):
            return C + r * np.array([np.cos(ang), np.sin(ang), 0.0])

        def dirz(ang):
            return np.array([np.cos(ang), np.sin(ang), 0.0])

        A = P(0)
        Ap = P(PI)
        B120 = P(2 * PI / 3)

        def crea_testo_con_ombra(latex, font_size, color):
            t_ = MathTex(latex, font_size=font_size, color=color)
            t_.set_stroke(color=BLACK, width=2.4, opacity=0.95, background=True)
            return t_

        def pos_B(a):
            return P(a) + 0.38 * dirz(a) + 0.12 * UP

        def pos_uno(a, lato=1):
            nrm = np.array([-np.sin(a), np.cos(a), 0.0])
            return P(a, R / 2) + lato * 0.32 * nrm

        def angolo_retto(V, p1, p2, s=0.24, color=GIALLO):
            u = (p1 - V) / np.linalg.norm(p1 - V)
            v = (p2 - V) / np.linalg.norm(p2 - V)
            return VMobject(color=color, stroke_width=3).set_points_as_corners(
                [V + s * u, V + s * u + s * v, V + s * v]
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
        dot_A = Dot(A, radius=0.07, color=FG)
        lab_O = MathTex(r"O", font_size=36, color=FG).next_to(dot_O, DL, buff=0.12)
        lab_A = MathTex(r"A", font_size=36, color=FG).next_to(dot_A, DR, buff=0.12)
        raggio_OA = Line(O, A, color=FG, stroke_width=3)
        uno_OA = MathTex(r"1", font_size=30, color=MUT).next_to(raggio_OA, DOWN, buff=0.15)

        self.add(
            griglia, asse_x, asse_y, lab_x, lab_y,
            cerchio, dot_O, lab_O, raggio_OA, uno_OA, dot_A, lab_A
        )
        self.wait(0.3)

        X_L = 0.75
        ys = [2.90, 2.30, 1.70, 1.10, 0.50]
        MAXW = 6.2

        def riga(m, i):
            if m.width > MAXW:
                m.scale_to_fit_width(MAXW)
            return m.move_to([0, ys[i], 0]).align_to([X_L, 0, 0], LEFT)

        titolo = MathTex(r"\text{Calcolo }", r"AB", r"\text{ nei cinque casi}", font_size=38, color=FG)
        titolo[1].set_color(C_AB)
        titolo.move_to([0, 3.55, 0]).align_to([X_L, 0, 0], LEFT)
        self.play(Write(titolo), run_time=0.9)

        larg_lab = 1.20
        larg_col = 0.96
        x_start = 0.75

        y_top = -0.95
        h_row = 0.60
        y_h = [y_top - k * h_row for k in range(5)]
        ys_row = [(y_h[i] + y_h[i + 1]) / 2 for i in range(4)]
        y_sn_center = y_h[4] - 0.75 / 2

        x_div_lab = x_start + larg_lab
        x_lab_center = x_start + larg_lab / 2
        xs_col_center = [x_div_lab + larg_col * (k + 0.5) for k in range(5)]
        xs_div = [x_div_lab + larg_col * k for k in range(6)]

        lab_r2t = MathTex(r"2\theta", font_size=31, color=GIALLO).move_to([x_lab_center, ys_row[0], 0])
        lab_rth = MathTex(r"\theta", font_size=31, color=GIALLO).move_to([x_lab_center, ys_row[1], 0])
        lab_rab = MathTex(r"AB", font_size=31, color=C_AB).move_to([x_lab_center, ys_row[2], 0])
        lab_rn = MathTex(r"n", font_size=31, color=VERDE).move_to([x_lab_center, ys_row[3], 0])
        lab_rsn = MathTex(r"\sin\theta", font_size=29, color=ARANCIO)

        VALORI_2T = [r"0^\circ", r"60^\circ", r"90^\circ", r"120^\circ", r"180^\circ"]
        VALORI_TH = [r"0^\circ", r"30^\circ", r"45^\circ", r"60^\circ", r"90^\circ"]
        VALORI_AB = [r"0", r"1", r"\sqrt{2}", r"\sqrt{3}", r"2"]
        VALORI_N = [r"0", r"1", r"2", r"3", r"4"]
        VALORI_SN = [r"0", r"\tfrac{1}{2}", r"\tfrac{\sqrt{2}}{2}", r"\tfrac{\sqrt{3}}{2}", r"1"]

        c2t = [MathTex(v, font_size=29, color=GIALLO).move_to([xs_col_center[k], ys_row[0], 0]) for k, v in enumerate(VALORI_2T)]
        cth = [MathTex(v, font_size=29, color=GIALLO).move_to([xs_col_center[k], ys_row[1], 0]) for k, v in enumerate(VALORI_TH)]
        cab = [MathTex(v, font_size=29, color=C_AB).move_to([xs_col_center[k], ys_row[2], 0]) for k, v in enumerate(VALORI_AB)]
        cn = [MathTex(v, font_size=29, color=VERDE).move_to([xs_col_center[k], ys_row[3], 0]) for k, v in enumerate(VALORI_N)]
        csn = [MathTex(v, font_size=28, color=ARANCIO) for v in VALORI_SN]

        quadro_iniziale = VGroup(
            Rectangle(width=larg_lab + larg_col, height=4 * h_row,
                      stroke_color=MUT, stroke_width=2.0, stroke_opacity=0.6, fill_opacity=0.0)
            .move_to([(x_start + xs_div[1]) / 2, (y_h[0] + y_h[4]) / 2, 0]),
            Line([x_div_lab, y_h[0], 0], [x_div_lab, y_h[4], 0], color=MUT, stroke_width=1.6, stroke_opacity=0.6),
            Line([x_start, y_h[1], 0], [xs_div[1], y_h[1], 0], color=MUT, stroke_width=1.0, stroke_opacity=0.3),
            Line([x_start, y_h[2], 0], [xs_div[1], y_h[2], 0], color=MUT, stroke_width=1.5, stroke_opacity=0.55),
            Line([x_start, y_h[3], 0], [xs_div[1], y_h[3], 0], color=MUT, stroke_width=1.0, stroke_opacity=0.3),
        )

        self.play(
            Create(quadro_iniziale),
            LaggedStart(Write(lab_r2t), Write(lab_rth), Write(lab_rab), Write(lab_rn), lag_ratio=0.12),
            Write(c2t[0]),
            run_time=1.1,
        )
        self.wait(0.2)

        pezzi_tabella = [quadro_iniziale, lab_r2t, lab_rth, lab_rab, lab_rn, c2t[0]]

        def espandi_colonna(k):
            x_l = xs_div[k]
            x_r = xs_div[k + 1]
            modulo = VGroup(
                Line([x_l, y_h[0], 0], [x_r, y_h[0], 0], color=MUT, stroke_width=2.0, stroke_opacity=0.6),
                Line([x_l, y_h[4], 0], [x_r, y_h[4], 0], color=MUT, stroke_width=2.0, stroke_opacity=0.6),
                Line([x_r, y_h[0], 0], [x_r, y_h[4], 0], color=MUT, stroke_width=2.0 if k == 4 else 1.2, stroke_opacity=0.6),
                Line([x_l, y_h[1], 0], [x_r, y_h[1], 0], color=MUT, stroke_width=1.0, stroke_opacity=0.3),
                Line([x_l, y_h[2], 0], [x_r, y_h[2], 0], color=MUT, stroke_width=1.5, stroke_opacity=0.55),
                Line([x_l, y_h[3], 0], [x_r, y_h[3], 0], color=MUT, stroke_width=1.0, stroke_opacity=0.3),
            )
            pezzi_tabella.append(modulo)
            pezzi_tabella.append(c2t[k])
            self.play(Create(modulo), Write(c2t[k]), run_time=0.6)

        def trascina_valori(k, src_ab, src_n):
            pezzi_tabella.extend([cab[k], cn[k], cth[k]])
            self.play(
                GrowFromCenter(cth[k], rate_func=POP),
                TransformFromCopy(src_ab, cab[k]),
                TransformFromCopy(src_n, cn[k]),
                run_time=0.9,
            )

        # B parametrizzato dal tracker t
        t = ValueTracker(0.0)
        ang = t.get_value

        dot_B = Dot(P(0), radius=0.07, color=FG).set_z_index(10)
        lab_B = MathTex(r"B", font_size=36, color=FG).move_to(pos_B(0))
        raggio_OB = Line(O, P(0), color=FG, stroke_width=3)
        corda = Line(A, P(0), color=C_AB, stroke_width=5)
        tri = Polygon(O, A, P(0), color=FG, stroke_width=0, fill_color=FG, fill_opacity=0.08)
        arco = Arc(radius=0.65, start_angle=0, angle=1e-3, arc_center=O, color=GIALLO, stroke_width=3.5)

        def lettura_gradi():
            a = ang()
            cifre = DecimalNumber(a / DEGREES, num_decimal_places=0, font_size=28, color=GIALLO)
            gr = MathTex(r"^\circ", font_size=28, color=GIALLO).next_to(cifre, RIGHT, buff=0.02).shift(UP * 0.06)
            g = VGroup(cifre, gr)
            raggio_lettura = float(np.interp(a, [60 * DEGREES, 120 * DEGREES], [1.25, 0.95]))
            shift_x = float(np.interp(a, [100 * DEGREES, 180 * DEGREES], [0.0, -0.42]))
            g.move_to(P(a / 2, raggio_lettura) + shift_x * RIGHT)
            g.set_opacity(float(np.clip(a / (35 * DEGREES), 0, 1)))
            return g

        lab_2t = always_redraw(lettura_gradi)

        def aggiorna(mob=None):
            a = ang()
            Bp = P(a)
            dot_B.move_to(Bp)
            lab_B.move_to(pos_B(a))
            raggio_OB.set_points_as_corners([O, Bp])
            corda.set_points_as_corners([A, Bp])
            tri.set_points_as_corners([O, A, Bp, O])
            arco.become(Arc(radius=0.65, start_angle=0, angle=max(a, 1e-3), arc_center=O,
                            color=GIALLO, stroke_width=3.5))
            arco.set_stroke(opacity=float(np.clip(a / (12 * DEGREES), 0, 1)))

        self.add(tri, raggio_OB, corda, arco, lab_2t)
        self.bring_to_front(dot_O, dot_A)

        # Caso 2theta = 0
        lab_equiv = MathTex(r"\equiv", font_size=36, color=FG)
        gruppo_coinc = VGroup(lab_A, lab_equiv, lab_B).arrange(RIGHT, buff=0.1)
        gruppo_coinc.next_to(dot_A, DOWN, buff=0.28).shift(LEFT * 0.15)

        self.play(FadeIn(dot_B, scale=0.5), Write(lab_equiv), Write(lab_B), run_time=0.7)

        l0a = riga(MathTex(r"2\theta", r"=", r"0^\circ", r"\;\Rightarrow\;", r"B \equiv A", font_size=FS, color=FG), 0)
        l0a[0].set_color(GIALLO)
        l0a[2].set_color(GIALLO)
        l0b = riga(MathTex(r"AB", r"=", r"0", r"\;\Rightarrow\;", r"n", r"=", r"AB^2", r"=", r"0", font_size=FS, color=FG), 1)
        l0b[0].set_color(C_AB)
        l0b[2].set_color(C_AB)
        l0b[4].set_color(VERDE)
        l0b[6].set_color(C_AB)
        l0b[8].set_color(VERDE)
        righe0 = VGroup(l0a, l0b)

        self.play(Write(l0a), run_time=0.8)
        self.play(Flash(A, color=C_AB, line_length=0.18, flash_radius=0.35), Write(l0b), run_time=1.0)
        self.wait(0.3)
        trascina_valori(0, l0b[2], l0b[8])
        self.wait(0.7)

        # Caso 2theta = 60: triangolo equilatero
        a60 = 60 * DEGREES
        self.play(
            FadeOut(righe0),
            FadeOut(lab_equiv),
            lab_A.animate.next_to(dot_A, DR, buff=0.12),
            lab_B.animate.move_to(pos_B(0)),
            run_time=0.6,
            rate_func=SMOOTH,
        )

        cerchio.add_updater(aggiorna)
        self.play(t.animate.set_value(a60), run_time=1.4, rate_func=EASE)
        espandi_colonna(1)

        l1 = riga(MathTex(r"\widehat{AOB}", r"=", r"2\theta", r"=", r"60^\circ", font_size=FS, color=FG), 0)
        for i in (0, 2, 4):
            l1[i].set_color(GIALLO)
        l2 = riga(MathTex(r"\widehat{OAB}=\widehat{OBA}=\dfrac{180^\circ-60^\circ}{2}=", r"60^\circ", font_size=FS, color=FG), 1)
        l2[1].set_color(GIALLO)
        l3 = riga(MathTex(r"\triangle OAB\text{ equilatero}", font_size=FS, color=FG), 2)
        l3.set_color(C_AB)
        l4 = riga(MathTex(r"AB", r"=", r"1", r"\;\Rightarrow\;", r"n", r"=", r"1", font_size=FS, color=FG), 3)
        l4[0].set_color(C_AB)
        l4[2].set_color(C_AB)
        l4[4].set_color(VERDE)
        l4[6].set_color(VERDE)
        righe60 = VGroup(l1, l2, l3, l4)

        arc_A = Arc(radius=0.5, start_angle=2 * PI / 3, angle=PI / 3, arc_center=A, color=GIALLO, stroke_width=3.5)
        arc_B = Arc(radius=0.5, start_angle=4 * PI / 3, angle=PI / 3, arc_center=P(a60), color=GIALLO, stroke_width=3.5)
        t_A = MathTex(r"60^\circ", font_size=22, color=GIALLO).move_to(A + 0.88 * dirz(150 * DEGREES))
        t_B = MathTex(r"60^\circ", font_size=22, color=GIALLO).move_to(P(a60) + 0.88 * dirz(270 * DEGREES))
        uno_OB = MathTex(r"1", font_size=30, color=MUT).move_to(pos_uno(a60))
        lab_AB = crea_testo_con_ombra(r"1", 28, C_AB).move_to(
            (A + P(a60)) / 2 + 0.22 * dirz(30 * DEGREES)
        )
        dec60 = VGroup(arc_A, arc_B, t_A, t_B, uno_OB, lab_AB)

        self.play(Write(l1), run_time=0.8)
        self.play(Create(arc_A), Create(arc_B), Write(t_A), Write(t_B), Write(l2), run_time=1.2)
        self.wait(0.4)
        self.play(tri.animate.set_fill(C_AB, 0.22), Write(l3), Write(uno_OB), run_time=1.0)
        self.play(Write(lab_AB), Write(l4), run_time=1.0)
        self.wait(0.3)
        trascina_valori(1, l4[2], l4[6])
        self.wait(0.8)

        self.play(FadeOut(dec60), FadeOut(righe60), run_time=0.5)

        # Caso 2theta = 90: Pitagora
        a90 = 90 * DEGREES
        self.play(
            tri.animate.set_fill(FG, 0.08),
            t.animate.set_value(a90),
            run_time=1.3, rate_func=EASE,
        )
        espandi_colonna(2)

        m1 = riga(MathTex(r"2\theta", r"=", r"90^\circ", r"\;\Rightarrow\;", r"\triangle OAB\text{ rettangolo in }O", font_size=FS, color=FG), 0)
        m1[0].set_color(GIALLO)
        m1[2].set_color(GIALLO)
        m2 = riga(MathTex(r"AB^2=1^2+1^2=2", r"\;\Rightarrow\;", r"AB", r"=", r"\sqrt{2}", font_size=FS, color=FG), 1)
        m2[2].set_color(C_AB)
        m2[4].set_color(C_AB)
        m3 = riga(MathTex(r"n", r"=", r"AB^2", r"=", r"2", font_size=FS, color=FG), 2)
        m3[0].set_color(VERDE)
        m3[2].set_color(C_AB)
        m3[4].set_color(VERDE)
        righe90 = VGroup(m1, m2, m3)

        marca_O = angolo_retto(O, A, P(a90), s=0.26, color=GIALLO)
        uno_OB = MathTex(r"1", font_size=30, color=MUT).move_to(pos_uno(a90))
        lab_AB = crea_testo_con_ombra(r"\sqrt{2}", 28, C_AB).move_to(
            (A + P(a90)) / 2 + 0.32 * dirz(45 * DEGREES)
        )

        cerchio.remove_updater(aggiorna)
        self.play(
            Write(m1),
            Write(uno_OB),
            ReplacementTransform(arco, marca_O),
            run_time=1.0,
        )
        self.play(tri.animate.set_fill(C_AB, 0.22), Write(m2), run_time=1.1)
        self.play(Write(m3), Write(lab_AB), run_time=0.9)
        self.wait(0.3)
        trascina_valori(2, m2[4], m3[4])
        self.wait(0.8)

        arco.become(Arc(radius=0.65, start_angle=0, angle=a90, arc_center=O, color=GIALLO, stroke_width=3.5))
        self.play(ReplacementTransform(marca_O, arco), run_time=0.4)
        cerchio.add_updater(aggiorna)

        self.play(FadeOut(righe90), FadeOut(uno_OB), FadeOut(lab_AB), run_time=0.5)

        self.play(
            tri.animate.set_fill(FG, 0.08),
            t.animate.set_value(2 * PI / 3),
            run_time=1.3, rate_func=EASE,
        )
        espandi_colonna(3)

        # Caso 2theta = 120: equilatero OBA' piu' Talete
        dot_Ap = Dot(Ap, radius=0.07, color=FG).set_z_index(10)
        lab_Ap = MathTex(r"A'", font_size=36, color=FG).next_to(dot_Ap, DL, buff=0.14).shift(DOWN * 0.12)

        e1 = riga(MathTex(r"\widehat{BOA'}", r"=", r"180^\circ-120^\circ", r"=", r"60^\circ", font_size=FS, color=FG), 0)
        e1[0].set_color(GIALLO)
        e1[4].set_color(GIALLO)
        e2 = riga(MathTex(r"\triangle OBA'\text{ equilatero},\quad A'B=1", font_size=FS, color=FG), 1)
        e2.set_color(C_EQ)
        e3 = riga(MathTex(r"\triangle ABA'\text{ rettangolo in }B\text{ (diametro }AA'=2)", font_size=FS, color=FG), 2)
        e3.set_color(C_AB)
        e4 = riga(MathTex(r"AB^2", r"=", r"AA'^2-A'B^2", r"=", r"2^2-1^2=3", font_size=FS, color=FG), 3)
        e4[0].set_color(C_AB)
        e5 = riga(MathTex(r"AB", r"=", r"\sqrt{3}", r"\;\Rightarrow\;", r"n", r"=", r"3", font_size=FS, color=FG), 4)
        e5[0].set_color(C_AB)
        e5[2].set_color(C_AB)
        e5[4].set_color(VERDE)
        e5[6].set_color(VERDE)
        righe120 = VGroup(e1, e2, e3, e4, e5)

        tri_OBAp = Polygon(O, B120, Ap, color=C_EQ, stroke_width=0, fill_color=C_EQ, fill_opacity=0.25)
        seg_ApB = Line(Ap, B120, color=C_EQ, stroke_width=6)
        tri_ABAp = Polygon(A, B120, Ap, color=C_AB, stroke_width=0, fill_color=C_AB, fill_opacity=0.18)
        semicirc = Arc(radius=R, start_angle=0, angle=PI, arc_center=C, color=GIALLO, stroke_width=5)
        marca_B = angolo_retto(B120, A, Ap, s=0.22, color=FG)

        uno_OB = MathTex(r"1", font_size=30, color=MUT).move_to(pos_uno(2 * PI / 3, lato=-1))
        uno_OAp = MathTex(r"1", font_size=30, color=MUT).move_to(P(PI, R / 2) + 0.30 * DOWN)
        lab_ApB = crea_testo_con_ombra(r"1", 28, C_EQ).move_to(
            (Ap + B120) / 2 + 0.24 * dirz(-30 * DEGREES)
        )
        lab_AB = crea_testo_con_ombra(r"\sqrt{3}", 28, C_AB).move_to(
            (A + B120) / 2 + 0.36 * dirz(60 * DEGREES)
        )

        self.play(FadeIn(dot_Ap, scale=0.5), Write(lab_Ap), Write(e1), run_time=0.9)
        self.play(
            FadeIn(tri_OBAp), Create(seg_ApB),
            Write(uno_OB), Write(uno_OAp), Write(lab_ApB),
            Write(e2),
            run_time=1.1,
        )
        self.bring_to_front(dot_Ap, dot_B)
        self.wait(0.4)
        self.play(
            FadeIn(tri_ABAp), Create(marca_B),
            Write(e3),
            run_time=1.2,
        )
        self.play(Write(e4), run_time=1.0)
        self.play(Write(e5), Write(lab_AB), run_time=0.9)
        self.wait(0.3)
        trascina_valori(3, e5[2], e5[6])
        self.wait(0.8)

        decor120 = VGroup(
            tri_OBAp, seg_ApB, tri_ABAp, marca_B, uno_OB, uno_OAp, lab_ApB, lab_AB,
            dot_Ap, lab_Ap
        )

        self.play(FadeOut(righe120), FadeOut(decor120), run_time=0.6)

        # Caso 2theta = 180: diametro
        a180 = PI
        self.play(t.animate.set_value(a180), run_time=1.4, rate_func=EASE)
        espandi_colonna(4)

        d1 = riga(MathTex(r"2\theta", r"=", r"180^\circ", r"\;\Rightarrow\;", r"AB\text{ è un diametro}", font_size=FS, color=FG), 0)
        d1[0].set_color(GIALLO)
        d1[2].set_color(GIALLO)
        d2 = riga(MathTex(r"AB", r"=", r"2\cdot OA", r"=", r"2", font_size=FS, color=FG), 1)
        d2[0].set_color(C_AB)
        d2[4].set_color(C_AB)
        d3 = riga(MathTex(r"n", r"=", r"AB^2", r"=", r"4", font_size=FS, color=FG), 2)
        d3[0].set_color(VERDE)
        d3[2].set_color(C_AB)
        d3[4].set_color(VERDE)
        righe180 = VGroup(d1, d2, d3)

        uno_OB = MathTex(r"1", font_size=30, color=MUT).move_to(pos_uno(a180, lato=1))
        lab_AB = crea_testo_con_ombra(r"2", 28, C_AB).move_to(C + 0.32 * UP + 0.40 * RIGHT)
        lab_B.move_to(pos_B(a180) + 0.15 * LEFT)

        self.play(Write(d1), Write(uno_OB), Write(lab_AB), run_time=1.0)
        self.play(Write(d2), run_time=0.8)
        self.play(Write(d3), run_time=0.8)
        self.wait(0.3)
        trascina_valori(4, d2[4], d3[4])
        self.wait(1.0)

        self.play(FadeOut(righe180), FadeOut(uno_OB), FadeOut(lab_AB), run_time=0.6)

        # Conclusione: sin(theta) = AB/2
        fin1 = MathTex(r"AB^2", r"=", r"n", r"\;\Rightarrow\;", r"AB", r"=", r"\sqrt{n}",
                       font_size=38, color=FG).move_to([0, 2.95, 0]).align_to([X_L, 0, 0], LEFT)
        fin1[0].set_color(C_AB)
        fin1[2].set_color(VERDE)
        fin1[4].set_color(C_AB)
        fin1[6].set_color(VERDE)

        fin2 = MathTex(r"\sin\theta", r"=", r"\dfrac{AB}{2}", r"=", r"\dfrac{\sqrt{n}}{2}",
                       font_size=42, color=FG).move_to([0, 1.75, 0]).align_to([X_L, 0, 0], LEFT)
        fin2[0].set_color(ARANCIO)
        fin2[2].set_color(C_AB)
        fin2[4].set_color(VERDE)
        box_fin = SurroundingRectangle(fin2, color=VERDE, buff=0.18, stroke_width=2.5)

        self.play(Write(fin1), run_time=0.9)
        self.play(
            ShowPassingFlash(semicirc, time_width=0.6),
            Write(fin2),
            Create(box_fin),
            run_time=1.2
        )
        self.wait(0.5)

        SHIFT_TABELLA = UP * 1.15
        tabella_da_alzare = VGroup(*pezzi_tabella)
        self.play(tabella_da_alzare.animate.shift(SHIFT_TABELLA), run_time=1.3, rate_func=EASE)

        y_sn_top = y_h[4] + 1.15
        y_sn_bot = y_sn_top - 0.75
        y_sn_c = (y_sn_top + y_sn_bot) / 2

        modulo_sn = VGroup(
            Line([x_start, y_sn_bot, 0], [xs_div[5], y_sn_bot, 0], color=MUT, stroke_width=2.0, stroke_opacity=0.6),
            Line([x_start, y_sn_top, 0], [x_start, y_sn_bot, 0], color=MUT, stroke_width=2.0, stroke_opacity=0.6),
            Line([xs_div[5], y_sn_top, 0], [xs_div[5], y_sn_bot, 0], color=MUT, stroke_width=2.0, stroke_opacity=0.6),
            Line([x_div_lab, y_sn_top, 0], [x_div_lab, y_sn_bot, 0], color=MUT, stroke_width=1.6, stroke_opacity=0.6),
            *[Line([x, y_sn_top, 0], [x, y_sn_bot, 0], color=MUT, stroke_width=1.2, stroke_opacity=0.35) for x in xs_div[1:5]]
        )
        lab_rsn.move_to([x_lab_center, y_sn_c, 0])

        self.play(Create(modulo_sn), Write(lab_rsn), run_time=0.7)

        for k in range(5):
            csn[k].move_to([xs_col_center[k], y_sn_c, 0])

        self.play(
            LaggedStart(
                *[TransformFromCopy(cab[k], csn[k]) for k in range(5)],
                lag_ratio=0.20
            ),
            run_time=1.8,
        )
        self.wait(1.5)

        cerchio.remove_updater(aggiorna)
        # Riepilogo: le quattro corde sul cerchio
        lab_2t.clear_updaters()

        cose_extra = [
            tri, arco, lab_2t, corda, raggio_OB, raggio_OA, uno_OA,
            dot_B, lab_B
        ]
        self.play(FadeOut(*cose_extra), run_time=0.8, rate_func=SMOOTH)
        self.bring_to_front(dot_O, lab_O, dot_A, lab_A)

        p60 = P(PI / 3)
        p90 = P(PI / 2)
        p120 = P(2 * PI / 3)

        dot_0 = Dot(A, radius=0.082, color=ARANCIO).set_z_index(10)
        lab_caso_0 = VGroup(
            MathTex(r"AB = 0", font_size=25, color=FG),
            MathTex(r"2\theta = 0^\circ", font_size=20, color=FG)
        ).arrange(DOWN, buff=0.06).next_to(A, UR, buff=0.18)

        self.play(
            Flash(A, color=ARANCIO, line_length=0.18, num_lines=8),
            GrowFromCenter(dot_0, rate_func=POP),
            GrowFromCenter(lab_caso_0, rate_func=POP),
            run_time=0.6,
        )
        self.wait(0.2)

        corda_60 = Line(A, p60, color=ARANCIO, stroke_width=4.5)
        dot_60 = Dot(p60, radius=0.082, color=ARANCIO).set_z_index(10)
        lab_caso_60 = VGroup(
            MathTex(r"AB = 1", font_size=25, color=ARANCIO),
            MathTex(r"2\theta = 60^\circ", font_size=20, color=FG)
        ).arrange(DOWN, buff=0.06).next_to(p60, UR, buff=0.16)

        self.play(Create(corda_60), run_time=0.55, rate_func=EASE)
        self.play(
            Flash(p60, color=ARANCIO, line_length=0.18, num_lines=8),
            GrowFromCenter(dot_60, rate_func=POP),
            GrowFromCenter(lab_caso_60, rate_func=POP),
            run_time=0.45,
        )
        self.wait(0.15)

        corda_90 = Line(A, p90, color=BLU, stroke_width=4.5)
        dot_90 = Dot(p90, radius=0.082, color=ARANCIO).set_z_index(10)
        lab_caso_90 = VGroup(
            MathTex(r"AB = \sqrt{2}", font_size=25, color=BLU),
            MathTex(r"2\theta = 90^\circ", font_size=20, color=FG)
        ).arrange(DOWN, buff=0.06).next_to(p90, UP, buff=0.16)

        self.play(Create(corda_90), run_time=0.55, rate_func=EASE)
        self.play(
            Flash(p90, color=BLU, line_length=0.18, num_lines=8),
            GrowFromCenter(dot_90, rate_func=POP),
            GrowFromCenter(lab_caso_90, rate_func=POP),
            run_time=0.45,
        )
        self.wait(0.15)

        corda_120 = Line(A, p120, color=VERDE, stroke_width=4.5)
        dot_120 = Dot(p120, radius=0.082, color=ARANCIO).set_z_index(10)
        lab_caso_120 = VGroup(
            MathTex(r"AB = \sqrt{3}", font_size=25, color=VERDE),
            MathTex(r"2\theta = 120^\circ", font_size=20, color=FG)
        ).arrange(DOWN, buff=0.06).next_to(p120, UL, buff=0.16)

        self.play(Create(corda_120), run_time=0.55, rate_func=EASE)
        self.play(
            Flash(p120, color=VERDE, line_length=0.18, num_lines=8),
            GrowFromCenter(dot_120, rate_func=POP),
            GrowFromCenter(lab_caso_120, rate_func=POP),
            run_time=0.45,
        )
        self.wait(0.15)

        corda_180 = Line(A, Ap, color=FG, stroke_width=4.0)
        dot_180 = Dot(Ap, radius=0.082, color=ARANCIO).set_z_index(10)
        lab_Ap_fig = MathTex(r"A'", font_size=32, color=FG).next_to(Ap, DL, buff=0.14)
        lab_caso_180 = VGroup(
            MathTex(r"AB = 2", font_size=25, color=FG),
            MathTex(r"2\theta = 180^\circ", font_size=20, color=FG)
        ).arrange(DOWN, buff=0.06).move_to(C + 1.35 * LEFT + 0.48 * UP)

        self.play(Create(corda_180), run_time=0.60, rate_func=EASE)
        self.play(
            Flash(Ap, color=FG, line_length=0.20, num_lines=8),
            GrowFromCenter(dot_180, rate_func=POP),
            Write(lab_Ap_fig),
            GrowFromCenter(lab_caso_180, rate_func=POP),
            run_time=0.50,
        )
        self.wait(0.2)

        fasci_luce = [
            Line(A, p60, color=ARANCIO, stroke_width=7.5),
            Line(A, p90, color=BLU, stroke_width=7.5),
            Line(A, p120, color=VERDE, stroke_width=7.5),
            Line(A, Ap, color=FG, stroke_width=7.5),
        ]
        self.play(
            LaggedStart(*[ShowPassingFlash(f, time_width=0.5) for f in fasci_luce], lag_ratio=0.08),
            run_time=1.0,
        )
        self.wait(3.0)

        da_togliere_scena05 = [
            titolo, fin1, fin2, box_fin,
            tabella_da_alzare, modulo_sn, lab_rsn, *csn,
            dot_0, lab_caso_0,
            corda_60, dot_60, lab_caso_60,
            corda_90, dot_90, lab_caso_90,
            corda_120, dot_120, lab_caso_120,
            corda_180, dot_180, lab_caso_180, lab_Ap_fig
        ]

        raggio_OA = Line(O, A, color=FG, stroke_width=3)
        uno_OA = MathTex(r"1", font_size=30, color=MUT).next_to(raggio_OA, DOWN, buff=0.15)

        self.play(
            FadeOut(*da_togliere_scena05),
            Create(raggio_OA),
            Write(uno_OA),
            run_time=1.1,
            rate_func=SMOOTH,
        )
        self.wait(0.6)