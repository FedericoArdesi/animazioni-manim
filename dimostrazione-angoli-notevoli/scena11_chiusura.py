from common import *


class Scena11Chiusura(Scene):
    """Risposta alle due domande, a specchio con la scena 03, e nota sulla non circolarita'."""

    def construct(self):
        SMOOTH = rate_functions.ease_in_out_sine
        X_L = -6.0

        def a_sinistra(m, y):
            return m.move_to([0, y, 0]).align_to([X_L, 0, 0], LEFT)

        titolo = Tex("Le due risposte", font_size=54, color=FG)
        titolo.to_edge(UP, buff=0.9)
        self.play(Write(titolo), run_time=0.8)
        self.wait(0.3)
        self.play(titolo.animate.scale(0.6).to_edge(UP, buff=0.35), run_time=0.7, rate_func=SMOOTH)

        # ---------- risposta 1 ----------
        d1 = a_sinistra(domanda_seno(), 2.1)

        a1 = MathTex(r"\sin\theta", r"=", r"\dfrac{AB}{2}", r"=", r"\dfrac{\sqrt{n}}{2}",
                     font_size=44, color=FG)
        a1[0].set_color(ARANCIO)
        a1[2].set_color(BLU)
        a1[4].set_color(VERDE)
        a_sinistra(a1, 0.7)
        b1 = SurroundingRectangle(a1, color=VERDE, buff=0.16, stroke_width=2.5)

        spiega1 = Tex(r"$AB$ è la corda sottesa da $2\theta$, e $AB^2=n$", font_size=34, color=MUT)
        a_sinistra(spiega1, -0.4)

        nota = VGroup(
            Tex(r"Le cinque corde usano solo:", font_size=32, color=FG),
            Tex(r"triangolo equilatero, Pitagora, Talete.", font_size=32, color=FG),
            Tex(r"Nessun valore di $\sin$ o $\cos$ in partenza:", font_size=32, color=FG),
            Tex(r"la dimostrazione non è circolare.", font_size=32, color=VERDE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        a_sinistra(nota, -2.1)

        self.play(Write(d1), run_time=1.2)
        self.wait(0.3)
        self.play(Write(a1), run_time=1.3)
        self.play(Create(b1), run_time=0.6)
        self.play(Write(spiega1), run_time=1.0)
        self.wait(0.6)
        self.play(Write(nota[0]), Write(nota[1]), run_time=1.4)
        self.play(Write(nota[2]), run_time=1.1)
        self.play(Write(nota[3]), run_time=0.9)
        self.wait(3.0)
        self.play(FadeOut(d1, a1, b1, spiega1, nota), run_time=0.8)
        self.wait(0.3)

        # ---------- risposta 2 ----------
        d2 = a_sinistra(domanda_salti(), 2.5)

        passo1 = Tex(r"$n$ sale di $1$ a ogni passo", font_size=38, color=FG)
        passo1[0][0].set_color(VERDE)

        passo2 = MathTex(r"\cos2\theta", r"=", r"1-\dfrac{n}{2}", font_size=44, color=FG)
        passo2[0].set_color(BLU)
        passo2[2].set_color(VERDE)

        passo3 = Tex(r"quindi $\cos2\theta$ scende sempre di $\tfrac12$", font_size=38, color=FG)

        passo4a = Tex(r"Ma il coseno non è una retta:", font_size=38, color=FG)
        passo4b = Tex(r"piatto agli estremi, ripido al centro", font_size=38, color=GIALLO)

        passo5a = Tex(r"Per questo $\theta$ non cresce di un passo fisso:", font_size=38, color=FG)
        passo5b = Tex(r"non esiste nessuna formula $\theta=a\,n+b$", font_size=38, color=GIALLO)

        a_sinistra(passo1, 1.35)
        a_sinistra(passo2, 0.6)
        a_sinistra(passo3, -0.15)
        a_sinistra(passo4a, -0.95)
        a_sinistra(passo4b, -1.5)
        a_sinistra(passo5a, -2.4)
        a_sinistra(passo5b, -2.95)

        self.play(Write(d2), run_time=1.6)
        self.wait(0.4)
        self.play(Write(passo1), run_time=1.0)
        self.wait(0.3)
        self.play(Write(passo2), run_time=1.1)
        self.wait(0.3)
        self.play(Write(passo3), run_time=1.2)
        self.wait(0.8)
        self.play(Write(passo4a), run_time=1.1)
        self.play(Write(passo4b), run_time=1.1)
        self.wait(0.8)
        self.play(Write(passo5a), run_time=1.2)
        self.play(Write(passo5b), run_time=1.2)
        self.wait(2.0)

        self.play(FadeOut(passo1, passo2, passo3, passo4a, passo4b, passo5a, passo5b), run_time=0.8)

        legame = Tex(r"Il legame esatto è", font_size=38, color=FG)
        a2 = MathTex(r"\theta_n", r"=", r"\dfrac12\arccos\!\Big(1-\dfrac{n}{2}\Big)",
                     font_size=56, color=FG)
        a2[0].set_color(GIALLO)
        legame.move_to([0, 0.9, 0])
        a2.move_to([0, -0.4, 0])
        b2 = SurroundingRectangle(a2, color=VERDE, buff=0.22, stroke_width=3)

        self.play(Write(legame), run_time=0.9)
        self.play(Write(a2), run_time=1.5)
        self.play(Create(b2), run_time=0.7)
        self.wait(3.5)

        self.play(FadeOut(*self.mobjects), run_time=1.2)
        self.wait(1.0)
