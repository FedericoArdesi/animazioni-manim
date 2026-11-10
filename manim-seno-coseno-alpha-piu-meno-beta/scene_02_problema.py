from manim import *
from palette import *

ALPHA = 25 * DEGREES
BETA = 40 * DEGREES
R = 1.75  # raggio delle tre circonferenze


def pt(center, ang, r=R):
    """Punto sulla circonferenza di centro `center` all'angolo `ang`."""
    return center + r * np.array([np.cos(ang), np.sin(ang), 0])


def build_panel(center, theta, cos_parts, arcs, faded_alpha=False):
    """Costruisce i pezzi di una circonferenza unitaria (senza mostrarli).

    center      : centro della circonferenza
    theta       : angolo totale del raggio giallo
    cos_parts   : parti di fm(...) per l'etichetta del coseno
    arcs        : lista di (start, end, colore, tex) per gli archi degli angoli
    faded_alpha : se True, lascia la retta di alpha sfumata
    """
    center = np.array(center, dtype=float)
    over = 0.25  # quanto gli assi sporgono dalla circonferenza

    axis_x = Line(center + LEFT * (R + over), center + RIGHT * (R + over))
    axis_y = Line(center + DOWN * (R + over), center + UP * (R + over))
    for ax in (axis_x, axis_y):
        ax.set_stroke(MUTED, 1.5)
    circ = Circle(radius=R, color=MUTED, stroke_width=2).move_to(center)

    # raggio e punto partono sull'asse x (angolo 0) e poi vengono ruotati
    radius = Line(center, pt(center, 0), color=UNIT_COLOR, stroke_width=5)
    dot = Dot(pt(center, 0), radius=0.08, color=UNIT_COLOR)
    rot = VGroup(radius, dot)

    segs = []
    for start, end, color, tex in arcs:
        arc = Arc(
            radius=0.9, start_angle=start, angle=end - start,
            arc_center=center, color=color, stroke_width=5,
        )
        mid = (start + end) / 2
        lab = MathTex(tex, color=color, font_size=40)
        # l'etichetta sta dentro lo spicchio, oltre l'arco, lontana dalle linee
        lab.move_to(center + 1.3 * np.array([np.cos(mid), np.sin(mid), 0]))
        segs.append({"arc": arc, "lab": lab, "start": start, "end": end})

    P = pt(center, theta)
    foot = np.array([P[0], center[1], 0.0])
    proj = DashedLine(P, foot, color=SIN_COLOR, stroke_width=3.5)
    cos_seg = Line(center, foot, color=COS_COLOR, stroke_width=7)
    cos_lab = fm(*cos_parts, font_size=42)
    cos_lab.move_to((center + foot) / 2 + DOWN * 0.6)
    # sfondo nero: l'etichetta resta leggibile anche se tocca l'asse verticale
    cos_lab.add_background_rectangle(color=BG, opacity=1, buff=0.1)

    faded = None
    if faded_alpha:
        faded = Line(
            center, pt(center, ALPHA),
            color=ALPHA_COLOR, stroke_width=4, stroke_opacity=0.4,
        )

    return {
        "center": center, "axis_x": axis_x, "axis_y": axis_y, "circ": circ,
        "rot": rot, "segs": segs, "proj": proj, "cos_seg": cos_seg,
        "cos_lab": cos_lab, "faded": faded,
    }


