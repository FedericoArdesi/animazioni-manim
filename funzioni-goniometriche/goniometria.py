"""
Le sei funzioni goniometriche.
Render:  manim -pqh goniometria.py Goniometria
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from manim import *

# ============================================================
#  LAYOUT
# ============================================================
R = 1.6                                    # raggio della circonferenza (unita' schermo)
O = np.array([-3.6, -0.5, 0.0])            # centro della circonferenza
SEP_X = -0.15                              # separatore tra circonferenza e grafico
BOX = (-12.0, SEP_X, -8.0, 8.0)            # zona di clip: xmin, xmax, ymin, ymax
GRAPH_C = np.array([3.55, -0.5, 0.0])      # centro degli assi cartesiani
YMAX = 2.5                                 # semi-altezza dell'asse y del grafico
BIG = 30.0                                 # "infinito" (in unita' di raggio)
RUN_TIME = 7                               # secondi per un giro completo
RUN_TIME_FINALE = 10                       # secondi per il giro finale

W_THICK, W_THIN = 6, 2
C_THIN = GREY_B


# ============================================================
#  FUNZIONI DI SUPPORTO
# ============================================================
def P(x: float, y: float) -> np.ndarray:
    """Coordinate della circonferenza unitaria -> coordinate schermo."""
    return O + R * np.array([x, y, 0.0])


def num(f: Callable[[float], float], t: float) -> float:
    """Valuta f(t) senza warning; infiniti e NaN diventano numeri enormi."""
    with np.errstate(all="ignore"):
        v = float(f(t))
    if np.isnan(v):
        return 1e9
    return float(np.clip(v, -1e9, 1e9))


def lim(v: float) -> float:
    return float(np.clip(v, -BIG, BIG))


def lim_vec(x: float, y: float) -> tuple[float, float]:
    """Riduce (x, y) a lunghezza massima BIG mantenendo la direzione."""
    m = max(abs(x), abs(y))
    return (x, y) if m <= BIG else (x * BIG / m, y * BIG / m)


def clip_box(a: np.ndarray, b: np.ndarray, box=BOX):
    """Taglia il segmento a-b sul rettangolo box (Liang-Barsky)."""
    xmin, xmax, ymin, ymax = box
    x0, y0 = a[0], a[1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - xmin), (dx, xmax - x0), (-dy, y0 - ymin), (dy, ymax - y0)):
        if abs(p) < 1e-12:
            if q < 0:
                return None
            continue
        r = q / p
        if p < 0:
            if r > t1:
                return None
            t0 = max(t0, r)
        else:
            if r < t0:
                return None
            t1 = min(t1, r)
    return a + (b - a) * t0, a + (b - a) * t1


def segmento(a, b, colore, w=W_THICK):
    """Segmento tra due punti in coordinate unitarie, tagliato sul separatore."""
    c = clip_box(P(*a), P(*b))
    if c is None:
        return None
    return Line(c[0], c[1], color=colore, stroke_width=w)


def sottile(a, b):
    return segmento(a, b, C_THIN, W_THIN)


def crea(*parti) -> VGroup:
    return VGroup(*[p for p in parti if p is not None])


# ============================================================
#  GEOMETRIA: un costruttore per ogni funzione
#  (t = angolo, c = colore)  ->  VGroup di segmenti
# ============================================================
def g_sin(t, c):
    co, si = np.cos(t), np.sin(t)
    return crea(segmento((co, 0), (co, si), c))       # dall'asse x fino a P


def g_cos(t, c):
    co, si = np.cos(t), np.sin(t)
    return crea(segmento((0, si), (co, si), c))       # da P fino all'asse y


def g_tan(t, c):
    v = num(np.tan, t)
    qx, qy = lim_vec(1, v)
    return crea(sottile((0, 0), (qx, qy)),            # raggio prolungato
                segmento((1, 0), (1, lim(v)), c))     # segmento sulla tangente in A


def g_cot(t, c):
    v = num(lambda x: np.cos(x) / np.sin(x), t)
    qx, qy = lim_vec(v, 1)
    return crea(sottile((0, 0), (qx, qy)),
                segmento((0, 1), (lim(v), 1), c))     # segmento sulla tangente in B


def _tangente_in_P(t, s):
    """Punto della tangente in P a distanza s (con segno) da P."""
    co, si = np.cos(t), np.sin(t)
    return co - s * si, si + s * co


def g_sec(t, c):
    v = num(lambda x: 1 / np.cos(x), t)
    s = lim(-num(np.tan, t))                          # arriva sull'asse x
    return crea(sottile((np.cos(t), np.sin(t)), _tangente_in_P(t, s)),
                segmento((0, 0), (lim(v), 0), c))


def g_csc(t, c):
    v = num(lambda x: 1 / np.sin(x), t)
    s = lim(num(lambda x: np.cos(x) / np.sin(x), t))  # arriva sull'asse y
    return crea(sottile((np.cos(t), np.sin(t)), _tangente_in_P(t, s)),
                segmento((0, 0), (0, lim(v)), c))


def retta_x(x):
    """Retta verticale infinita x = costante."""
    return lambda: crea(sottile((x, -BIG), (x, BIG)))


def retta_y(y):
    """Retta orizzontale infinita y = costante."""
    return lambda: crea(sottile((-BIG, y), (BIG, y)))


# ============================================================
#  DATI DELLE SEI FUNZIONI
# ============================================================
@dataclass(frozen=True)
class Funzione:
    nome: str
    tex: str
    f: Callable[[float], float]
    colore: object
    descrizione: str
    geometria: Callable
    statico: Callable | None = None
    asintoti: tuple = ()


FUNZIONI = [
    Funzione("Seno", r"\sin\theta", np.sin, BLUE,
             r"ordinata del punto sulla circonferenza", g_sin),
    Funzione("Coseno", r"\cos\theta", np.cos, GREEN,
             r"ascissa del punto sulla circonferenza", g_cos),
    Funzione("Tangente", r"\tan\theta", np.tan, ORANGE,
             r"segmento sulla tangente verticale in $(1,0)$", g_tan,
             statico=retta_x(1), asintoti=(PI / 2, 3 * PI / 2)),
    Funzione("Cotangente", r"\cot\theta", lambda x: np.cos(x) / np.sin(x), PURPLE,
             r"segmento sulla tangente orizzontale in $(0,1)$", g_cot,
             statico=retta_y(1), asintoti=(PI, TAU)),
    Funzione("Secante", r"\sec\theta", lambda x: 1 / np.cos(x), TEAL,
             r"intercetta sull'asse $x$ della tangente alla circonferenza", g_sec,
             asintoti=(PI / 2, 3 * PI / 2)),
    Funzione("Cosecante", r"\csc\theta", lambda x: 1 / np.sin(x), PINK,
             r"intercetta sull'asse $y$ della tangente alla circonferenza", g_csc,
             asintoti=(PI, TAU)),
]


# ============================================================
#  SCENA
# ============================================================
class Goniometria(Scene):

    def construct(self):
        self.th = ValueTracker(0)          # angolo theta in radianti
        self.da_togliere = []              # curve e asintoti da pulire nel finale
        self.titolo()
        self.costruisci_sfondo()
        self.costruisci_circonferenza()
        self.costruisci_grafico()
        for fn in FUNZIONI:
            self.mostra(fn)
        self.finale()

    # ---------- titolo ----------
    def titolo(self):
        t = Tex(r"\textbf{Le funzioni goniometriche}", color=BLUE, font_size=72)
        lista = MathTex(r"\sin \qquad \cos \qquad \tan \qquad \cot \qquad \sec \qquad \csc",
                      color=BLUE_B, font_size=44)
        lista.next_to(t, DOWN, buff=0.4)
        gruppo = VGroup(t, lista).move_to(ORIGIN)

        self.play(Write(t), run_time=1.6)
        self.play(FadeIn(lista, shift=UP * 0.2))
        self.wait(0.9)
        self.play(FadeOut(gruppo))

    # ---------- separatore ----------
    def costruisci_sfondo(self):
        su = Line([SEP_X, 0, 0], [SEP_X, 4.2, 0], color=GREY_B, stroke_width=1.2)
        giu = Line([SEP_X, 0, 0], [SEP_X, -4.2, 0], color=GREY_B, stroke_width=1.2)
        self.play(Create(su), Create(giu), run_time=1.2, rate_func=smooth)

    # ---------- circonferenza goniometrica ----------
    def costruisci_circonferenza(self):
        th = self.th
        cerchio = Circle(radius=R, color=WHITE, stroke_width=3).move_to(O)

        def pos_P():
            return P(np.cos(th.get_value()), np.sin(th.get_value()))

        raggio = always_redraw(lambda: Line(O, pos_P(), color=YELLOW, stroke_width=4))
        arco = always_redraw(lambda: Arc(
            radius=0.4, start_angle=0, angle=max(th.get_value(), 0.001),
            arc_center=O, color=YELLOW, stroke_width=3))

        lab_theta = MathTex(r"\theta =", font_size=40)
        gradi = DecimalNumber(0, num_decimal_places=0, unit=r"^\circ", font_size=40)
        gruppo = VGroup(lab_theta, gradi).arrange(RIGHT).to_corner(DL, buff=0.5)
        gradi.add_updater(lambda m: m.set_value(th.get_value() * 180 / PI)
                          .next_to(lab_theta, RIGHT))

        asse_x = Line([-7.3, O[1], 0], [SEP_X, O[1], 0], color=GREY_B, stroke_width=2)
        asse_y = Line([O[0], -4.2, 0], [O[0], 4.2, 0], color=GREY_B, stroke_width=2)

        self.play(Create(cerchio), Create(asse_x), Create(asse_y))
        self.play(Create(raggio), Create(arco), FadeIn(gruppo))

    # ---------- assi cartesiani ----------
    def costruisci_grafico(self):
        self.assi = assi = Axes(
            x_range=[0, TAU, PI / 2], y_range=[-YMAX, YMAX, 1],
            x_length=6.4, y_length=4.6, tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2, "include_numbers": False},
        ).move_to(GRAPH_C)

        etichette = VGroup()
        for v, tex in [(PI / 2, r"\frac{\pi}{2}"), (PI, r"\pi"),
                       (3 * PI / 2, r"\frac{3\pi}{2}"), (TAU, r"2\pi")]:
            etichette.add(MathTex(tex, font_size=26).next_to(assi.c2p(v, 0), DOWN, buff=0.15))
            etichette.add(Line(assi.c2p(v, -0.06), assi.c2p(v, 0.06),
                               color=GREY_B, stroke_width=2))
        for v in (1, -1):
            etichette.add(MathTex(str(v), font_size=26).next_to(assi.c2p(0, v), LEFT, buff=0.15))
            etichette.add(Line(assi.c2p(-0.06, v), assi.c2p(0.06, v),
                               color=GREY_B, stroke_width=2))

        self.play(Create(assi), FadeIn(etichette))
        self.wait(0.5)

    # ---------- elementi dinamici del grafico ----------
    def traccia(self, f, colore):
        """Curva di f disegnata da 0 fino a theta, che arriva fino al bordo dell'asse."""
        th, assi = self.th, self.assi

        def build():
            t = th.get_value()
            if t < 0.01:
                return VGroup()
            pezzi, corrente, prev = [], [], None
            for x in np.linspace(0, t, int(t * 120) + 2):
                y = num(f, x)
                dentro = abs(y) <= YMAX
                if prev is not None and dentro != prev[2]:
                    y_fuori = y if not dentro else prev[1]
                    b = YMAX * np.sign(y_fuori)                  # bordo attraversato
                    xc = prev[0] + (x - prev[0]) * (b - prev[1]) / (y - prev[1])
                    corrente.append((xc, b))
                    if not dentro:                               # uscita: chiudi il pezzo
                        if len(corrente) > 1:
                            pezzi.append(corrente)
                        corrente = []
                if dentro:
                    corrente.append((x, y))
                prev = (x, y, dentro)
            if len(corrente) > 1:
                pezzi.append(corrente)

            g = VGroup()
            for p in pezzi:
                m = VMobject(color=colore, stroke_width=4)
                m.set_points_as_corners([assi.c2p(*q) for q in p])
                g.add(m)
            return g

        return always_redraw(build)

    def punto_grafico(self, f, colore, tratteggio: bool = True):
        """Punto sulla curva + verticale tratteggiata (arriva al bordo se f esce)."""
        th, assi = self.th, self.assi

        def build():
            t = th.get_value()
            y = num(f, t)
            yc = float(np.clip(y, -YMAX, YMAX))
            parti = []
            if tratteggio and t > 0.01 and abs(yc) > 0.03:
                parti.append(DashedLine(assi.c2p(t, 0), assi.c2p(t, yc), color=colore,
                                        stroke_width=2, stroke_opacity=0.6,
                                        dash_length=0.08))
            if abs(y) <= YMAX:
                parti.append(Dot(assi.c2p(t, y), color=colore, radius=0.07))
            return VGroup(*parti)

        return always_redraw(build)

    # ---------- una funzione alla volta ----------
    def mostra(self, fn: Funzione):
        th, assi = self.th, self.assi
        asintoti = VGroup(*[
            DashedLine(assi.c2p(x, -YMAX), assi.c2p(x, YMAX),
                       color=GREY, stroke_width=2) for x in fn.asintoti])
        fissi = fn.statico() if fn.statico else None

        entrate = []
        if fissi is not None:
            entrate.append(FadeIn(fissi))
        if len(asintoti) > 0:
            entrate.append(FadeIn(asintoti))
        if entrate:
            self.play(*entrate)

        th.set_value(0)
        geo = always_redraw(lambda: fn.geometria(th.get_value(), fn.colore))
        grafico = self.traccia(fn.f, fn.colore)
        punto = self.punto_grafico(fn.f, fn.colore)
        self.add(geo, grafico, punto)

        self.play(th.animate.set_value(TAU), run_time=RUN_TIME, rate_func=linear)
        self.wait(0.5)

        for m in (geo, grafico, punto):
            m.clear_updaters()
        self.da_togliere.append(grafico)
        if len(asintoti) > 0:
            self.da_togliere.append(asintoti)

        uscite = [FadeOut(geo), FadeOut(punto)]
        if fissi is not None:
            uscite.append(FadeOut(fissi))
        self.play(*uscite)

    # ---------- finale: tutte insieme ----------
    def finale(self):
        th, assi = self.th, self.assi

        # toglie solo curve e asintoti accumulati; cerchio, grafico e separatore restano
        self.play(FadeOut(*self.da_togliere), th.animate.set_value(0), run_time=1.2)
        self.wait(0.3)

        # tangenti in A e B
        fissi = VGroup(retta_x(1)(), retta_y(1)())
        asintoti = VGroup(*[
            DashedLine(assi.c2p(x, -YMAX), assi.c2p(x, YMAX),
                       color=GREY, stroke_width=2)
            for x in (PI / 2, PI, 3 * PI / 2, TAU)])
        self.play(FadeIn(fissi), FadeIn(asintoti))

        geos = [always_redraw(lambda fn=fn: fn.geometria(th.get_value(), fn.colore))
                for fn in FUNZIONI]
        grafici = [self.traccia(fn.f, fn.colore) for fn in FUNZIONI]
        punti = [self.punto_grafico(fn.f, fn.colore, tratteggio=False)
                 for fn in FUNZIONI]
        self.add(*geos, *grafici, *punti)

        self.play(th.animate.set_value(TAU), run_time=RUN_TIME_FINALE, rate_func=linear)
        self.wait(3)