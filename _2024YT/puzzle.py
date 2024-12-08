from manim import *

class SimpleTrain(VMobject):
  def __init__(self, no_of_cars=1, no_of_tyre_groups=2, **kwargs):
    super().__init__(**kwargs)

    self.train = VGroup()
    self.cars = VGroup()
    self.colors = ["#6a6a6a", "#f7f7f7"]

    for _ in range(no_of_cars):
      car = VGroup().add(Rectangle(height=1, width=3, fill_color=WHITE, fill_opacity=1)).set_color_by_gradient(self.colors)
      tyres = VGroup()

      for _ in range(no_of_tyre_groups):
        sub_tyres_group = VGroup().add(self._create_tyre(VGroup()), self._create_tyre(VGroup()))

        sub_tyres_group.arrange_in_grid(1, buff=.15)
        tyres.add(sub_tyres_group)

      tyres.arrange_in_grid(1, buff=0.50)\
        .next_to(car, direction=DOWN, buff=0)\
        .shift(UP*0.25)\
        .set_z_index(-1)\
        .scale(car.width/tyres.width * 0.85)

      car.add(tyres)
      self.cars.add(car).arrange_in_grid(1, buff=0.5)

    self.add(self.cars)

  def _create_tyre(self, tyre_group) -> VMobject:
    tyre = Circle(color=WHITE, radius=0.3, fill_color=WHITE, fill_opacity=1).set_color_by_gradient(self.colors)
    tyre_rim = Circle(color=LOGO_BLACK, radius=0.12, fill_color=BLACK, fill_opacity=.75).move_to(tyre)
    tyre_group.add(tyre, tyre_rim)

    return tyre_group

class Puzzle(Scene):
  def construct(self):
    # Animate the creation of a complex train
    # complexTrainSVG = SVGMobject('./_2024YT/fly_2trains/assets/complex_train.svg').set_color(WHITE).rotate(PI, UP)

    # self.play(
    #   Write(complexTrainSVG),
    #   complexTrainSVG.animate.scale(0.25),
    #   run_time=3
    # )

    # TODO: animate the creation of a train track and a background
    # Not sure if this would be good enough in a 3D space or if it should be confined to 2D space.
    train = SimpleTrain()
    self.play(Write(train))
    self.wait()

    # TODO: Make a class that handles the custom mobject creation of a fly.
    # We can use SVGs to handle this. Should we be ambitious and animate the motion of the fly flapping its wings?

    # Undo creation of the complex train and then animate the creation of a simple train.
    # TODO: Make a class that handles the custom mobject creation of a train.
