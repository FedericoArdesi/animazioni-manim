import numpy as np
from common import *


class Scena08Salti(Scene):
    """Passo 5: da n all'angolo, con cos(2theta) = 1 - n/2."""

    def construct(self):
        EASE = rate_functions.ease_in_out_cubic
        SMOOTH = rate_functions.ease_in_out_sine
        POP = rate_functions.ease_out_back

        C_COS = BLU
        C_N = VERDE
        C_ANG = GIALLO

        R = 2.6
        C = np.array([-3.4, -0.2, 0.0])
        O = C.copy()

        def P(ang, r=R):
            return C + r * np.array([np.cos(ang), np.sin(ang), 0.0])

        def dirz(ang):
            return np.array([np.cos(ang), np.sin(ang), 0.0])

        A = P(0)
        Ap = P(PI)

        # Angoli doppi, livelli di cos(2theta) e salti
        ang2 = [0, 60, 90, 120, 180]
        a_k = [g * DEGREES for g in ang2]
        pts = [P(a) for a in a_k]
        lvl = [C[0] + R * (1 - k / 2) for k in range(5)]
        salti_2t = [60, 30, 30, 60]
        salti_th = [30, 15, 15, 30]

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
        # Titolo e formula di partenza
        titolo = MathTex(r"\text{Da }", r"n", r"\text{ all'angolo}", font_size=38, color=FG)
        titolo[1].set_color(C_N)
        titolo.move_to([0, 3.55, 0]).align_to([X_L, 0, 0], LEFT)

        f0 = MathTex(r"\cos2\theta", r"=", r"1-", r"\dfrac{n}{2}", font_size=38, color=FG)
        f0[0].set_color(C_COS)
        f0[3].set_color(C_N)
        f0.move_to([0, 2.75, 0]).align_to([X_L, 0, 0], LEFT)

        self.play(Write(titolo), run_time=0.7)
        self.play(Write(f0), run_time=0.9)
        self.wait(0.2)

        larg_lab = 1.20
        larg_col = 0.96
        x_start = 0.75
        y_top = 1.85
        h_row = 0.60
        y_h = [y_top - k * h_row for k in range(5)]
        ys_row = [(y_h[i] + y_h[i + 1]) / 2 for i in range(4)]
        x_div_lab = x_start + larg_lab
        x_lab_center = x_start + larg_lab / 2
        xs_col_center = [x_div_lab + larg_col * (k + 0.5) for k in range(5)]
        xs_div = [x_div_lab + larg_col * k for k in range(6)]

        # Tabella n, cos(2theta), 2theta, theta
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
        lab_rc = MathTex(r"\cos2\theta", font_size=27, color=C_COS).move_to([x_lab_center, ys_row[1], 0])
        lab_r2t = MathTex(r"2\theta", font_size=31, color=C_ANG).move_to([x_lab_center, ys_row[2], 0])
        lab_rth = MathTex(r"\theta", font_size=31, color=C_ANG).move_to([x_lab_center, ys_row[3], 0])

        VAL_N = [r"0", r"1", r"2", r"3", r"4"]
        VAL_C = [r"1", r"\tfrac12", r"0", r"-\tfrac12", r"-1"]
        VAL_2T = [r"0^\circ", r"60^\circ", r"90^\circ", r"120^\circ", r"180^\circ"]
        VAL_TH = [r"0^\circ", r"30^\circ", r"45^\circ", r"60^\circ", r"90^\circ"]

        cn = [MathTex(v, font_size=29, color=C_N).move_to([xs_col_center[k], ys_row[0], 0]) for k, v in enumerate(VAL_N)]
        cc = [MathTex(v, font_size=28, color=C_COS).move_to([xs_col_center[k], ys_row[1], 0]) for k, v in enumerate(VAL_C)]
        c2t = [MathTex(v, font_size=29, color=C_ANG).move_to([xs_col_center[k], ys_row[2], 0]) for k, v in enumerate(VAL_2T)]
        cth = [MathTex(v, font_size=29, color=C_ANG).move_to([xs_col_center[k], ys_row[3], 0]) for k, v in enumerate(VAL_TH)]

        cursore = Rectangle(width=larg_col, height=4 * h_row, stroke_width=0,
                            fill_color=FG, fill_opacity=0.07)
        cursore.move_to([xs_col_center[0], (y_h[0] + y_h[4]) / 2, 0])

        self.play(Create(scheletro), run_time=0.75)
        self.play(
            LaggedStart(Write(lab_rn), Write(lab_rc), Write(lab_r2t), Write(lab_rth), lag_ratio=0.15),
            run_time=0.75,
        )
        self.wait(0.2)

        # Oggetti della figura
        y_arr = C[1] - 1.25
        dash, dots, ticks = {}, {}, {}
        for k in range(5):
            if k in (1, 2, 3):
                dash[k] = DashedLine([lvl[k], C[1], 0], pts[k], color=FG, stroke_width=2,
                                     stroke_opacity=0.5, dash_length=0.08)
                dots[k] = Dot(pts[k], radius=0.07, color=FG).set_z_index(10)
            if k != 2:
                ticks[k] = Line([lvl[k], C[1], 0], [lvl[k], C[1] - 1.45, 0],
                                color=MUT, stroke_width=1.5, stroke_opacity=0.5)

        dot_Ap = Dot(Ap, radius=0.07, color=FG).set_z_index(10)
        lab_Ap = MathTex(r"A'", font_size=36, color=FG).next_to(dot_Ap, DL, buff=0.14).shift(DOWN * 0.12)

        self.play(
            FadeIn(cursore),
            GrowFromCenter(cn[0], rate_func=POP),
            GrowFromCenter(cc[0], rate_func=POP),
            GrowFromCenter(c2t[0], rate_func=POP),
            Create(ticks[0]),
            run_time=0.35,
        )
        self.wait(0.15)

        archi, lab_archi, frecce, lbl_hops = [], [], [], []

        for k in range(4):
            x_s, x_e = lvl[k], lvl[k + 1]

            hop = Arrow(
                np.array([x_s, y_arr, 0.0]), np.array([x_e, y_arr, 0.0]),
                buff=0, color=C_COS, stroke_width=2.5, tip_length=0.18,
            )
            lbl_hop = MathTex(r"-\tfrac12", font_size=26, color=C_COS).move_to(
                [(x_s + x_e) / 2, y_arr - 0.32, 0]
            )
            lbl_hops.append(lbl_hop)

            arco = Arc(radius=R, start_angle=a_k[k], angle=a_k[k + 1] - a_k[k],
                       arc_center=C, color=C_ANG, stroke_width=6)
            mid = (a_k[k] + a_k[k + 1]) / 2
            lbl_arco = MathTex(rf"+{salti_2t[k]}^\circ", font_size=28, color=C_ANG).move_to(
                P(mid, R + 0.50)
            )

            archi.append(arco)
            lab_archi.append(lbl_arco)
            frecce.append(hop)

            atterra = [
                GrowFromCenter(cn[k + 1], rate_func=POP),
                GrowFromCenter(cc[k + 1], rate_func=POP),
                cursore.animate.set_x(xs_col_center[k + 1]),
            ]
            if (k + 1) in ticks:
                atterra.append(Create(ticks[k + 1]))
            if (k + 1) in dash:
                atterra += [
                    Create(dash[k + 1]),
                    GrowFromPoint(dots[k + 1], np.array([lvl[k + 1], C[1], 0.0]), rate_func=POP),
                ]
            if k + 1 == 4:
                atterra += [GrowFromCenter(dot_Ap, rate_func=POP), Write(lab_Ap)]

            self.play(
                LaggedStart(
                    AnimationGroup(
                        GrowArrow(hop),
                        FadeIn(lbl_hop, shift=DOWN * 0.15),
                        run_time=0.5,
                    ),
                    AnimationGroup(*atterra, run_time=0.4),
                    AnimationGroup(
                        Create(arco),
                        FadeIn(lbl_arco, shift=dirz(mid) * 0.15),
                        GrowFromCenter(c2t[k + 1], rate_func=POP),
                        run_time=0.5,
                    ),
                    lag_ratio=0.70,
                )
            )
            self.wait(0.15)

        self.wait(0.6)

        self.play(
            LaggedStart(*[Indicate(ar, color=C_ANG, scale_factor=1.03) for ar in archi], lag_ratio=0.35),
            run_time=1.8,
        )
        self.wait(0.8)

        # I salti sono di 2theta, non di theta
        raggio_OB1 = Line(O, pts[1], color=FG, stroke_width=2.5)
        arco_O = Arc(radius=0.60, start_angle=0, angle=a_k[1], arc_center=O,
                     color=C_ANG, stroke_width=3.5)
        lab_O2t = MathTex(r"2\theta", font_size=28, color=C_ANG).move_to(P(a_k[1] / 2, 0.98))

        p1 = MathTex(r"\widehat{AOB}", r"=", r"2\theta", font_size=36, color=FG)
        p1[2].set_color(C_ANG)
        p1.move_to([0, y_h[4] - 0.75, 0]).align_to([X_L, 0, 0], LEFT)

        self.play(
            Create(raggio_OB1), Create(arco_O), Write(lab_O2t),
            Write(p1),
            run_time=1.1,
        )
        self.wait(0.8)

        box_2t = Rectangle(width=larg_lab + 5 * larg_col, height=h_row,
                           stroke_color=C_ANG, stroke_width=2.5, fill_opacity=0.0)
        box_2t.move_to([(x_start + xs_div[5]) / 2, ys_row[2], 0])

        p2 = MathTex(r"\text{salti di }", r"2\theta", r"\text{, non di }", r"\theta",
                     font_size=36, color=FG)
        p2[1].set_color(C_ANG)
        p2[3].set_color(MUT)
        p2.move_to([0, y_h[4] - 1.45, 0]).align_to([X_L, 0, 0], LEFT)

        self.play(Create(box_2t), run_time=0.6)
        self.play(
            Write(p2),
            LaggedStart(*[Indicate(lb, color=C_ANG, scale_factor=1.25) for lb in lab_archi], lag_ratio=0.3),
            run_time=1.6,
        )
        self.wait(1.4)

        # Si dimezza: da 2theta a theta
        p3 = MathTex(r"\theta", r"=", r"\dfrac{2\theta}{2}", font_size=38, color=FG)
        p3[0].set_color(C_ANG)
        p3[2].set_color(C_ANG)
        p3.move_to([0, y_h[4] - 2.30, 0]).align_to([X_L, 0, 0], LEFT)

        aiuti = [
            *dash.values(), *ticks.values(), *frecce, *lbl_hops,
            lab_Ap, raggio_OB1, arco_O, lab_O2t, box_2t, p1, *lab_archi,
        ]
        self.play(*[FadeOut(m) for m in aiuti], Write(p3), run_time=0.8)

        # I punti scivolano da 2theta a theta
        m = ValueTracker(1.0)
        for k in (1, 2, 3):
            dots[k].add_updater(lambda d, k=k: d.move_to(P(m.get_value() * a_k[k])))
        dot_Ap.add_updater(lambda d: d.move_to(P(m.get_value() * a_k[4])))
        for k in range(4):
            archi[k].add_updater(
                lambda ar, k=k: ar.become(
                    Arc(radius=R, start_angle=m.get_value() * a_k[k],
                        angle=m.get_value() * (a_k[k + 1] - a_k[k]),
                        arc_center=C, color=C_ANG, stroke_width=6)
                )
            )

        self.play(
            m.animate.set_value(0.5),
            cursore.animate.set_x(xs_col_center[0]),
            run_time=2.4, rate_func=EASE,
        )
        for k in (1, 2, 3):
            dots[k].clear_updaters()
        dot_Ap.clear_updaters()
        for k in range(4):
            archi[k].clear_updaters()

        lab_archi = []
        for k in range(4):
            mid_th = (a_k[k] + a_k[k + 1]) / 4
            lab_archi.append(
                MathTex(rf"+{salti_th[k]}^\circ", font_size=26, color=C_ANG).move_to(P(mid_th, R + 0.55))
            )
        self.play(
            LaggedStart(*[FadeIn(lb, shift=dirz((a_k[k] + a_k[k + 1]) / 4) * 0.15)
                          for k, lb in enumerate(lab_archi)], lag_ratio=0.25),
            run_time=1.0,
        )
        self.wait(0.8)
        self.play(FadeOut(p2), FadeOut(p3), run_time=0.5)
        self.wait(0.2)

        self.play(GrowFromCenter(cth[0], rate_func=POP), run_time=0.35)
        self.wait(0.15)

        # Salti di theta, come nella scena 02
        y_hop = ys_row[3] - 0.55
        hop_lab = []

        for k in range(4):
            x0 = xs_col_center[k] + 0.22
            x1 = xs_col_center[k + 1] - 0.22
            ar = ArcBetweenPoints(
                np.array([x0, y_hop, 0.0]), np.array([x1, y_hop, 0.0]),
                angle=PI / 2, color=C_ANG, stroke_width=2.5,
            ).add_tip(tip_length=0.18, tip_width=0.15).shift(UP * 0.2)
            lb = MathTex(rf"+{salti_th[k]}^\circ", font_size=28, color=C_ANG).move_to(
                [(xs_col_center[k] + xs_col_center[k + 1]) / 2, y_hop - 0.60, 0]
            )
            hop_lab.append(lb)

            self.play(
                LaggedStart(
                    AnimationGroup(
                        GrowFromPoint(ar, ar.get_start()),
                        FadeIn(lb, shift=DOWN * 0.15),
                        Indicate(lab_archi[k], color=C_ANG, scale_factor=1.25),
                        run_time=0.5,
                    ),
                    AnimationGroup(
                        GrowFromPoint(cth[k + 1], ar.get_end(), rate_func=POP),
                        cursore.animate.set_x(xs_col_center[k + 1]),
                        run_time=0.4,
                    ),
                    lag_ratio=0.70,
                )
            )
            self.wait(0.15)

        self.wait(0.6)

        box_salti = SurroundingRectangle(VGroup(*hop_lab), color=C_ANG, buff=0.18, stroke_width=2.5)
        self.play(
            FadeOut(cursore),
            Create(box_salti),
            run_time=0.8,
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