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

class GojoFly(SVGMobject):
  def __init__(self, file_name, obstacle1: VMobject, obstacle2: VMobject, color, **kwargs):
    super().__init__(file_name, **kwargs)
    self.fly = SVGMobject(file_name).set_color(color)
    self.add(self.fly)
    self.obstacle1 = obstacle1
    self.obstacle2 = obstacle2
    self.point_tracker = self.get_point_tracker()
    self.direction = 1

  def get_point_tracker(self):
    """Gets the current points of the obstacles; we actually need only the x coord"""
    p1 = self.obstacle1.get_right()[0]
    p2 = self.obstacle2.get_left()[0]

    return (p1, p2)

  def update_direction(self, dir: int):
    """Updates the direction of the fly"""
    self.direction = dir

  def restore(self):
    return super().restore()

  def roam(self):
    """Allows the fly to roam horizontally, changing direction if a collision is detected"""
    # Add an updater to track the motion of the left and right trains
    def obstacle_updater(mob: VMobject, dt):
      if self.direction == 1:
        if (self.get_point_tracker()[1] - mob.get_right()[0] >= mob.width/2):
          mob.move_to(
            np.array((
              # mob.get_center()[0] + dt * self.get_point_tracker()[1],
              mob.get_center()[0] + .25,
              mob.get_center()[1],
              0
            )),
          )

        else:
          self.fly.flip()
          self.update_direction(-1)

      elif self.direction == -1:
        if (mob.get_left()[0] - self.get_point_tracker()[0] >= mob.width/2):
          mob.move_to(
            np.array((
              # mob.get_center()[0] + dt * self.get_point_tracker()[0],
              mob.get_center()[0] - .25,
              mob.get_center()[1],
              0
            )),
          )

        else:
          self.fly.flip()
          self.update_direction(1)

    self.fly.add_updater(obstacle_updater)

class Puzzle(MovingCameraScene):

  CONFIG = {
    "easy_solution_font": "Times New Roman",
    "hard_solution_font": "Brush Script MT",
  }

  def construct(self):
    # self.camera.frame.save_state()

    #========== ANIMATE THE CREATION OF THE REQUIRED MOBJECTS ONTO THE SCENE. ==========#
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
    gojo_fly = GojoFly('./_2024YT/fly_2trains/assets/gojo_fly.svg', left_train, right_train, WHITE).rotate(PI, axis=Y_AXIS)
    self.play(
      Write(gojo_fly),
      gojo_fly.animate.scale(0.15).next_to(left_train, direction=RIGHT, buff=0.1),
      run_time=2
    )

    # Make the fly oscillate at the starting position
    self.play(
      gojo_fly.animate.shift(UP * 0.125),
     )

    # Save the initial states of the fly and trains
    left_train.save_state()
    right_train.save_state()
    #======================================================================================#


    #========= Simulate the movement of the trains and the fly (loop a few times)  ========#
    def puzzle_demo():
      gojo_fly.roam()
      self.play(
        AnimationGroup(
          left_train.animate(rate_func=linear).shift(RIGHT * 5 - np.array((left_train.width/2 + .03, 0.0, 0.0))),
          right_train.animate(rate_func=linear).shift(LEFT * 5 + np.array((right_train.width/2 + .03, 0.0, 0.0))),
          run_time=10,
        )
      )
      self.wait(0.3)

      # Reset the fly and trains to their initial positions
      self.play(
        Restore(left_train),
        Restore(right_train),
      )

      self.wait(0.3)

    # for _ in range():
    #   puzzle_demo()
    #======================================================================================#

    #================================== INTRO SCENE =======================================#
    # Remove all the mobjects from the current scene
    self.clear()

    # Fade in the "Easy Solution" text
    easy_title = VGroup()
    easy_text = Text("The Easy Solution", font="Times New Roman")
    easy_border = Rectangle(width=easy_text.width * 1.25, height=easy_text.height * 2.5)
    easy_title.add(easy_text, easy_border)

    self.play(
      AnimationGroup(
        Write(easy_title),
        lag_ratio=.75
      )
    )

    self.play(
      FadeOut(easy_title)
    )

    # Add the fly and trains back to the scene
    self.add(gojo_fly, left_train, right_train, track)
    self.wait(0.5)

    # Add a line at the center of the scene (the collision point)
    collision_demarcation = Line(start=UP, end=DOWN * 2)
    point_one = Dot(UP, radius=.075)
    point_two = Dot(DOWN*2, radius=.075)
    points_group = VGroup(point_one, point_two)
    self.play(
      AnimationGroup(
        Write(points_group),
        Write(collision_demarcation),
        lag_ratio=1
      )
    )

    # zoom in on the fly and then fade out, with a flash
    self.camera.frame.save_state()

    self.play(
      AnimationGroup(
        AnimationGroup(
          FocusOn(gojo_fly),
          self.camera.frame.animate.move_to(gojo_fly).set_height(gojo_fly.height * 5),
          lag_ratio=.5
        ),
        AnimationGroup(
          FadeOut(gojo_fly),
          Flash(gojo_fly, num_lines=50, line_length=0.15, line_stroke_wdith=1, color=WHITE),
          lag_ratio=.5
        ),
        lag_ratio=.75
      )
    )

    self.play(self.camera.frame.animate.restore())

    # Day 3: TODO: Work on the Hard Solution

    # Day 4: TODO: Record voiceover and work on half of the more complex solution

    # Day 5: TODO: Work on the other half of the more complex solution

    # Day 6: TODO: Finishihng touches and edit the animations

    # Day 7: TODO: Edit it Adobe After EFfects

    #---------------- EASY SOLUTION ----------------#
    # Save the state of the fly and remove it from the scene
    # gojo_fly.save_state()

    # self.play(Unwrite(gojo_fly))
