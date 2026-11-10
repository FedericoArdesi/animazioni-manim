import numpy as np
from common import *


class Scena02Salti(Scene):
    """n sale di 1 alla volta, l'angolo a passi di 30, 15, 15, 30 gradi."""

    def construct(self):
        # Griglia a due righe: n sopra, theta sotto
        linea_centro = Line(LEFT * 6, RIGHT * 5.6, color=MUT, stroke_width=2)

        x_sep = -4.3
        linea_vert = Line(
            [x_sep, 1.7, 0], [x_sep, -1.7, 0],
            color=MUT, stroke_width=1.5, stroke_opacity=0.5
        )

        x_lab = -5.1
        lab_n = MathTex(r"n", font_size=50, color=VERDE).move_to([x_lab, 0.9, 0])
        lab_theta = MathTex(r"\theta", font_size=50, color=FG).move_to([x_lab, -0.9, 0])

        self.play(Create(linea_centro), Create(linea_vert), run_time=0.75)
        self.play(
            Write(lab_n),
            Write(lab_theta),
            run_time=0.75,
        )
        self.wait(0.2)

        # Dati e posizioni delle cinque colonne
        valori_n = [0, 1, 2, 3, 4]
        angoli = [0, 30, 45, 60, 90]
        salti_theta = [30, 15, 15, 30]

        xs = [-3.2, -1.2, 0.8, 2.8, 4.8]
        y_n = 0.9
        y_theta = -0.9

        n_0 = MathTex(r"0", font_size=42, color=VERDE).move_to([xs[0], y_n, 0])
        theta_0 = MathTex(r"0^\circ", font_size=42, color=FG).move_to([xs[0], y_theta, 0])

        self.play(
            GrowFromCenter(n_0, rate_func=rate_functions.ease_out_back),
            GrowFromCenter(theta_0, rate_func=rate_functions.ease_out_back),
            run_time=0.35,
        )
        self.wait(0.15)

        # Un salto per volta: +1 su n, salto variabile su theta
        for k in range(4):
            x_start = xs[k]
            x_end = xs[k + 1]
            x_mid = (x_start + x_end) / 2

            arco_n = CurvedArrow(
                np.array([x_start + 0.25, y_n + 0.35, 0]),
                np.array([x_end - 0.25, y_n + 0.35, 0]),
                angle=-PI / 2,
                color=VERDE,
                stroke_width=2.5,
            )
            lbl_n = MathTex(
                r"+1",
                font_size=28,
                color=VERDE,
            ).move_to([x_mid, y_n + 1.25, 0])

            arco_theta = CurvedArrow(
                np.array([x_start + 0.30, y_theta - 0.35, 0]),
                np.array([x_end - 0.30, y_theta - 0.35, 0]),
                angle=PI / 2,
                color=GIALLO,
                stroke_width=2.5,
            )
            lbl_theta = MathTex(
                rf"+{salti_theta[k]}^\circ",
                font_size=28,
                color=GIALLO,
            ).move_to([x_mid, y_theta - 1.25, 0])

            num_n = MathTex(
                str(valori_n[k + 1]),
                font_size=42,
                color=VERDE,
            ).move_to([x_end, y_n, 0])

            num_theta = MathTex(
                rf"{angoli[k + 1]}^\circ",
                font_size=42,
                color=FG,
            ).move_to([x_end, y_theta, 0])

            self.play(
                LaggedStart(
                    AnimationGroup(
                        GrowFromPoint(arco_n, arco_n.get_start()),
                        FadeIn(lbl_n, shift=UP * 0.15),
                        GrowFromPoint(arco_theta, arco_theta.get_start()),
                        FadeIn(lbl_theta, shift=DOWN * 0.15),
                        run_time=0.5,
                    ),
                    AnimationGroup(
                        GrowFromPoint(num_n, arco_n.get_end(), rate_func=rate_functions.ease_out_back),
                        GrowFromPoint(num_theta, arco_theta.get_end(), rate_func=rate_functions.ease_out_back),
                        run_time=0.35,
                    ),
                    lag_ratio=0.70,
                )
            )
            self.wait(0.15)

        # Pausa finale sulla riga completa
        self.wait(3)
        self.play(FadeOut(*self.mobjects))
        self.wait(1)