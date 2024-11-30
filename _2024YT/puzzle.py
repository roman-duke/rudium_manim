from manim import *

class Puzzle(Scene):
  def construct(self):
    # Animate the creation of a complex train
    complexTrainSVG = SVGMobject('./_2024YT/fly_2trains/assets/complex_train.svg').set_color(WHITE).rotate(PI, UP)

    self.play(
      Write(complexTrainSVG),
      complexTrainSVG.animate.scale(0.25),
      run_time=3
    )

    # Undo creation of the complex train and then animate the creation of a simple train.
    # TODO: Make a class that handles the custom mobject creation of a train.
