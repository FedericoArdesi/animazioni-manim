import numpy as np
from common import *


class Scena04Passo1(Scene):
    """Passo 1: dalla tesi a n = 4 sin^2(theta)."""

    def construct(self):
        font_sz = 52
        Y_BASE = 1.2
        SMOOTH = rate_functions.ease_in_out_sine

        def salto(h):
            """Restituisce una path_func con arco parabolico di altezza h (UP * h * sin(PI * a))."""
            return lambda s, e, a: (1 - a) * s + a * e + UP * h * np.sin(PI * a)

        def tpl(*parti):
            """Template di sola posizione: da qui prendo i centri finali di ogni pezzo."""
            return MathTex(*parti, font_size=font_sz, color=FG).move_to([0, Y_BASE, 0])

        # Formula di partenza
        uguale = MathTex(r"=", font_size=font_sz, color=FG).move_to([0, Y_BASE, 0])
        sin_theta = MathTex(r"\sin", r"\theta", font_size=font_sz, color=ARANCIO)
        sin_theta.next_to(uguale, LEFT, buff=0.35)

        n_mob = MathTex(r"n", font_size=font_sz, color=VERDE)
        l = n_mob.get_left()[0] - 0.42
        r = n_mob.get_right()[0] + 0.12
        top = n_mob.get_top()[1] + 0.14
        bot = n_mob.get_bottom()[1] - 0.06
        mid = (top + bot) / 2
        rad_sym = VMobject(color=FG, stroke_width=3.5)
        rad_sym.set_points_as_corners([
            [l, mid - 0.02, 0],
            [l + 0.09, mid + 0.04, 0],
            [l + 0.22, bot, 0],
            [l + 0.36, top, 0],
            [r, top, 0],
        ])
        radice = VGroup(rad_sym, n_mob)

        due_den = MathTex(r"2", font_size=font_sz, color=FG)

        w_num = radice.get_width()
        linea_frac = Line(
            LEFT * (w_num / 2 + 0.15),
            RIGHT * (w_num / 2 + 0.15),
            stroke_width=2.5,
            color=FG,
        ).move_to([0.85, Y_BASE, 0])

        radice.next_to(linea_frac, UP, buff=0.15)
        due_den.next_to(linea_frac, DOWN, buff=0.15)

        formula_iniziale = VGroup(sin_theta, uguale, linea_frac, radice, due_den)
        formula_iniziale.move_to([0, Y_BASE, 0])

        # Tabella delle condizioni sotto la formula
        c1 = MathTex(r"n", r"\in \{0,1,2,3,4\}", font_size=32, color=MUT)
        c1[0].set_color(VERDE)
        c2 = MathTex(r"n", r"\ge 0", font_size=32, color=MUT)
        c2[0].set_color(VERDE)
        c3 = MathTex(r"0^\circ \le \theta \le 90^\circ", font_size=32, color=MUT)
        c4 = MathTex(r"\sin\theta", r"\ge 0", font_size=32, color=MUT)
        c4[0].set_color(ARANCIO)

        w1 = max(c1.width, c3.width)
        w2 = max(c2.width, c4.width)
        pad, rh = 0.5, 0.7
        x_l = -(w1 / 2 + pad)
        x_r = w2 / 2 + pad
        c1.move_to([x_l, rh / 2, 0])
        c3.move_to([x_l, -rh / 2, 0])
        c2.move_to([x_r, rh / 2, 0])
        c4.move_to([x_r, -rh / 2, 0])
        tot_w = w1 + w2 + 4 * pad
        vline = Line([0, rh, 0], [0, -rh, 0], stroke_width=2, color=MUT)
        hline = Line([-tot_w / 2, 0, 0], [tot_w / 2, 0, 0], stroke_width=2, color=MUT)
        tabella_condizioni = VGroup(c1, c2, c3, c4, vline, hline).move_to([0, -2.0, 0])

        self.play(Write(formula_iniziale), run_time=1.6)
        self.wait(1)
        self.play(
            Create(hline, run_time=1.0, rate_func=SMOOTH),
            Create(vline, run_time=1.0, rate_func=SMOOTH),
            Write(VGroup(c1, c2), run_time=1.5),
            Write(VGroup(c3, c4), run_time=1.5)
        )
        self.wait(3.5)

        # Si toglie la frazione: il 2 salta a sinistra
        tB = tpl(r"2", r"\sin", r"\theta", r"=", r"n")
        d = n_mob.get_x() - rad_sym.get_left()[0]
        r_ext = rad_sym.get_right()[0] - n_mob.get_x()
        n_tx = tB[3].get_right()[0] + 0.3 + d
        left = tB[0].get_left()[0]
        right = n_tx + r_ext
        sh = RIGHT * (-(left + right) / 2)
        vec_rad = np.array([n_tx + sh[0] - n_mob.get_x(), tB[4].get_y() - n_mob.get_y(), 0])

        S = dict(run_time=0.7, rate_func=SMOOTH)
        self.play(
            AnimationGroup(
                Unwrite(linea_frac, run_time=0.4),
                AnimationGroup(
                    due_den.animate(path_arc=-0.6 * PI, **S).move_to(tB[0].get_center() + sh),
                    sin_theta[0].animate(**S).move_to(tB[1].get_center() + sh),
                    sin_theta[1].animate(**S).move_to(tB[2].get_center() + sh),
                    uguale.animate(**S).move_to(tB[3].get_center() + sh),
                    radice.animate(**S).shift(vec_rad),
                ),
                lag_ratio=0.5,
            )
        )
        self.wait(1.7)

        # Si toglie la radice: compaiono parentesi ed esponente
        tD = tpl(r"(", r"2", r"\sin", r"\theta", r")", r"^2", r"=", r"n")
        par_l = tD[0].copy()
        par_r = tD[4].copy()
        exp_2 = tD[5].copy()
        S2 = dict(run_time=0.8, rate_func=SMOOTH)

        self.play(
            Unwrite(rad_sym, run_time=0.5, reverse=True),
            GrowFromCenter(par_l, **S2),
            GrowFromCenter(par_r, **S2),
            GrowFromPoint(exp_2, exp_2.get_corner(DL), **S2),
            due_den.animate(**S2).move_to(tD[1].get_center()),
            sin_theta[0].animate(**S2).move_to(tD[2].get_center()),
            sin_theta[1].animate(**S2).move_to(tD[3].get_center()),
            uguale.animate(**S2).move_to(tD[6].get_center()),
            n_mob.animate(**S2).move_to(tD[7].get_center()),
        )
        self.wait(1.7)

        # I due membri si scambiano
        tE = tpl(r"n", r"=", r"(", r"2", r"\sin", r"\theta", r")", r"^2")
        lhs = VGroup(par_l, due_den, sin_theta, par_r, exp_2)
        dx_lhs = tE[2].get_x() - par_l.get_x()

        self.play(
            lhs.animate(path_func=salto(0.9)).shift(RIGHT * dx_lhs),
            uguale.animate.move_to(tE[1].get_center()),
            n_mob.animate(path_func=salto(-0.65)).move_to(tE[0].get_center()),
            run_time=1.5,
            rate_func=SMOOTH,
        )
        self.wait(0.7)

        # Forma finale n = 4 sin^2(theta)
        tF = tpl(r"n", r"=", r"4", r"\sin", r"^2", r"\theta")
        HB = 0.7
        HE = HB / 3

        copia_exp = exp_2.copy().set_color(FG)
        self.add(copia_exp)
        quattro_m = tF[2].copy().set_color(ARANCIO)

        self.play(
            ShrinkToCenter(par_l),
            ShrinkToCenter(par_r),
            ReplacementTransform(copia_exp, quattro_m, path_func=salto(HB)),
            FadeOut(due_den, target_position=tF[2].get_center()),
            sin_theta[0].animate.move_to(tF[3].get_center()),
            exp_2.animate(path_func=salto(HE)).move_to(tF[4].get_center()).set_color(ARANCIO),
            sin_theta[1].animate.move_to(tF[5].get_center()),
            n_mob.animate.move_to(tF[0].get_center()),
            uguale.animate.move_to(tF[1].get_center()),
            run_time=1.0,
            rate_func=SMOOTH,
        )

        self.wait(3)
        self.play(FadeOut(*self.mobjects), run_time=1.2)
        self.wait(1)