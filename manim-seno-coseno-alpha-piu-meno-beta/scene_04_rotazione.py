from manim import *
from palette import *

ALPHA = 25 * DEGREES
BETA = 40 * DEGREES
R = 5.2  # raggio della circonferenza = ipotenusa

# colore per cerchiare il punto P (cambialo qui se lo vuoi diverso)
HILITE = UNIT_COLOR


def unit(ang):
    return np.array([np.cos(ang), np.sin(ang), 0.0])


class Scene04Rotazione(Scene):
    def construct(self):
        self.camera.background_color = BG

        # posizione del triangolo a fine scena 3 e posizione finale in questa scena
        O3 = np.array([-2.0, -1.7, 0.0])
        O = np.array([-5.2, -2.5, 0.0])      # origine: disegno piu' al centro
        move = O - O3

        H0 = O + R * unit(BETA)               # vertice in alto, prima della rotazione
        F0 = np.array([H0[0], O[1], 0.0])     # piede del cateto, prima della rotazione

        # --- Triangolo come a fine scena 3 (costruito in O, poi spostato in O3) ---
        hyp = Line(O, H0, color=UNIT_COLOR, stroke_width=6)
        leg_cos = Line(O, F0, color=MUTED, stroke_width=2.5)
        leg_sin = Line(F0, H0, color=MUTED, stroke_width=2.5)

        s = 0.3
        right = VMobject(color=MUTED, stroke_width=2.5)
        right.set_points_as_corners([
            F0 + LEFT * s,
            F0 + LEFT * s + UP * s,
            F0 + UP * s,
        ])

        sector_beta = Sector(
            radius=1.1, angle=BETA, start_angle=0, arc_center=O,
            color=BETA_COLOR, fill_opacity=0.5, stroke_width=0,
        )

        beta_lab = fm(r"\beta", font_size=40)
        beta_lab.move_to(O + 1.55 * unit(BETA / 2))
        cos_lab = fm(r"\cos", r"\beta", font_size=44)
        cos_lab.next_to(leg_cos, DOWN, buff=0.25)
        sin_lab = fm(r"\sin", r"\beta", font_size=44)
        sin_lab.next_to(leg_sin, RIGHT, buff=0.3)
        one_lab = MathTex("1", color=UNIT_COLOR, font_size=48)
        one_lab.move_to((O + H0) / 2 + 0.4 * np.array([-np.sin(BETA), np.cos(BETA), 0]))

        triangle = VGroup(hyp, leg_cos, leg_sin, right, sector_beta)
        side_labels = VGroup(one_lab, cos_lab, sin_lab)
        everything = VGroup(triangle, side_labels, beta_lab)

        everything.shift(-move)   # parte esattamente dove finiva la scena 3
        self.add(everything)
        self.wait(0.8)

        # il disegno scivola verso il centro
        self.play(everything.animate.shift(move), run_time=1.0)
        self.wait(0.3)

        # =====================================================
        # Assi e quarto di circonferenza tratteggiata
        # =====================================================
        axis_x = Line(O + LEFT * 0.3, O + RIGHT * (R + 0.3), color=MUTED, stroke_width=1.5)
        axis_y = Line(O + DOWN * 0.3, O + UP * (R + 0.15), color=MUTED, stroke_width=1.5)
        quarter = DashedVMobject(
            Arc(radius=R, start_angle=0, angle=PI / 2, arc_center=O,
                color=MUTED, stroke_width=2),
            num_dashes=50,
        )

        self.play(
            LaggedStart(
                Create(axis_x, run_time=0.8),
                Create(axis_y, run_time=0.8),
                lag_ratio=0.4,
            )
        )
        self.play(Create(quarter), run_time=1.5)
        self.wait(0.3)

        # =====================================================
        # Il triangolo ruota di alpha attorno all'origine.
        # Le etichette dei lati spariscono, beta segue il suo angolo.
        # =====================================================
        self.play(FadeOut(side_labels), run_time=0.6)

        def move_beta_label(m, a):
            r = 1.55 + 0.15 * a
            m.move_to(O + r * unit(BETA / 2 + a * ALPHA))

        self.play(
            Rotate(triangle, angle=ALPHA, about_point=O, rate_func=smooth),
            UpdateFromAlphaFunc(beta_lab, move_beta_label, rate_func=smooth),
            run_time=1.8,
        )
        self.wait(0.3)

        # punti dopo la rotazione
        F = O + R * np.cos(BETA) * unit(ALPHA)         # piede del cateto cos beta
        P = O + R * unit(ALPHA + BETA)                 # punto sulla circonferenza
        G = np.array([F[0], O[1], 0.0])                # proiezione di F sull'asse x

        # =====================================================
        # Angolo alpha
        # =====================================================
        sector_alpha = Sector(
            radius=1.1, angle=ALPHA, start_angle=0, arc_center=O,
            color=ALPHA_COLOR, fill_opacity=0.5, stroke_width=0,
        )
        alpha_lab = fm(r"\alpha", font_size=40)
        alpha_lab.move_to(O + 1.7 * unit(ALPHA / 2))

        self.play(FadeIn(sector_alpha), run_time=0.8)
        self.play(Write(alpha_lab), run_time=0.5)
        self.wait(0.3)

        # =====================================================
        # Verticale dal piede all'asse x e punto sulla circonferenza
        # =====================================================
        drop = DashedLine(F, G, color=MUTED, stroke_width=2.5)
        dot = Dot(P, radius=0.1, color=UNIT_COLOR)

        self.play(Create(drop), run_time=0.8)
        self.play(GrowFromCenter(dot), run_time=0.5)
        self.wait(0.4)

        # =====================================================
        # Il punto P e le sue coordinate
        # =====================================================
        ring = Circle(radius=0.25, color=HILITE, stroke_width=3).move_to(P)
        coords = fm(
            r"(", r"\cos", r"(", r"\alpha", r"+", r"\beta", r")",
            r",",
            r"\sin", r"(", r"\alpha", r"+", r"\beta", r")", r")",
            font_size=40,
        )
        coords.next_to(P, UP + RIGHT, buff=0.15)

        self.play(Create(ring), run_time=0.8)
        self.play(Write(coords), run_time=1.8)
        self.wait(2)