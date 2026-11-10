import numpy as np
from common import *


class Scena07Coordinate(Scene):
    """Passo 3: AB^2 = 2 - 2 cos(2theta) con le coordinate."""

    def construct(self):
        EASE = rate_functions.ease_in_out_cubic
        SMOOTH = rate_functions.ease_in_out_sine

        C_COS = BLU
        C_SIN = ARANCIO
        C_AB = BLU
        FS = 31

        R = 2.6
        C = np.array([-3.4, -0.2, 0.0])
        O = C.copy()
        TH = 38 * DEGREES
        a = 2 * TH

        def P(ang, r=R):
            return C + r * np.array([np.cos(ang), np.sin(ang), 0.0])

        def dirz(ang):
            return np.array([np.cos(ang), np.sin(ang), 0.0])

        A = P(0)
        B = P(a)
        Hx = np.array([B[0], C[1], 0.0])

        def crea_testo_con_ombra(latex, font_size, color):
            t_ = MathTex(latex, font_size=font_size, color=color)
            t_.set_stroke(color=BLACK, width=2.4, opacity=0.95, background=True)
            return t_

        def pos_B(ang):
            return P(ang) + 0.38 * dirz(ang) + 0.12 * UP

        def pos_uno(ang, lato=1):
            nrm = np.array([-np.sin(ang), np.cos(ang), 0.0])
            return P(ang, R / 2) + lato * 0.32 * nrm

        def angolo_retto(V, p1, p2, s=0.22, color=FG):
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

        def riga_uguale(m, i, rif):
            """Come riga(), ma l'= della riga cade sotto l'= di rif."""
            m.move_to([0, ys[i], 0])
            m.shift(RIGHT * (rif.get_center()[0] - m[0].get_center()[0]))
            return m

        titolo = MathTex(r"AB", r"\text{ con le coordinate}", font_size=38, color=FG)
        titolo[0].set_color(C_AB)
        titolo.move_to([0, 3.55, 0]).align_to([X_L, 0, 0], LEFT)
        self.play(Write(titolo), run_time=0.9)
        self.wait(0.2)

        # A e B con le coordinate
        raggio_OB = Line(O, B, color=FG, stroke_width=3)
        dot_B = Dot(B, radius=0.07, color=FG)
        lab_B = MathTex(r"B", font_size=36, color=FG).move_to(pos_B(a))

        arco_2t = Arc(radius=0.46, start_angle=0, angle=a, arc_center=O,
                      color=GIALLO, stroke_width=3.2)
        lab_2t = MathTex(r"2\theta", font_size=26, color=GIALLO).move_to(P(TH, 0.80)).shift(UP*0.1, LEFT*0.3)
        corda = Line(A, B, color=FG, stroke_width=5)

        r1 = riga(
            MathTex(r"A", r"=(1,0),\quad ", r"B", r"=(", r"\cos2\theta", r",", r"\sin2\theta", r")",
                    font_size=FS, color=FG),
            0,
        )
        r1[4].set_color(C_COS)
        r1[6].set_color(C_SIN)

        self.play(
            Create(raggio_OB),
            FadeIn(dot_B, scale=0.5), Write(lab_B),
            Create(arco_2t), Write(lab_2t),
            run_time=0.9, rate_func=SMOOTH,
        )
        self.play(Create(corda), run_time=0.8, rate_func=SMOOTH)
        self.play(Write(r1), run_time=1.1)
        self.wait(0.8)

        # Pitagora sulla corda
        tri_AHB = Polygon(A, Hx, B, stroke_width=0, fill_color=FG, fill_opacity=0.08)
        leg_h = Line(A, Hx, color=C_COS, stroke_width=6)
        leg_v = Line(Hx, B, color=C_SIN, stroke_width=6)
        marca_H1 = angolo_retto(Hx, A, B, s=0.22, color=FG)

        lab_leg_h = crea_testo_con_ombra(r"1-\cos2\theta", 26, C_COS).move_to(
            (A + Hx) / 2 + 0.36 * DOWN
        )
        lab_leg_v = crea_testo_con_ombra(r"\sin2\theta", 26, C_SIN).move_to(
            (Hx + B) / 2 + 0.50 * RIGHT
        )
        lab_AB = crea_testo_con_ombra(r"AB", 28, C_AB).move_to(
            (A + B) / 2 + 0.32 * dirz(TH)
        )

        r2 = riga(
            MathTex(r"AB^2", r"=", r"(\cos2\theta-1)^2", r"+", r"(\sin2\theta-0)^2",
                    font_size=FS, color=FG),
            1,
        )
        r2[0].set_color(C_AB)
        r2[2].set_color(C_COS)
        r2[4].set_color(C_SIN)

        self.play(FadeOut(uno_OA), run_time=0.4)
        self.play(
            FadeIn(tri_AHB),
            Create(leg_h), Create(leg_v), Create(marca_H1),
            run_time=0.9, rate_func=SMOOTH,
        )
        self.bring_to_front(dot_A, dot_B, dot_O)
        self.play(Write(lab_leg_h), Write(lab_leg_v), Write(lab_AB), run_time=0.8)
        self.play(Write(r2), run_time=1.3)
        self.wait(1.0)

        # Sviluppo dei quadrati
        r3 = riga_uguale(
            MathTex(r"=", r"\cos^2 2\theta", r"-2\cos2\theta", r"+1", r"+", r"\sin^2 2\theta",
                    font_size=FS, color=FG),
            2, r2[1],
        )
        r3[1].set_color(C_COS)
        r3[2].set_color(C_COS)
        r3[5].set_color(C_SIN)

        self.play(Write(r3), run_time=1.3)
        self.wait(1.0)

        # cos^2 + sin^2 = 1 nel triangolo O-H-B
        tri_OHB = Polygon(O, Hx, B, stroke_width=0, fill_color=FG, fill_opacity=0.08)
        seg_cos = Line(O, Hx, color=C_COS, stroke_width=6)
        marca_H2 = angolo_retto(Hx, O, B, s=0.22, color=FG)
        lab_cos = crea_testo_con_ombra(r"\cos2\theta", 26, C_COS).move_to(
            (O + Hx) / 2 + 0.38 * RIGHT + 0.32 * DOWN
        )
        uno_OB = MathTex(r"1", font_size=30, color=MUT).move_to(pos_uno(a, lato=1)).shift(RIGHT*0.15, UP*0.5)

        r4 = riga_uguale(
            MathTex(r"=", r"1", r"-2\cos2\theta", r"+1", font_size=FS, color=FG),
            3, r2[1],
        )
        r4[2].set_color(C_COS)

        r5 = riga_uguale(
            MathTex(r"=", r"2", r"-2\cos2\theta", font_size=FS, color=FG),
            4, r2[1],
        )
        r5[2].set_color(C_COS)

        self.play(
            FadeOut(tri_AHB), FadeOut(leg_h), FadeOut(lab_leg_h),
            FadeOut(marca_H1), FadeOut(lab_AB),
            corda.animate.set_stroke(opacity=0.3),
            run_time=0.6,
        )
        self.play(
            FadeIn(tri_OHB), Create(seg_cos), Create(marca_H2),
            Write(lab_cos), Write(uno_OB),
            run_time=1.0, rate_func=SMOOTH,
        )
        self.bring_to_front(dot_A, dot_B, dot_O)
        self.wait(0.3)
        self.play(
            Indicate(r3[1], color=C_COS, scale_factor=1.2),
            Indicate(r3[5], color=C_SIN, scale_factor=1.2),
            run_time=0.9,
        )
        self.play(Write(r4), run_time=0.9)
        self.play(Write(r5), run_time=0.9)
        r_concl = MathTex(
            r"\Rightarrow\;",
            r"AB^2",
            r"=",
            r"2-2",
            r"\cos2\theta",
            font_size=36,
            color=FG,
        )
        r_concl[1].set_color(C_AB)
        r_concl[4].set_color(C_COS)

        r_concl.move_to([0, -0.15, 0]).align_to([X_L, 0, 0], LEFT)

        self.play(Write(r_concl), run_time=0.8)
        self.wait(1.0)

        # Da AB^2 = n a cos(2theta) = 1 - n/2
        dash = DashedLine(B, Hx, color=MUT, stroke_width=2)

        f1 = riga(
            MathTex(r"n", r"=", r"AB^2", r"=", r"2-2", r"\cos2\theta",
                    font_size=38, color=FG),
            0,
        )
        f1[0].set_color(VERDE)
        f1[2].set_color(C_AB)
        f1[5].set_color(C_COS)

        f2 = riga(
            MathTex(r"2", r"\cos2\theta", r"=", r"2-", r"n", font_size=38, color=FG),
            1,
        )
        f2[1].set_color(C_COS)
        f2[4].set_color(VERDE)

        f3 = MathTex(r"\cos2\theta", r"=", r"1-", r"\dfrac{n}{2}", font_size=42, color=FG)
        f3.move_to([0, 0.85, 0]).align_to([X_L, 0, 0], LEFT)
        f3[0].set_color(C_COS)
        f3[3].set_color(VERDE)
        box_f3 = SurroundingRectangle(f3, color=VERDE, buff=0.18, stroke_width=2.5)

        self.play(
            FadeOut(VGroup(r1, r2, r3, r4, r5)),
            FadeOut(tri_OHB), FadeOut(marca_H2), FadeOut(uno_OB),
            FadeOut(leg_v), FadeOut(lab_leg_v), FadeOut(seg_cos), FadeOut(lab_cos),
            corda.animate.set_stroke(opacity=0.6),
            run_time=0.7,
        )
        self.play(Create(dash), Write(f1), run_time=1.0)
        self.wait(0.4)
        self.play(Write(f2), run_time=0.9)
        self.wait(0.3)
        self.play(Write(f3), run_time=1.0)
        self.play(Create(box_f3), run_time=0.7)
        self.wait(3.0)

        # Resta solo la base della figura
        da_mantenere = VGroup(
            griglia, asse_x, asse_y, lab_x, lab_y,
            cerchio, dot_O, lab_O, raggio_OA, dot_A, lab_A,
        )
        sub_mantenere = set(da_mantenere.get_family())
        da_rimuovere = [m for m in self.mobjects if m not in sub_mantenere]
        self.play(*[FadeOut(m) for m in da_rimuovere], run_time=1.0)
        self.wait(0.5)