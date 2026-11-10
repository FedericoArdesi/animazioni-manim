import numpy as np
from common import *


class Scena10Riepilogo(Scene):
    """Riepilogo sul grafico: n, cos(2theta), sin(theta), cos(theta)."""

    def construct(self):
        EASE = rate_functions.ease_in_out_cubic
        SMOOTH = rate_functions.ease_in_out_sine
        POP = rate_functions.ease_out_back

        C_SIN = ARANCIO
        C_COS = BLU
        C_N = VERDE
        C_ANG = GIALLO

        x0, W = -5.4, 7.0
        y0, H = -1.8, 3.9
        X_R, MAXW_R = 2.6, 4.3
        X_T = -6.6

        angoli = [0, 30, 45, 60, 90]
        sin_v = [0.0, 0.5, np.sqrt(2) / 2, np.sqrt(3) / 2, 1.0]
        cos_v = sin_v[::-1]
        salti = [30, 15, 15, 30]
        ts = np.linspace(0, 90, 61)

        def gx(deg):
            return x0 + W * deg / 90.0

        def hs(v):
            return y0 + H * v

        def mix(c1, c2, u):
            return interpolate_color(ManimColor(c1), ManimColor(c2), u)

        def pannello(m, y):
            if m.width > MAXW_R:
                m.scale_to_fit_width(MAXW_R)
            m.move_to([0, y, 0])
            m.align_to([X_R, 0, 0], LEFT)
            return m

        def titolo_tex(*parti):
            t_ = MathTex(*parti, font_size=36, color=FG)
            t_.move_to([0, 3.4, 0]).align_to([X_T, 0, 0], LEFT)
            return t_

        # Costruttori della curva, dei punti e dei livelli
        def altezza(k, u):
            return y0 + H * ((1 - u) * k / 4 + u * sin_v[k])

        def curva(u, col=None):
            pts = [np.array([gx(t), y0 + H * ((1 - u) * np.sin(t * DEGREES) ** 2 + u * np.sin(t * DEGREES)), 0.0])
                   for t in ts]
            return VMobject(color=col or mix(C_N, C_SIN, u), stroke_width=5).set_points_smoothly(pts)

        def punto(k, u):
            return Dot([gx(angoli[k]), altezza(k, u), 0], radius=0.08, color=FG).set_z_index(10)

        def livello(k, u):
            h = altezza(k, u)
            return DashedLine([x0, h, 0], [gx(angoli[k]), h, 0], color=mix(C_N, C_SIN, u),
                              stroke_width=2, stroke_opacity=0.6, dash_length=0.08)

        def guida(k, u):
            return DashedLine([gx(angoli[k]), altezza(k, u), 0], [gx(angoli[k]), y0, 0], color=C_ANG,
                              stroke_width=2, stroke_opacity=0.6, dash_length=0.08)

        asse_x = Arrow([x0 - 0.2, y0, 0], [x0 + W + 0.45, y0, 0], buff=0,
                       color=MUT, stroke_width=2, tip_length=0.18)
        asse_y = Arrow([x0, y0 - 0.2, 0], [x0, y0 + H + 0.45, 0], buff=0,
                       color=MUT, stroke_width=2, tip_length=0.18)
        lab_th = MathTex(r"\theta", font_size=28, color=C_ANG).move_to([x0 + W + 0.45, y0 - 0.32, 0])
        yl_n = MathTex(r"n", font_size=30, color=C_N).move_to([x0, y0 + H + 0.68, 0])

        tk = [MathTex(rf"{a}^\circ", font_size=24, color=C_ANG).move_to([gx(a), y0 - 0.32, 0]) for a in angoli]
        lab_n = [MathTex(str(k), font_size=26, color=C_N).move_to([x0 - 0.45, hs(k / 4), 0]) for k in range(5)]

        # Atto A: n = 4 sin^2(theta), n sale a passi uguali
        tit_a = titolo_tex(r"\text{Il piano }(", r"\theta", r",\,", r"n", r")")
        tit_a[1].set_color(C_ANG)
        tit_a[3].set_color(C_N)

        self.play(Write(tit_a), run_time=0.8)
        self.play(Create(asse_x), Create(asse_y), run_time=0.9, rate_func=SMOOTH)
        self.play(Write(lab_th), Write(yl_n), run_time=0.6)
        self.wait(0.2)

        curva_n = curva(0.0)
        f_a = MathTex(r"n=(2\sin\theta)^2=4\sin^2\theta", font_size=34, color=FG)
        pannello(f_a, 2.5)

        self.play(Create(curva_n), Write(f_a), run_time=1.8, rate_func=SMOOTH)
        self.wait(0.4)

        pts = [punto(k, 0) for k in range(5)]
        lvl_s = {k: livello(k, 0) for k in range(1, 5)}
        gd_s = {k: guida(k, 0) for k in range(1, 5)}

        x_arr = x0 - 1.0
        arr = {k: Arrow([x_arr, hs((k - 1) / 4) + 0.06, 0], [x_arr, hs(k / 4) - 0.06, 0], buff=0,
                        color=C_N, stroke_width=2.5, tip_length=0.16) for k in range(1, 5)}
        plus = {k: MathTex(r"+1", font_size=24, color=C_N).move_to([x_arr - 0.4, hs((k - 0.5) / 4), 0])
                for k in range(1, 5)}

        arcs, lab_arcs = {}, {}
        for k in range(1, 5):
            xs_, xe_ = gx(angoli[k - 1]) + 0.14, gx(angoli[k]) - 0.14
            arcs[k] = ArcBetweenPoints(
                np.array([xs_, y0 - 0.72, 0.0]), np.array([xe_, y0 - 0.72, 0.0]),
                angle=PI / 3, color=C_ANG, stroke_width=2.5,
            ).add_tip(tip_length=0.16, tip_width=0.13)
            lab_arcs[k] = MathTex(rf"+{salti[k - 1]}^\circ", font_size=26, color=C_ANG).move_to(
                [(gx(angoli[k - 1]) + gx(angoli[k])) / 2, y0 - 1.38, 0]
            )

        self.play(
            GrowFromCenter(pts[0], rate_func=POP),
            FadeIn(lab_n[0]), FadeIn(tk[0]),
            run_time=0.4,
        )
        self.wait(0.15)

        for k in range(1, 5):
            self.play(
                LaggedStart(
                    AnimationGroup(
                        Create(lvl_s[k]),
                        FadeIn(lab_n[k], shift=RIGHT * 0.15),
                        GrowArrow(arr[k]),
                        FadeIn(plus[k], shift=DOWN * 0.1),
                        run_time=0.5,
                    ),
                    AnimationGroup(
                        GrowFromCenter(pts[k], rate_func=POP),
                        Create(gd_s[k]),
                        FadeIn(tk[k], shift=UP * 0.1),
                        run_time=0.4,
                    ),
                    AnimationGroup(
                        GrowFromPoint(arcs[k], arcs[k].get_start()),
                        FadeIn(lab_arcs[k], shift=DOWN * 0.15),
                        run_time=0.5,
                    ),
                    lag_ratio=0.70,
                )
            )
            self.wait(0.1)

        p_a1 = MathTex(r"n:\ +1,\ +1,\ +1,\ +1", font_size=32, color=C_N)
        p_a2 = MathTex(r"\theta:\ +30^\circ,\ +15^\circ,\ +15^\circ,\ +30^\circ", font_size=32, color=C_ANG)
        pannello(p_a1, 1.4)
        pannello(p_a2, 0.6)
        self.play(
            Write(p_a1),
            LaggedStart(*[Indicate(arr[k], color=C_N, scale_factor=1.15) for k in range(1, 5)], lag_ratio=0.2),
            run_time=1.2,
        )
        self.play(
            Write(p_a2),
            LaggedStart(*[Indicate(lab_arcs[k], color=C_ANG, scale_factor=1.25) for k in range(1, 5)], lag_ratio=0.2),
            run_time=1.4,
        )
        self.wait(1.4)

        # Atto B: stessa curva, scala di cos(2theta)
        tit_b = titolo_tex(r"\text{Stessa curva, altra scala: }", r"\cos2\theta")
        tit_b[1].set_color(C_COS)

        yl_c2 = MathTex(r"\cos2\theta", font_size=28, color=C_COS).move_to([x0 + 0.1, y0 + H + 0.68, 0])
        VAL_C2 = [r"1", r"\tfrac12", r"0", r"-\tfrac12", r"-1"]
        lab_c2 = [MathTex(v, font_size=26, color=C_COS).move_to([x0 - 0.45, hs(k / 4), 0])
                  for k, v in enumerate(VAL_C2)]

        self.play(
            FadeOut(VGroup(*arcs.values(), *lab_arcs.values(), *arr.values(), *plus.values(), p_a1, p_a2, f_a)),
            FadeTransform(tit_a, tit_b),
            run_time=0.8,
        )
        self.play(
            *[ReplacementTransform(lab_n[k], lab_c2[k], run_time=1.0) for k in range(5)],
            ReplacementTransform(yl_n, yl_c2, run_time=1.0),
        )

        f_b1 = MathTex(r"n", r"=", r"2-2", r"\cos2\theta", font_size=36, color=FG)
        f_b1[0].set_color(C_N)
        f_b1[3].set_color(C_COS)
        pannello(f_b1, 2.5)
        f_b2 = MathTex(r"\cos2\theta", r"=", r"1-", r"\dfrac{n}{2}", font_size=40, color=FG)
        f_b2[0].set_color(C_COS)
        f_b2[3].set_color(C_N)
        pannello(f_b2, 1.4)
        box_b2 = SurroundingRectangle(f_b2, color=C_N, buff=0.16, stroke_width=2.5)

        self.play(Write(f_b1), run_time=0.9)
        self.play(Write(f_b2), run_time=0.9)
        self.play(Create(box_b2), run_time=0.6)
        self.wait(0.5)

        def segmento(t0, t1):
            tt = np.linspace(t0, t1, 16)
            return VMobject(color=C_ANG, stroke_width=10).set_points_smoothly(
                [np.array([gx(t), y0 + H * np.sin(t * DEGREES) ** 2, 0.0]) for t in tt]
            )

        flat = VGroup(segmento(0, 30), segmento(60, 90))
        ripida = segmento(30, 60)

        p_b1 = MathTex(r"\text{curva piatta}", r"\Rightarrow", r"\text{salto lungo}", font_size=30, color=FG)
        p_b1[0].set_color(C_ANG)
        p_b2 = MathTex(r"\text{curva ripida}", r"\Rightarrow", r"\text{salto corto}", font_size=30, color=FG)
        p_b2[0].set_color(C_ANG)
        pannello(p_b1, 0.2)
        pannello(p_b2, -0.5)

        self.play(Write(p_b1), Create(flat), run_time=1.3)
        self.wait(0.9)
        self.play(FadeOut(flat), run_time=0.4)
        self.play(Write(p_b2), Create(ripida), run_time=1.3)
        self.wait(0.9)
        self.play(FadeOut(ripida), run_time=0.4)
        self.wait(0.3)

        # Atto C: l'altezza si schiaccia, n/4 diventa sqrt(n)/2
        tit_c = titolo_tex(r"\text{Schiaccio l'altezza: ecco il }", r"\sin\theta")
        tit_c[1].set_color(C_SIN)

        yl_s = MathTex(r"\sin\theta", font_size=28, color=C_SIN).move_to([x0 + 0.1, y0 + H + 0.68, 0])
        VAL_S = [r"0", r"\tfrac12", r"\tfrac{\sqrt2}{2}", r"\tfrac{\sqrt3}{2}", r"1"]
        lab_s = [MathTex(v, font_size=24, color=C_SIN).move_to([x_, hs(sin_v[k]), 0])
                 for k, (v, x_) in enumerate(zip(VAL_S, [x0 - 0.45] * 5))]

        f_c = MathTex(r"\sin\theta", r"=", r"\dfrac{\sqrt{", r"n", r"}}{2}", font_size=40, color=FG)
        f_c[0].set_color(C_SIN)
        f_c[2].set_color(C_SIN)
        f_c[3].set_color(C_N)
        f_c[4].set_color(C_SIN)
        pannello(f_c, 2.55)
        box_c = SurroundingRectangle(f_c, color=C_N, buff=0.16, stroke_width=2.5)

        p_c = MathTex(r"\dfrac{n}{4}", r"\ \longrightarrow\ ", r"\dfrac{\sqrt n}{2}", font_size=34, color=FG)
        p_c[0].set_color(C_N)
        p_c[2].set_color(C_SIN)
        pannello(p_c, 1.2)

        self.play(
            FadeOut(VGroup(f_b1, f_b2, box_b2, p_b1, p_b2)),
            FadeTransform(tit_b, tit_c),
            run_time=0.7,
        )

        u = ValueTracker(0.0)
        live_curva = always_redraw(lambda: curva(u.get_value()))
        live_pts = [always_redraw(lambda k=k: punto(k, u.get_value())) for k in range(5)]
        live_lvl = [always_redraw(lambda k=k: livello(k, u.get_value())) for k in range(1, 5)]
        live_gd = [always_redraw(lambda k=k: guida(k, u.get_value())) for k in range(1, 5)]
        self.remove(curva_n, *pts, *lvl_s.values(), *gd_s.values())
        self.add(live_curva, *live_lvl, *live_gd, *live_pts)

        self.play(Write(p_c), run_time=0.8)
        self.wait(0.3)
        DUR = 2.4
        self.play(
            u.animate(rate_func=EASE, run_time=DUR).set_value(1.0),
            *[ReplacementTransform(lab_c2[k], lab_s[k], rate_func=EASE, run_time=DUR) for k in range(5)],
            ReplacementTransform(yl_c2, yl_s, rate_func=EASE, run_time=DUR),
        )
        for m in [live_curva, *live_lvl, *live_gd, *live_pts]:
            m.clear_updaters()
        self.play(Write(f_c), run_time=1.0)
        self.play(Create(box_c), run_time=0.6)
        self.wait(1.2)

        # Atto D: lo specchio a 45 gradi da' il coseno
        tit_d = titolo_tex(r"\text{Specchio in }45^\circ\text{: ecco il }", r"\cos\theta")
        tit_d[1].set_color(C_COS)

        x45 = gx(45)
        specchio = DashedLine([x45, y0, 0], [x45, y0 + H + 0.35, 0], color=MUT, stroke_width=2,
                              stroke_opacity=0.8, dash_length=0.1)
        lab_45 = MathTex(r"45^\circ", font_size=26, color=MUT).move_to([x45 + 0.5, y0 + H + 0.35, 0])

        self.play(
            FadeOut(p_c),
            FadeTransform(tit_c, tit_d),
            Create(specchio), Write(lab_45),
            VGroup(*lab_s).animate.set_color(FG),
            FadeOut(yl_s),
            run_time=0.9, rate_func=SMOOTH,
        )

        curva_cos = live_curva.copy()
        self.add(curva_cos)
        self.play(
            Rotate(curva_cos, angle=PI, axis=UP, about_point=np.array([x45, y0, 0])),
            run_time=1.5, rate_func=EASE,
        )
        self.play(curva_cos.animate.set_color(C_COS), run_time=0.6)

        lab_cs = MathTex(r"\sin\theta", font_size=30, color=C_SIN).move_to([gx(76), hs(np.sin(76 * DEGREES)) + 0.42, 0])
        lab_cc = MathTex(r"\cos\theta", font_size=30, color=C_COS).move_to([gx(14), hs(np.cos(14 * DEGREES)) + 0.42, 0])
        self.play(Write(lab_cs), Write(lab_cc), run_time=0.8)
        self.wait(0.3)

        pc = [Dot([gx(a), hs(v), 0], radius=0.08, color=C_COS).set_z_index(10) for a, v in zip(angoli, cos_v)]
        ext_h = DashedLine([gx(30), hs(0.5), 0], [gx(60), hs(0.5), 0], color=C_SIN,
                           stroke_width=2, stroke_opacity=0.6, dash_length=0.08)
        ext_v = DashedLine([gx(30), hs(0.5), 0], [gx(30), hs(sin_v[3]), 0], color=C_ANG,
                           stroke_width=2, stroke_opacity=0.6, dash_length=0.08)

        f_d1 = MathTex(r"\cos\theta", r"=", r"\sin(90^\circ-\theta)", font_size=34, color=FG)
        f_d1[0].set_color(C_COS)
        f_d1[2].set_color(C_SIN)
        pannello(f_d1, 1.45)
        f_d2 = MathTex(r"\cos\theta", r"=", r"\dfrac{\sqrt{", r"4-n", r"}}{2}", font_size=40, color=FG)
        f_d2[0].set_color(C_COS)
        f_d2[2].set_color(C_COS)
        f_d2[3].set_color(C_N)
        f_d2[4].set_color(C_COS)
        pannello(f_d2, 0.4)
        box_d2 = SurroundingRectangle(f_d2, color=C_N, buff=0.16, stroke_width=2.5)
        p_d = MathTex(r"\text{stessi livelli, angoli al contrario}", font_size=28, color=MUT)
        pannello(p_d, -0.75)

        self.play(
            LaggedStart(
                AnimationGroup(Create(ext_h), Create(ext_v), run_time=0.8),
                LaggedStart(*[GrowFromCenter(d, rate_func=POP) for d in pc], lag_ratio=0.2, run_time=1.2),
                lag_ratio=0.5,
            ),
            Write(f_d1),
        )
        self.play(Write(f_d2), run_time=1.1)
        self.play(Create(box_d2), Write(p_d), run_time=0.8)
        self.wait(1.4)

        # Atto E: seno e coseno insieme
        tit_e = titolo_tex(r"\text{Tutto insieme}")

        self.play(
            FadeOut(VGroup(f_d1, p_d, ext_h, ext_v)),
            FadeTransform(tit_d, tit_e),
            VGroup(f_d2, box_d2).animate.shift(UP * 0.6),
            run_time=0.9, rate_func=SMOOTH,
        )

        th = ValueTracker(0.0)

        def s_(): return np.sin(th.get_value() * DEGREES)
        def c_(): return np.cos(th.get_value() * DEGREES)

        tr_s = always_redraw(lambda: Dot([gx(th.get_value()), hs(s_()), 0], radius=0.1, color=C_SIN).set_z_index(12))
        tr_c = always_redraw(lambda: Dot([gx(th.get_value()), hs(c_()), 0], radius=0.1, color=C_COS).set_z_index(12))
        tr_v = always_redraw(lambda: DashedLine(
            [gx(th.get_value()), y0, 0], [gx(th.get_value()), hs(max(s_(), c_())), 0],
            color=FG, stroke_width=2, stroke_opacity=0.5, dash_length=0.08))

        r_t = MathTex(r"\theta=", font_size=34, color=C_ANG)
        r_s = MathTex(r"\sin\theta=", font_size=34, color=C_SIN)
        r_c = MathTex(r"\cos\theta=", font_size=34, color=C_COS)
        for m, y in ((r_t, -0.15), (r_s, -0.85), (r_c, -1.55)):
            m.move_to([0, y, 0]).align_to([X_R, 0, 0], LEFT)
        d_t = DecimalNumber(0, num_decimal_places=0, unit=r"^\circ", font_size=34, color=C_ANG)
        d_s = DecimalNumber(0, num_decimal_places=3, font_size=34, color=C_SIN)
        d_c = DecimalNumber(1, num_decimal_places=3, font_size=34, color=C_COS)
        d_t.next_to(r_t, RIGHT, buff=0.15)
        d_s.next_to(r_s, RIGHT, buff=0.15)
        d_c.next_to(r_c, RIGHT, buff=0.15)
        d_t.add_updater(lambda d: d.set_value(th.get_value()))
        d_s.add_updater(lambda d: d.set_value(s_()))
        d_c.add_updater(lambda d: d.set_value(c_()))

        self.play(
            Write(r_t), Write(r_s), Write(r_c),
            FadeIn(d_t), FadeIn(d_s), FadeIn(d_c),
            FadeIn(tr_s, scale=0.5), FadeIn(tr_c, scale=0.5), FadeIn(tr_v),
            run_time=0.9,
        )
        self.play(th.animate(rate_func=SMOOTH, run_time=3.2).set_value(45.0))

        cx, cy = x45, hs(sin_v[2])
        lab_x = MathTex(r"\tfrac{\sqrt2}{2}", font_size=30, color=FG).move_to([cx - 0.95, cy, 0])
        self.play(
            Flash(np.array([cx, cy, 0.0]), color=FG, line_length=0.25, flash_radius=0.35, run_time=0.9),
            Write(lab_x),
        )
        self.wait(1.0)

        self.play(th.animate(rate_func=SMOOTH, run_time=3.2).set_value(90.0))
        self.wait(2.5)

        self.play(FadeOut(*self.mobjects), run_time=1.2)
        self.wait(1.0)