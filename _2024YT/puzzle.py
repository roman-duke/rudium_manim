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

      self.train.add(self.cars)

    self.add(self.train)

  def _create_tyre(self, tyre_group) -> VMobject:
    tyre = Circle(color=WHITE, radius=0.3, fill_color=WHITE, fill_opacity=1).set_color_by_gradient(self.colors)
    tyre_rim = Circle(color=LOGO_BLACK, radius=0.12, fill_color=BLACK, fill_opacity=.75).move_to(tyre)
    tyre_group.add(tyre, tyre_rim)

    return tyre_group

class Puzzle(MovingCameraScene):
  def construct(self):
    self.camera.frame.save_state()

    #---------- Animate the creation of the required mobjects onto the scene. -----------#
    track = Line(start=LEFT*12, end=RIGHT*12).shift(DOWN*2)

    self.play(Write(track))

    # Create the left train
    left_train = SimpleTrain(2)\
      .scale(0.5)\
      .next_to(track, direction=UP, buff=0.01)\
      .shift(LEFT*5)

    # Create the right train
    right_train = SimpleTrain(2)\
      .scale(0.5)\
      .next_to(track, direction=UP, buff=0.01)\
      .shift(RIGHT * 5)

    self.play(
      AnimationGroup(
        Write(left_train),
        Write(right_train),
        lag_ratio=.5
      )
    )

    # Animate the creation of our fly, Gojo.
    gojo_fly = SVGMobject('./_2024YT/fly_2trains/assets/gojo_fly.svg').set_color(WHITE).rotate(PI, axis=Y_AXIS)
    self.play(
      Write(gojo_fly),
      gojo_fly.animate.scale(0.15).next_to(left_train, direction=RIGHT, buff=0.1),
      run_time=2
    )

    # Make the fly oscillate at the starting position
    self.play(
      gojo_fly.animate.shift(UP * 0.125),
     )

    # TODO: complete this simulation
    # Simulate the movement of the trains and the fly (loop a few times)
    def puzzle_demo():
      self.play(
        AnimationGroup(
          left_train.animate(rate_func=linear).shift(RIGHT * 5 - np.array((left_train.width/2 + .03, 0.0, 0.0))),
          right_train.animate(rate_func=linear).shift(LEFT * 5 + np.array((right_train.width/2 + .03, 0.0, 0.0))),
          run_time=5,
        )
      )

    puzzle_demo()
    self.wait(0.2)

    # Day2: TODO: Work on the Easy solution

    # Day 3: TODO: Work on the Hard Solution

    # Day 4: TODO: Record voiceover and work on half of the more complex solution

    # Day 5: TODO: Work on the other half of the more complex solution

    # Day 6: TODO: Finishihng touches and edit the animations

    # Day 7: TODO: Edit it Adobe After EFfects


    #---------------- EASY SOLUTION ----------------#
    # Save the state of the fly and remove it from the scene
    # gojo_fly.save_state()

    # self.play(Unwrite(gojo_fly))
