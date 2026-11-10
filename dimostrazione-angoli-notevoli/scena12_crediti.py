import numpy as np
from common import *


class Scena12Crediti(Scene):
    """Crediti finali: cielo di stelle, nome con gradiente e scintille."""

    def construct(self):
        SMOOTH = rate_functions.ease_in_out_sine
        rng = np.random.RandomState(7)

        def colore_gradiente(u):
            u = float(np.clip(u, 0, 1))
            if u < 0.5:
                return interpolate_color(ManimColor(ARANCIO), ManimColor(ROSA), u * 2)
            return interpolate_color(ManimColor(ROSA), ManimColor(BLU), (u - 0.5) * 2)

        # ================= CIELO DI STELLE =================
        palette = [FG, ARANCIO, BLU, ROSA]
        stelle = VGroup()
        basi, freq, fasi = [], [], []
        for _ in range(75):
            d = Dot(
                [rng.uniform(-7.1, 7.1), rng.uniform(-4.0, 4.0), 0],
                radius=rng.uniform(0.014, 0.038),
                color=palette[rng.randint(4)],
            ).set_z_index(-5)
            stelle.add(d)
            basi.append(rng.uniform(0.25, 0.65))
            freq.append(rng.uniform(0.8, 2.2))
            fasi.append(rng.uniform(0, 2 * PI))

        tempo = ValueTracker(0.0)
        visibili = ValueTracker(0.0)
        tempo.add_updater(lambda m, dt: m.increment_value(dt))

        def brilla(gruppo):
            t = tempo.get_value()
            v = visibili.get_value()
            for s, b, f, p in zip(gruppo, basi, freq, fasi):
                o = b + 0.25 * np.sin(f * t + p)
                s.set_fill(opacity=float(np.clip(o, 0.05, 0.9)) * v)

        stelle.add_updater(brilla)
        self.add(tempo, stelle)
        self.play(visibili.animate(rate_func=SMOOTH, run_time=1.8).set_value(1.0))

        # ================= CREDITI =================
        creato = Tex("Creato da", font_size=38, color=MUT)
        nome = Tex("Federico Ardesi", font_size=88)
        nome.set_color_by_gradient(ARANCIO, ROSA, BLU)
        creato.move_to([0, 1.25, 0])
        nome.move_to([0, 0.15, 0])

        x_l, x_r = nome.get_left()[0], nome.get_right()[0]
        y_barra = nome.get_bottom()[1] - 0.35
        n_seg = 60
        passo = (x_r - x_l) / n_seg
        segmenti = VGroup(*[
            Line(
                [x_l + i * passo, y_barra, 0],
                [x_l + (i + 1) * passo, y_barra, 0],
                color=colore_gradiente(i / (n_seg - 1)),
                stroke_width=5,
            )
            for i in range(n_seg)
        ])
        brillio = Line([x_l, y_barra, 0], [x_r, y_barra, 0], color=WHITE, stroke_width=7.5)

        sotto = Tex("Seno e coseno degli angoli notevoli", font_size=30, color=MUT)
        sotto.move_to([0, y_barra - 0.65, 0])

        # Sequenza crediti
        self.play(FadeIn(creato, shift=UP * 0.2), run_time=0.9, rate_func=SMOOTH)
        self.play(Write(nome), run_time=2.0)

        # Barra e lampo di scorrimento sincronizzati da sinistra a destra
        self.play(
            LaggedStart(*[FadeIn(s, scale=0.9) for s in segmenti], lag_ratio=0.015),
            ShowPassingFlash(brillio, time_width=0.35, rate_func=rate_functions.ease_out_sine),
            run_time=1.2,
        )

        # Sottotitolo e scintille insieme
        self.play(
            FadeIn(sotto, shift=UP * 0.12),
            LaggedStart(
                Flash(
                    [x_r + 0.35, nome.get_top()[1] + 0.05, 0],
                    color=ROSA,
                    num_lines=6,
                    line_length=0.35,
                    flash_radius=0.18,
                    line_stroke_width=3.5,
                    run_time=0.9,
                ),
                Flash(
                    [x_l - 0.25, nome.get_top()[1] - 0.05, 0],
                    color=ARANCIO,
                    num_lines=6,
                    line_length=0.28,
                    flash_radius=0.15,
                    line_stroke_width=3,
                    run_time=0.8,
                ),
                Flash(
                    [x_r - 0.8, y_barra, 0],
                    color=BLU,
                    num_lines=5,
                    line_length=0.22,
                    flash_radius=0.14,
                    line_stroke_width=3,
                    run_time=0.8,
                ),
                lag_ratio=0.25,
            ),
            run_time=1.4,
        )

        self.wait(3.0)

        # Chiusura morbida
        self.play(
            FadeOut(creato, nome, segmenti, sotto, shift=DOWN * 0.1),
            visibili.animate.set_value(0.0),
            run_time=1.4,
            rate_func=SMOOTH,
        )
        self.wait(0.3)