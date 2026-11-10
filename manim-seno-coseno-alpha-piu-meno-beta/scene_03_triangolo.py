from manim import *
from palette import *

BETA = 40 * DEGREES
R = 5.2  # lunghezza dell'ipotenusa (= 1 nel disegno)


class Scene03Triangolo(Scene):
    def construct(self):
        self.camera.background_color = BG

        # --- Geometria: O all'origine del triangolo, ipotenusa a angolo beta ---
        O = np.array([-2.0, -1.7, 0.0])
        H = O + R * np.array([np.cos(BETA), np.sin(BETA), 0])   # vertice in alto
        F = np.array([H[0], O[1], 0.0])                          # piede del cateto

        hyp = Line(O, H, color=UNIT_COLOR, stroke_width=6)
        leg_cos = Line(O, F, color=MUTED, stroke_width=2.5)
        leg_sin = Line(F, H, color=MUTED, stroke_width=2.5)

        # segno di angolo retto, dentro il triangolo
        s = 0.3
        right = VMobject(color=MUTED, stroke_width=2.5)
        right.set_points_as_corners([
            F + LEFT * s,
            F + LEFT * s + UP * s,
            F + UP * s,
        ])

        # angolo beta riempito
        sector = Sector(
            radius=1.1, angle=BETA, start_angle=0, arc_center=O,
            color=BETA_COLOR, fill_opacity=0.5, stroke_width=0,
        )
        beta_lab = fm(r"\beta", font_size=40)
        beta_lab.move_to(O + 1.55 * np.array([np.cos(BETA / 2), np.sin(BETA / 2), 0]))

        # etichette dei lati
        cos_lab = fm(r"\cos", r"\beta", font_size=44)
        cos_lab.next_to(leg_cos, DOWN, buff=0.25)

        sin_lab = fm(r"\sin", r"\beta", font_size=44)
        sin_lab.next_to(leg_sin, RIGHT, buff=0.3)

        one_lab = MathTex("1", color=UNIT_COLOR, font_size=48)
        normal = np.array([-np.sin(BETA), np.cos(BETA), 0])  # verso l'alto-sinistra
        one_lab.move_to((O + H) / 2 + 0.4 * normal)

        # --- Animazione ---
        # ipotenusa e cateto orizzontale partono insieme da O (angolo in basso a sinistra)
        # il cateto verticale continua dal punto dove finisce quello orizzontale,
        # e tutti e tre i lati finiscono nello stesso istante
        self.play(
            Create(hyp, rate_func=linear),
            Succession(
                Create(leg_cos, run_time=1.1, rate_func=linear),
                Create(leg_sin, run_time=0.9, rate_func=linear),
            ),
            run_time=1.3,
        )
        self.play(Create(right), run_time=0.8)
        self.wait(0.3)

        # l'etichetta 1 viene dopo
        self.play(Write(one_lab), run_time=0.6)
        self.wait(0.3)

        self.play(FadeIn(sector), run_time=0.8)
        self.play(Write(beta_lab), run_time=0.5)
        self.wait(0.3)

        self.play(Write(cos_lab), run_time=1.0)
        self.play(Write(sin_lab), run_time=1.0)
        self.wait(2)