class Scene02Problema(Scene):
    def animate_panel(self, p):
        """Il raggio ruota fino all'angolo, l'arco si disegna insieme a lui,
        poi cade la proiezione e cresce il segmento del coseno."""
        center = p["center"]
        radius, dot = p["rot"][0], p["rot"][1]

        # il raggio giallo si genera dal centro lungo l'asse x
        self.play(
            LaggedStart(
                Create(radius, rate_func=smooth),
                GrowFromCenter(dot),
                lag_ratio=0.8,
            ),
            run_time=1.0,
        )
        self.add(p["rot"])

        for i, s in enumerate(p["segs"]):
            self.play(
                Rotate(
                    p["rot"], angle=s["end"] - s["start"],
                    about_point=center, rate_func=smooth,
                ),
                Create(s["arc"], rate_func=smooth),
                run_time=1.4,
            )
            extra = [FadeIn(s["lab"], shift=UP * 0.1)]
            if i == 0 and p["faded"] is not None and len(p["segs"]) > 1:
                # la retta di alpha resta sfumata mentre il raggio va avanti
                extra.append(FadeIn(p["faded"]))
            self.play(*extra, run_time=0.5)
            if p["faded"] is not None:
                self.bring_to_front(p["rot"])

        self.play(Create(p["proj"]), run_time=0.8)
        self.play(
            Create(p["cos_seg"]),
            FadeIn(p["cos_lab"], shift=UP * 0.15),
            run_time=1.0,
        )
        self.wait(0.4)

    def construct(self):
        self.camera.background_color = BG

        # =====================================================
        # PARTE 1 - La domanda
        # =====================================================
        q1 = Tex("Possiamo esprimere", font_size=48, color=NEUTRAL)
        g1 = VGroup(
            fm(r"\cos", r"(", r"\alpha", r"+", r"\beta", r")", font_size=48),
            fm(r"\sin", r"(", r"\alpha", r"+", r"\beta", r")", font_size=48),
        ).arrange(RIGHT, buff=0.8)
        q2 = Tex("in funzione di", font_size=48, color=NEUTRAL)
        g2 = VGroup(
            fm(r"\cos", r"\alpha", font_size=48),
            fm(r"\cos", r"\beta", font_size=48),
            fm(r"\sin", r"\alpha", font_size=48),
            fm(r"\sin", r"\beta", font_size=48),
        ).arrange(RIGHT, buff=0.7)

        VGroup(q1, g1, q2, g2).arrange(DOWN, buff=0.7).move_to(ORIGIN)

        # riquadri squadrati, giallo della palette
        box1 = SurroundingRectangle(g1, color=UNIT_COLOR, buff=0.25, stroke_width=3)
        box2 = SurroundingRectangle(g2, color=UNIT_COLOR, buff=0.25, stroke_width=3)
        qmark = Tex("?", font_size=60, color=NEUTRAL).next_to(box2, RIGHT, buff=0.3)

        self.play(Write(q1), run_time=1.2)
        # riquadro e testo partono insieme; il riquadro finisce un attimo prima
        self.play(Write(g1, run_time=1.8), Create(box1, run_time=1.5))
        self.play(Write(q2), run_time=1.0)
        self.play(Write(g2, run_time=2.2), Create(box2, run_time=1.8))
        self.play(Write(qmark), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(VGroup(q1, g1, q2, g2, box1, box2, qmark)))

        # =====================================================
        # PARTE 2 - Tre circonferenze unitarie (in fila, grandi)
        # =====================================================
        y0 = 1.4
        c1 = (-4.6, y0, 0)   # alpha
        c2 = (0.0, y0, 0)    # beta
        c3 = (4.6, y0, 0)    # alpha + beta

        p1 = build_panel(
            c1, ALPHA,
            [r"\cos", r"\alpha"],
            [(0, ALPHA, ALPHA_COLOR, r"\alpha")],
        )
        p2 = build_panel(
            c2, BETA,
            [r"\cos", r"\beta"],
            [(0, BETA, BETA_COLOR, r"\beta")],
        )
        p3 = build_panel(
            c3, ALPHA + BETA,
            [r"\cos", r"(", r"\alpha", r"+", r"\beta", r")"],
            [
                (0, ALPHA, ALPHA_COLOR, r"\alpha"),
                (ALPHA, ALPHA + BETA, BETA_COLOR, r"\beta"),
            ],
            faded_alpha=True,
        )
        panels = (p1, p2, p3)

        # assi e circonferenze: partono uno dopo l'altro, sfasati.
        # Anche dentro lo stesso pannello: asse x, poi asse y, poi cerchio
        base_groups = [
            LaggedStart(
                Create(p["axis_x"], run_time=0.7),
                Create(p["axis_y"], run_time=0.7),
                Create(p["circ"], run_time=1.2),
                lag_ratio=0.3,
            )
            for p in panels
        ]
        self.play(LaggedStart(*base_groups, lag_ratio=0.3))
        self.wait(0.3)

        # poi un angolo alla volta: alpha, beta, alpha + beta
        for p in panels:
            self.animate_panel(p)

        # =====================================================
        # PARTE 3 - Le disuguaglianze
        # =====================================================
        cos_ineq = fm(
            r"\cos", r"(", r"\alpha", r"+", r"\beta", r")",
            r"\neq",
            r"\cos", r"\alpha", r"+", r"\cos", r"\beta",
            font_size=54,
        )
        sin_ineq = fm(
            r"\sin", r"(", r"\alpha", r"+", r"\beta", r")",
            r"\neq",
            r"\sin", r"\alpha", r"+", r"\sin", r"\beta",
            font_size=54,
        )
        ineqs = VGroup(cos_ineq, sin_ineq).arrange(DOWN, buff=0.45)
        if ineqs.width > 12.8:
            ineqs.scale_to_fit_width(12.8)
        ineqs.move_to(DOWN * 2.2)

        self.play(Write(cos_ineq), run_time=2)
        self.wait(0.8)
        self.play(Write(sin_ineq), run_time=2)
        self.wait(2.5)

        self.play(FadeOut(Group(*self.mobjects)))