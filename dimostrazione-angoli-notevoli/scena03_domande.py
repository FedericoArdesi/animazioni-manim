from common import *


class Scena03Domande(Scene):
    """Le due domande a cui risponde il video."""

    def construct(self):
        titolo = Tex("Due domande", font_size=54, color=FG)
        titolo.to_edge(UP, buff=0.9)

        d1 = domanda_seno()
        d2 = domanda_salti()
        d1.move_to([0, 0.7, 0])
        d2.move_to([0, -0.7, 0])

        self.play(Write(titolo), run_time=0.9)
        self.wait(0.3)
        self.play(Write(d1), run_time=1.6)
        self.wait(1.2)
        self.play(Write(d2), run_time=2.0)
        self.wait(3.0)
        self.play(FadeOut(*self.mobjects), run_time=1.0)
        self.wait(0.5)
