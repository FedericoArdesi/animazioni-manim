import numpy as np
from common import *


class Scena05Passo2(Scene):
    """Passo 2: AB = 2 sin(theta), la corda sottesa dall'angolo al centro 2theta."""

    def construct(self):
        EASE = rate_functions.ease_in_out_cubic
        SMOOTH = rate_functions.ease_in_out_sine

        C_AM = ARANCIO
        C_MB = ROSA
        C_AB = BLU

        # Geometria: cerchio di raggio 1 (R in unita' di scena)
        R = 2.6
        C = np.array([0.0, -0.2, 0.0])
        TH = 38 * DEGREES

        def P(ang, r=R):
            return C + r * np.array([np.cos(ang), np.sin(ang), 0.0])

        O = C.copy()
        A = P(0)
        B = P(2 * TH)
        M = (A + B) / 2

        def crea_testo_con_ombra(latex, font_size, color):
            t = MathTex(latex, font_size=font_size, color=color)
            t.set_stroke(color=BLACK, width=2.4, opacity=0.95, background=True)
            return t

        def pos_B(a):
            return P(a) + 0.38 * np.array([np.cos(a), np.sin(a), 0.0]) + 0.12 * UP

        def pos_uno(a):
            return P(a, R * 0.5) + 0.38 * LEFT + 0.08 * UP

        def pos_M(a):
            norm_dir = np.array([np.cos(a / 2), np.sin(a / 2), 0.0])
            return (A + P(a)) / 2 + 0.30 * norm_dir

        def pos_T(a):
            """Via di mezzo: né troppo vicina alla corda, né troppo lontana fuori."""
            return (A + P(a)) / 2 + np.array([0.95, 0.55, 0.0])

        step = R / 4
        x_min, x_max = C[0] - 5 * step, C[0] + 5 * step
        y_min, y_max = C[1] - 5 * step, C[1] + 5 * step

        linee_vert = VGroup(*[Line([C[0] + k * step, y_min, 0], [C[0] + k * step, y_max, 0]) for k in range(-4, 5)])
        linee_oriz = VGroup(*[Line([x_min, C[1] + k * step, 0], [x_max, C[1] + k * step, 0]) for k in range(-4, 5)])
        griglia = VGroup(linee_vert, linee_oriz)
        griglia.set_stroke(color=MUT, width=1, opacity=0.18)

        asse_x = Arrow([x_min - 0.1, C[1], 0], [x_max + 0.3, C[1], 0], buff=0,
                       color=MUT, stroke_width=2, tip_length=0.18)
        asse_y = Arrow([C[0], y_min - 0.1, 0], [C[0], y_max + 0.3, 0], buff=0,
                       color=MUT, stroke_width=2, tip_length=0.18)
        lab_x = MathTex(r"x", font_size=28, color=MUT).move_to([x_max + 0.3, C[1] - 0.3, 0])
        lab_y = MathTex(r"y", font_size=28, color=MUT).move_to([C[0] + 0.3, y_max + 0.3, 0])

        self.play(
            LaggedStart(*[Create(l) for l in linee_vert], lag_ratio=0.04, run_time=0.9),
            Succession(Wait(0.35), LaggedStart(*[Create(l) for l in linee_oriz], lag_ratio=0.04, run_time=0.9)),
            Succession(Wait(0.85), Create(asse_y, run_time=0.6, rate_func=SMOOTH)),
            Succession(Wait(1.15), Create(asse_x, run_time=0.6, rate_func=SMOOTH)),
        )

        self.play(Write(lab_y), Write(lab_x), run_time=0.5)
        self.wait(0.2)

        cerchio = Circle(radius=R, color=MUT, stroke_width=3).move_to(C)
        dot_O = Dot(O, radius=0.07, color=FG)
        dot_A = Dot(A, radius=0.07, color=FG)
        lab_O = MathTex(r"O", font_size=36, color=FG).next_to(dot_O, DL, buff=0.12)
        lab_A = MathTex(r"A", font_size=36, color=FG).next_to(dot_A, DR, buff=0.12)
        raggio_OA = Line(O, A, color=FG, stroke_width=3)
        uno_OA = MathTex(r"1", font_size=30, color=MUT).next_to(raggio_OA, DOWN, buff=0.15)

        self.play(Create(cerchio), run_time=1.2, rate_func=SMOOTH)
        self.play(FadeIn(dot_O, scale=0.5), Write(lab_O), run_time=0.5)
        self.play(
            Create(raggio_OA),
            FadeIn(dot_A, scale=0.5), Write(lab_A),
            run_time=0.8, rate_func=SMOOTH,
        )
        self.play(Write(uno_OA), run_time=0.4)
        self.wait(0.4)

        # Punto B a 2theta e corda AB
        raggio_OB = Line(O, B, color=FG, stroke_width=3)
        dot_B = Dot(B, radius=0.07, color=FG)
        lab_B = MathTex(r"B", font_size=36, color=FG).move_to(pos_B(2 * TH))
        uno_OB = MathTex(r"1", font_size=30, color=MUT).next_to(raggio_OB, RIGHT, buff=0).shift(UP * 0.2, LEFT * 0.15)

        arco_2t = Arc(radius=0.65, start_angle=0, angle=2 * TH, arc_center=O,
                      color=GIALLO, stroke_width=3.5)
        lab_2t = MathTex(r"2\theta", font_size=30, color=GIALLO).move_to(P(TH, 1.1))

        corda = Line(A, B, color=FG, stroke_width=5)

        self.play(
            Create(raggio_OB),
            FadeIn(dot_B, scale=0.5), Write(lab_B),
            run_time=0.9, rate_func=SMOOTH,
        )
        self.play(Write(uno_OB), Create(arco_2t), Write(lab_2t), run_time=0.8)
        self.wait(0.3)
        self.play(Create(corda), run_time=0.9, rate_func=SMOOTH)
        self.wait(0.6)

        # La figura scorre a sinistra e lascia spazio ai passaggi
        SHIFT_VEC = LEFT * 3.4
        elementi_da_spostare = [
            griglia, asse_x, asse_y, lab_x, lab_y,
            cerchio, dot_O, lab_O, raggio_OA, uno_OA, dot_A, lab_A,
            raggio_OB, uno_OB, dot_B, lab_B, arco_2t, lab_2t, corda
        ]

        self.play(
            *[m.animate.shift(SHIFT_VEC) for m in elementi_da_spostare],
            run_time=1.3,
            rate_func=EASE,
        )
        self.wait(0.3)

        C += SHIFT_VEC
        O = C.copy()
        A = P(0)
        B = P(2 * TH)
        M = (A + B) / 2

        X_L = 0.7
        ys = [2.9, 1.9, 0.9, -0.1, -1.1, -2.1]

        def riga(m, y):
            return m.move_to([0, y, 0]).align_to([X_L, 0, 0], LEFT)

        # Triangolo isoscele OAB
        r1 = riga(
            MathTex(r"OA", r"=", r"OB", r"=", r"1", font_size=36, color=FG),
            ys[0],
        )
        r1b = MathTex(r"\Rightarrow\ \triangle OAB\ \text{isoscele}", font_size=36, color=FG)
        r1b.next_to(r1, RIGHT, buff=0.4)

        tri_iso = Polygon(O, A, B, color=FG, stroke_width=0, fill_color=FG, fill_opacity=0.08)

        self.play(FadeIn(tri_iso), Write(r1), run_time=0.9)
        self.play(Write(r1b), run_time=0.8)
        self.wait(1.0)

        # OM e' mediana, altezza e bisettrice
        dot_M = Dot(M, radius=0.07, color=FG)
        lab_M = MathTex(r"M", font_size=34, color=FG).move_to(pos_M(2 * TH))
        seg_OM = Line(O, M, color=FG, stroke_width=3)

        u = (A - M) / np.linalg.norm(A - M)
        v = (O - M) / np.linalg.norm(O - M)
        s = 0.20
        angolo_retto = VMobject(color=FG, stroke_width=2.5).set_points_as_corners(
            [M + s * u, M + s * u + s * v, M + s * v]
        )

        arco_t1 = Arc(radius=0.65, start_angle=0, angle=TH, arc_center=O,
                      color=GIALLO, stroke_width=3.5)
        arco_t2 = Arc(radius=0.65, start_angle=TH, angle=TH, arc_center=O,
                      color=GIALLO, stroke_width=3.5)
        lab_t1 = MathTex(r"\theta", font_size=28, color=GIALLO).move_to(P(TH / 2, 1.05))
        lab_t2 = MathTex(r"\theta", font_size=28, color=GIALLO).move_to(P(3 * TH / 2, 1.05))

        r2 = riga(
            MathTex(r"OM", r"\perp", r"AB", r",\quad",
                    r"\widehat{AOM}", r"=", r"\widehat{MOB}", r"=", r"\theta",
                    font_size=36, color=FG),
            ys[1],
        )
        r2[4].set_color(GIALLO)
        r2[6].set_color(GIALLO)
        r2[8].set_color(GIALLO)

        self.play(FadeOut(lab_2t), run_time=0.2)

        self.remove(arco_2t)
        self.add(arco_t1, arco_t2)
        self.play(
            FadeIn(dot_M, scale=0.5), Write(lab_M),
            Create(seg_OM),
            run_time=0.8, rate_func=SMOOTH,
        )
        self.play(Create(angolo_retto), run_time=0.35)

        self.play(Write(lab_t1), Write(lab_t2), run_time=0.35)
        self.play(Write(r2), run_time=1.2)
        self.wait(1.2)

        # Nel triangolo rettangolo OMA, AM = sin(theta)
        tri_OMA = Polygon(O, M, A, color=C_AM, stroke_width=0,
                          fill_color=C_AM, fill_opacity=0.25)
        seg_AM = Line(A, M, color=C_AM, stroke_width=6)

        norm_dir = (M - O) / np.linalg.norm(M - O)
        lab_AM = crea_testo_con_ombra(r"\sin\theta", font_size=26, color=C_AM).move_to(
            (A + M) / 2 + 0.24 * norm_dir
        )

        r3 = riga(
            MathTex(r"AM", r"=", r"OA\cdot", r"\sin\theta", r"=", r"\sin\theta",
                    font_size=36, color=FG),
            ys[2],
        )
        r3[0].set_color(C_AM)
        r3[3].set_color(C_AM)
        r3[5].set_color(C_AM)

        self.play(FadeIn(tri_OMA), Create(seg_AM), run_time=0.9)
        self.play(Write(lab_AM), Write(r3), run_time=1.1)
        self.wait(1.2)

        # Stesso discorso per MB
        tri_OMB = Polygon(O, M, B, color=C_MB, stroke_width=0,
                          fill_color=C_MB, fill_opacity=0.25)
        seg_MB = Line(M, B, color=C_MB, stroke_width=6)
        lab_MB = crea_testo_con_ombra(r"\sin\theta", font_size=26, color=C_MB).move_to(
            (M + B) / 2 + 0.24 * norm_dir
        )

        self.play(FadeIn(tri_OMB), Create(seg_MB), run_time=0.9)
        self.play(Write(lab_MB), run_time=0.6)
        self.wait(1.0)

        self.play(
            corda.animate.set_color(C_AB),
            seg_AM.animate.set_color(C_AB),
            seg_MB.animate.set_color(C_AB),
            run_time=0.8,
        )
        self.wait(0.2)

        T = pos_T(2 * TH)
        due_lab = crea_testo_con_ombra(r"2", font_size=30, color=C_AB).move_to(T + LEFT * 0.30)

        self.play(
            lab_AM.animate.move_to(T + RIGHT * 0.15).set_color(C_AB),
            lab_MB.animate.move_to(T + RIGHT * 0.15).set_color(C_AB),
            FadeIn(due_lab, shift=RIGHT * 0.15),
            run_time=1.0,
            rate_func=SMOOTH,
        )
        self.wait(0.3)

        r4 = riga(
            MathTex(r"AB", r"=", r"2\,AM", r"=", r"2\sin\theta",
                    font_size=36, color=FG),
            ys[3],
        )
        r4[0].set_color(C_AB)
        r4[4].set_color(C_AB)

        self.play(Write(r4), run_time=1.1)
        self.play(Indicate(r4[4], color=C_AB, scale_factor=1.15), run_time=0.8)
        self.wait(1.0)

        # AB^2 = 4 sin^2(theta) = n
        r5 = riga(
            MathTex(r"AB^2", r"=", r"(2\sin\theta)^2", r"=", r"4\sin^2\theta", r"=", r"n",
                    font_size=36, color=FG),
            ys[4],
        )
        r5[0].set_color(C_AB)
        r5[2].set_color(C_AB)
        r5[4].set_color(C_AB)
        r5[6].set_color(VERDE)

        self.play(Write(r5), run_time=1.4)
        self.wait(0.7)
        self.play(Indicate(r5[6], color=VERDE, scale_factor=1.35), run_time=0.8)
        self.wait(0.8)

        r6 = riga(
            MathTex(r"AB", r"=", r"\sqrt{", r"n", r"}", font_size=44, color=FG),
            ys[5],
        )
        r6[0].set_color(C_AB)
        r6[3].set_color(VERDE)
        box = SurroundingRectangle(r6, color=VERDE, buff=0.2, stroke_width=3)

        self.play(Write(r6), run_time=1.1)
        self.play(Create(box), run_time=0.7)
        self.wait(1.2)

        self.play(FadeOut(uno_OB), run_time=0.5)
        self.wait(0.1)

        # B si muove da 0 a 180 gradi e torna
        t = ValueTracker(2 * TH)

        def aggiorna_geometria(mob=None):
            a = t.get_value()
            th = a / 2
            Bp = P(a)
            Mp = (A + Bp) / 2

            dot_B.move_to(Bp)
            lab_B.move_to(pos_B(a))
            raggio_OB.set_points_as_corners([O, Bp])
            corda.set_points_as_corners([A, Bp])
            tri_iso.set_points_as_corners([O, A, Bp, O])

            dot_M.move_to(Mp)
            lab_M.move_to(pos_M(a))
            seg_OM.set_points_as_corners([O, Mp])
            seg_AM.set_points_as_corners([A, Mp])
            seg_MB.set_points_as_corners([Mp, Bp])
            tri_OMA.set_points_as_corners([O, Mp, A, O])
            tri_OMB.set_points_as_corners([O, Mp, Bp, O])

            lun_a = np.linalg.norm(A - Mp)
            lun_o = np.linalg.norm(O - Mp)
            if lun_a < 1e-3 or lun_o < 1e-3:
                angolo_retto.set_points_as_corners([Mp, Mp, Mp])
            else:
                uu = (A - Mp) / lun_a
                vv = (O - Mp) / lun_o
                ss = min(0.20, 0.35 * min(lun_a, lun_o))
                angolo_retto.set_points_as_corners(
                    [Mp + ss * uu, Mp + ss * uu + ss * vv, Mp + ss * vv]
                )

            th_c = max(th, 1e-3)
            arco_t1.become(Arc(radius=0.65, start_angle=0, angle=th_c, arc_center=O,
                               color=GIALLO, stroke_width=3.5))
            arco_t2.become(Arc(radius=0.65, start_angle=th, angle=th_c, arc_center=O,
                               color=GIALLO, stroke_width=3.5))
            lab_t1.move_to(P(th / 2, 1.05))
            lab_t2.move_to(P(3 * th / 2, 1.05))
            op = float(np.clip(th / (12 * DEGREES), 0, 1))
            lab_t1.set_opacity(op)
            lab_t2.set_opacity(op)

            Tp = pos_T(a)
            lab_AM.move_to(Tp + RIGHT * 0.15)
            lab_MB.move_to(Tp + RIGHT * 0.15)
            due_lab.move_to(Tp + LEFT * 0.30)

        cerchio.add_updater(aggiorna_geometria)

        self.play(t.animate.set_value(PI), run_time=1.9, rate_func=EASE)
        self.wait(0.2)

        self.play(t.animate.set_value(0.001), run_time=3.7, rate_func=EASE)
        self.wait(0.2)

        self.play(t.animate.set_value(2 * TH), run_time=2.7, rate_func=EASE)
        self.wait(1.5)

        cerchio.remove_updater(aggiorna_geometria)

        self.wait(3.0)

        da_mantenere = {
            griglia, asse_x, asse_y, lab_x, lab_y,
            cerchio, dot_O, lab_O, dot_A, lab_A,
            raggio_OA, uno_OA
        }
        sub_mantenere = set()
        for mob in da_mantenere:
            sub_mantenere.update(mob.get_family())

        da_rimuovere = [m for m in self.mobjects if m not in sub_mantenere]
        self.play(*[FadeOut(m) for m in da_rimuovere], run_time=1.0)
        self.wait(0.5)