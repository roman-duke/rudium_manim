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
  def __init__(self, file_name, color, **kwargs):
    super().__init__(file_name, **kwargs)
    self.fly = SVGMobject(file_name).set_color(color)
    self.add(self.fly)
    self.direction = 1

  def get_point_tracker(self, obstacle1: VMobject, obstacle2: VMobject):
    """Gets the current points of the obstacles; we actually need only the x coord"""
    p1 = obstacle1.get_right()[0]
    p2 = obstacle2.get_left()[0]

    return (p1, p2)

  def update_direction(self, dir: int):
    """Updates the direction of the fly"""
    self.direction = dir

  def restore(self):
    return super().restore()

  def roam(self, ob1: VMobject, ob2: VMobject, infiniteRoam=True):
    """Allows the fly to roam horizontally, changing direction if a collision is detected"""
    # Add an updater to track the motion of the left and right trains
    def obstacle_updater(mob: VMobject, dt):
      if self.direction == 1:
        if (self.get_point_tracker(ob1, ob2)[1] - mob.get_right()[0] >= mob.width/2):
          mob.move_to(
            np.array((
              # mob.get_center()[0] + dt * self.get_point_tracker()[1],
              mob.get_center()[0] + .25,
              mob.get_center()[1],
              0
            )),
          )

        else:
          if infiniteRoam:
            self.fly.flip()
            self.update_direction(-1)


      elif self.direction == -1:
        if (mob.get_left()[0] - self.get_point_tracker(ob1, ob2)[0] >= mob.width/2):
          mob.move_to(
            np.array((
              # mob.get_center()[0] + dt * self.get_point_tracker()[0],
              mob.get_center()[0] - .25,
              mob.get_center()[1],
              0
            )),
          )

        else:
          if infiniteRoam:
            self.fly.flip()
            self.update_direction(1)

    self.fly.add_updater(obstacle_updater)

  def clear_all_updaters(self):
    self.fly.clear_updaters()

# Custom Count Animation
class Count(Animation):
  def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
    # Pass number as the mobject of the animation
    super().__init__(number,  **kwargs)
    # Set start and end
    self.start = start
    self.end = end

  def interpolate_mobject(self, alpha: float) -> None:
    # Set value of DecimalNumber according to alpha
    value = self.start + (alpha * (self.end - self.start))
    self.mobject.set_value(value)

class Puzzle(MovingCameraScene):

  CONFIG = {
    "easy_solution_font": "Times New Roman",
    "hard_solution_font": "Brush Script MT",
  }

  def construct(self):
    self.camera.frame.save_state()

    # #========== ANIMATE THE CREATION OF THE REQUIRED MOBJECTS ONTO THE SCENE. ==========#
    track = Line(start=LEFT*12, end=RIGHT*12).shift(DOWN*2)

    # self.play(Write(track))

    # # Create the left train
    left_train = SimpleTrain(2)\
      .scale(0.5)\
      .next_to(track, direction=UP, buff=0.01)\
      .shift(LEFT * 5)

    # Create the right train
    right_train = SimpleTrain(2)\
      .scale(0.5)\
      .next_to(track, direction=UP, buff=0.01)\
      .shift(RIGHT * 5)

    # self.play(
    #   AnimationGroup(
    #     Write(left_train),
    #     Write(right_train),
    #     lag_ratio=.5
    #   )
    # )

    # # Animate the creation of our fly, Gojo.
    # gojo_fly = GojoFly('./_2024YT/fly_2trains/assets/gojo_fly.svg', WHITE).rotate(PI, axis=Y_AXIS)
    # self.play(
    #   Write(gojo_fly),
    #   gojo_fly.animate.scale(0.15).next_to(left_train, direction=RIGHT, buff=0.1),
    #   run_time=2
    # )

    # # Make the fly oscillate at the starting position
    # self.play(
    #   gojo_fly.animate.shift(UP * 0.125),
    #  )

    # # Save the initial states of the fly and trains
    # left_train.save_state()
    # right_train.save_state()
    # #======================================================================================#


    # #========= Simulate the movement of the trains and the fly (loop a few times)  ========#
    # def puzzle_demo():
    #   self.play(
    #     AnimationGroup(
    #       left_train.animate(rate_func=linear).shift(RIGHT * 5 - np.array((left_train.width/2 + .03, 0.0, 0.0))),
    #       right_train.animate(rate_func=linear).shift(LEFT * 5 + np.array((right_train.width/2 + .03, 0.0, 0.0))),
    #       run_time=10,
    #     )
    #   )
    #   self.wait(0.3)

    #   # Reset the fly and trains to their initial positions
    #   self.play(
    #     Restore(left_train),
    #     Restore(right_train),
    #   )

    #   self.wait(0.3)

    # gojo_fly.roam(left_train, right_train)

    # for _ in range(2):
    #   puzzle_demo()
    # #======================================================================================#

    # #============================== EASY SOLUTION SCENE ===================================#
    # # Remove all the mobjects from the current scene
    # self.clear()

    # HACK: we have to create a new gojo_fly object as animation with this current one seems to be buggy
    gojo_fly = GojoFly('./_2024YT/fly_2trains/assets/gojo_fly.svg', WHITE)\
      .scale(0.15)\
      .rotate(PI, axis=Y_AXIS)\
      .next_to(left_train, direction=RIGHT, buff=0.1)\
      .shift(UP * 0.125)
    # #----------------------------------------------------------------------------------------#

    # # Fade in the "Easy Solution" text
    # easy_title = VGroup()
    # easy_text = Text("The Easy Solution", font="Times New Roman")
    # easy_border = Rectangle(width=easy_text.width * 1.25, height=easy_text.height * 2.5)
    # easy_title.add(easy_text, easy_border)

    # self.play(
    #   AnimationGroup(
    #     Write(easy_title),
    #     lag_ratio=.75
    #   )
    # )

    # self.play(
    #   FadeOut(easy_title)
    # )

    # # Add the fly and trains back to the scene
    # self.add(gojo_fly, left_train, right_train, track)
    # self.wait(0.5)

    # # zoom in on the fly and then fade out, with a flash
    # self.camera.frame.save_state()

    # self.play(
    #   AnimationGroup(
    #     AnimationGroup(
    #       FocusOn(gojo_fly),
    #       self.camera.frame.animate.move_to(gojo_fly).set_height(gojo_fly.height * 5),
    #       lag_ratio=.5
    #     ),
    #     AnimationGroup(
    #       FadeOut(gojo_fly),
    #       Flash(gojo_fly, num_lines=50, line_length=0.15, line_stroke_wdith=1, color=WHITE),
    #       lag_ratio=.5
    #     ),
    #     lag_ratio=.75
    #   )
    # )

    # self.play(self.camera.frame.animate.restore())

    # # Using a brace, show the initial distance between the two trains, then add an updater to track the changes
    # distance_brace = BraceBetweenPoints(left_train.get_right(), right_train.get_left()).next_to(track, direction=DOWN, buff=.2)
    # distance_between_trains = DecimalNumber(number=100, num_decimal_places=0, font_size=30).next_to(distance_brace, direction=DOWN, buff=.2)

    # Add a vector to indicate the speed of each of the trains
    left_train_velocity_vector = Arrow(start=LEFT, end=RIGHT).next_to(left_train, direction=UP, buff=.2).scale(.75, True)
    right_train_velocity_vector = Arrow(start=RIGHT, end=LEFT).next_to(right_train, direction=UP, buff=.2).scale(.75, True)

    left_train_velocity_label = MathTex("v_1 = 50 \, \mathrm{km/hr}").next_to(left_train_velocity_vector, direction=UP, buff=.1).scale(.5)
    right_train_velocity_label = MathTex("v_2 = 50 \, \mathrm{km/hr}").next_to(right_train_velocity_vector, direction=UP, buff=.1).scale(.5)

    left_train_velocity_annot = VGroup(left_train_velocity_vector, left_train_velocity_label)
    right_train_velocity_annot = VGroup(right_train_velocity_vector, right_train_velocity_label)

    # # # TODO: Use this at the end of the Easy Solution Scene
    # # # =======================================================================================================================================#
    # # # Show the time elapsed
    # # # time_elapsed_text = Tex('t = ').move_to(UP * 2)
    # # # elapsed_time = DecimalNumber(number=0, num_decimal_places=2, unit="hr").next_to(time_elapsed_text, RIGHT)
    # # # elapsed_time.add_updater(lambda m, dt: m.set_value(m.get_value() + 0.2))
    # # # =======================================================================================================================================#

    # self.play(
    #   Create(distance_brace),
    #   Write(distance_between_trains),
    #   Write(left_train_velocity_annot),
    #   Write(right_train_velocity_annot)
    # )

    # self.play(
    #   Uncreate(distance_brace),
    #   Unwrite(distance_between_trains),
    #   run_time=.75
    # )

    # # Display two braces that track the distance covered of the left and right trains
    # initial_left_train_pos = left_train.saved_state.get_right()
    # initial_right_train_pos = right_train.saved_state.get_left()

    # left_train_brace = BraceBetweenPoints(initial_left_train_pos, (initial_left_train_pos[0] + .15, initial_left_train_pos[1], initial_left_train_pos[2])).shift(DOWN*.25).scale(.85)
    # right_train_brace = BraceBetweenPoints((initial_right_train_pos[0] - .15, initial_right_train_pos[1], initial_right_train_pos[2]), initial_right_train_pos).shift(DOWN*.25).scale(.85)
    # left_train_distance_covered = DecimalNumber(number=0, num_decimal_places=0, unit="km", font_size=24).next_to(left_train_brace, direction=DOWN, buff=.1)
    # right_train_distance_covered = DecimalNumber(number=0, num_decimal_places=0, unit="km", font_size=24).next_to(right_train_brace, direction=DOWN, buff=.1)

    # def left_train_distance_updater(mob: DecimalNumber):
    #   # Get the distance between the starting pos. and the current pos. of the left train
    #   scaled_left_distance = abs((left_train.get_right()[0] - initial_left_train_pos[0]) / (initial_left_train_pos[0]) * 50)
    #   mob.set_value(scaled_left_distance)
    #   mob.next_to(left_train_brace, direction=DOWN)

    #   # # Update the brace in the process too
    #   # left_train_brace.become(BraceBetweenPoints(initial_left_train_pos, left_train.get_right())).next_to(track, direction=DOWN, buff=.2)

    # def right_train_distance_updater(mob: DecimalNumber):
    #   # Get the distance between the starting pos. and the current pos. of the right train
    #   scaled_right_distance = abs((right_train.get_left()[0] - initial_right_train_pos[0]) / (initial_right_train_pos[0]) * 50)
    #   mob.set_value(scaled_right_distance)
    #   mob.next_to(right_train_brace, direction=DOWN)

    #   # # Update the brace in the process too
    #   # right_train_brace.become(BraceBetweenPoints(initial_right_train_pos, right_train.get_left())).next_to(track, direction=DOWN, buff=.2)

    # def left_train_brace_updater(mob: BraceBetweenPoints):
    #   # Update the brace in the process too
    #   mob.become(BraceBetweenPoints(initial_left_train_pos, left_train.get_right())).shift(DOWN*.25).scale(.85)

    # def right_train_brace_updater(mob: BraceBetweenPoints):
    #   # Update the brace in the process too
    #   mob.become(BraceBetweenPoints(right_train.get_left(), initial_right_train_pos)).shift(DOWN*.25).scale(.85)

    # self.play(
    #   Create(left_train_brace),
    #   Create(right_train_brace),
    #   Write(left_train_distance_covered),
    #   Write(right_train_distance_covered),
    # )

    # left_train_brace.add_updater(left_train_brace_updater)
    # right_train_brace.add_updater(right_train_brace_updater)
    # left_train_distance_covered.add_updater(left_train_distance_updater)
    # right_train_distance_covered.add_updater(right_train_distance_updater)

    # # Add a line at the center of the scene (the collision point)
    # collision_demarcation = Line(start=ORIGIN, end=DOWN * 2)
    # point_one = Dot(ORIGIN, radius=.075)
    # point_two = Dot(DOWN*2, radius=.075)
    # points_group = VGroup(point_one, point_two)

    # self.play(
    #   AnimationGroup(
    #     AnimationGroup(
    #       left_train.animate(rate_func=linear).shift(RIGHT * 5 - np.array((left_train.width/2 + .03, 0.0, 0.0))),
    #       right_train.animate(rate_func=linear).shift(LEFT * 5 + np.array((right_train.width/2 + .03, 0.0, 0.0))),
    #       # Count(elapsed_time, 0, 2, rate_functions=linear),
    #       run_time=10,
    #     ),
    #     AnimationGroup(
    #       Write(points_group),
    #       Write(collision_demarcation),
    #       lag_ratio=1
    #     ),
    #     lag_ratio=.75
    #   )
    # )
    # self.wait(0.3)

    # #===================== Animation of the Easy Solution at the top right of the screen ========================#
    # self.camera.frame.save_state()
    # # Create the bounding box for the calculation at the right hand of the screen
    # easy_calculation_bounding_box = Square(side_length=5).move_to(UR * 4)

    # easy_method_title = Title("Distance-Speed-Time Relationship")\
    #   .scale_to_fit_width(easy_calculation_bounding_box.width * 0.85)\
    #   .move_to(easy_calculation_bounding_box)\
    #   .align_to(easy_calculation_bounding_box, direction=UP)\
    #   .shift(DOWN*.15)

    # train_distance_formula_text = MathTex(r"distance = speed \times time").move_to(easy_calculation_bounding_box).scale(.75)
    # train_distance_formula_symbol = MathTex(r"d_{\text{train}} = v_{\text{train}} \times t").move_to(easy_calculation_bounding_box).scale(.75)

    # self.play(
    #   self.camera.frame.animate.set_height(
    #     easy_calculation_bounding_box.height * 1.2
    #   )
    # )

    # self.play(
    #   Write(easy_calculation_bounding_box),
    #   Write(easy_method_title),
    #   self.camera.frame.animate.move_to(easy_calculation_bounding_box)
    # )

    # # Write the distance formula
    # self.play(
    #   Write(train_distance_formula_text)
    # )

    # self.play(
    #   Transform(train_distance_formula_text, train_distance_formula_symbol)
    # )

    # self.play(
    #   train_distance_formula_text.animate.shift(UP * 1.5),
    # )

    # time_formula_symbol = MathTex(r"t = \frac{d_{\text{train}}}{v_{\text{train}}}").move_to(train_distance_formula_text.get_center()).scale(.75)

    # time_taken_substituted = MathTex(r"\Rightarrow t = \frac{50 km}{50 km/hr}").move_to(easy_calculation_bounding_box).scale(.75)

    # time_taken = MathTex(r"t = 1 hr").next_to(time_taken_substituted, direction=DOWN).shift(DOWN * .5).scale(.75)

    # fly_distance_formula_symbol = MathTex(r"d_{\text{fly}} = v_{\text{fly}} \times time")\
    #     .move_to(train_distance_formula_text.get_center())\
    #     .scale(.75)

    # fly_distance_covered_substituted = MathTex(r"\Rightarrow d_{\text{fly}} = 100km/hr \times 1hr")\
    #   .move_to(easy_calculation_bounding_box)\
    #   .scale(.75)

    # fly_distance_covered = MathTex(r"d_{\text{fly}} = 100km")\
    #   .next_to(fly_distance_covered_substituted, direction=DOWN)\
    #   .shift(DOWN * .5)\
    #   .scale(.75)

    # self.play(Transform(train_distance_formula_text, time_formula_symbol))
    # self.wait(0.5)

    # self.play(
    #   Write(time_taken_substituted)
    # )

    # self.play(
    #   AnimationGroup(
    #     Write(time_taken),
    #     Circumscribe(time_taken),
    #     lag_ratio=1
    #   )
    # )

    # self.play(
    #   FadeOut(time_taken_substituted, time_taken)
    # )

    # self.remove(time_taken_substituted, time_taken)

    # # Calculation for the actual distance covered by the fly
    # self.play(
    #   AnimationGroup(
    #     Transform(train_distance_formula_text, fly_distance_formula_symbol),
    #     Write(fly_distance_covered_substituted),
    #     Write(fly_distance_covered),
    #     lag_ratio=1
    #   )
    # )

    # self.play(
    #   self.camera.frame.animate.restore()
    # )

    # self.play(
    #   FadeOut(
    #     track,
    #     left_train,
    #     right_train,
    #     collision_demarcation,
    #   )
    # )
    # #===================================================================================================#

    #============================= THE "NOT SO EASY" SOLUTION SCENE ====================================#
    medium_title = VGroup()
    medium_text = Text(r'The "Not So Easy" Solution', font="Brush Script MT")
    medium_border = Rectangle(width=medium_text.width * 1.25, height=medium_text.height * 2.5)
    medium_title.add(medium_text, medium_border)

    self.play(
      AnimationGroup(
        Write(medium_title),
        lag_ratio=.75
      )
    )

    self.play(
      FadeOut(medium_title)
    )

    self.play(
      self.camera.frame.animate.set_width(track.width * .95),
      FadeIn(track.shift(DOWN).set_color("#6a6a6a"))
    )

    # Animate the creation of the complex trains.
    left_complex_train = SVGMobject('./_2024YT/fly_2trains/assets/complex_train.svg')\
      .scale(0.2)\
      .rotate(PI, UP)\
      .set_color(WHITE)\
      .next_to(track, direction=UP, buff=0.02)\

    right_complex_train = SVGMobject('./_2024YT/fly_2trains/assets/complex_train.svg')\
      .scale(0.2)\
      .set_color(WHITE)\
      .next_to(track, direction=UP, buff=0.02)\

    self.play(
      AnimationGroup(
        Write(left_complex_train.shift(LEFT * left_complex_train.width * 1.6)),
        Write(right_complex_train.shift(RIGHT * right_complex_train.width * 1.6)),
        lag_ratio=.75
      ),
      run_time=2
    )

    # Set the initital position of the Gojo Fly to be at the left complex train, then show the creation
    gojo_fly.next_to(left_complex_train, direction=RIGHT, buff=0.025)

    self.camera.frame.save_state()

    self.play(
      AnimationGroup(
        self.camera.frame.animate.move_to(gojo_fly).set_height(gojo_fly.height * 3),
        Create(gojo_fly),
        lag_ratio=1
      )
    )

    # TODO: Create a method that allows the fly to oscillate in place.
    self.play(
      self.camera.frame.animate.restore()
    )

    left_train_velocity_annot.next_to(left_complex_train, direction=UP)
    right_train_velocity_annot.next_to(right_complex_train, direction=UP)
    left_train_velocity_vector.scale(1.33 * 0.5, True)
    right_train_velocity_vector.scale(1.33 * 0.5, True)

    gojo_fly_velocity_vector = Arrow(start=LEFT, end=RIGHT).next_to(gojo_fly, direction=UP, buff=.1).scale(.75, True)
    gojo_fly_velocity_label = MathTex("v_1 = 100 \, \mathrm{km/hr}").next_to(gojo_fly_velocity_vector, direction=UP, buff=.1).scale(.5)
    gojo_fly_velocity_annot = VGroup(gojo_fly_velocity_vector, gojo_fly_velocity_label)

    self.play(
      Write(gojo_fly_velocity_annot),
      Write(left_train_velocity_annot),
      Write(right_train_velocity_annot)
    )

    # Create box at the top of the screen for doing the calculations
    self.play(
      self.camera.frame.animate.shift(UP * 1.5)
    )

    solution_demarcation = Line(start=UP * 6.5, end=DOWN * 0.5)
    self.play(
      Write(solution_demarcation)
    )

    total_fly_distance_covered = MathTex(r"S_{\tiny \text{fly total}} =\ ?")\
        .next_to(solution_demarcation, direction=LEFT, buff=2)\
        .align_to(solution_demarcation, direction=UP)\
        .shift(DOWN * 0.65)

    total_distance_relationship_per_leg = MathTex(r"s_{\tiny \text{leg}} = s_{\tiny \text{fly}} + s_{\tiny \text{train}}")\
        .next_to(solution_demarcation, direction=RIGHT, buff=2)\
        .align_to(solution_demarcation, direction=UP)\
        .shift(DOWN * 0.65)

    self.play(
      Write(total_fly_distance_covered)
    )

    self.play(
      Write(
        total_distance_relationship_per_leg
      )
    )

    #----------------------------- The animation of the first two leg trips -------------------------------------------------#
    gojo_fly.roam(left_complex_train, right_complex_train, infiniteRoam=False)

    self.play(
      left_complex_train.animate(rate_func=linear).shift((RIGHT * left_complex_train.width * 1.6 - np.array((left_complex_train.width/2 - 0.05, 0.0, 0.0)))/2),
      right_complex_train.animate(rate_func=linear).shift((LEFT * right_complex_train.width * 1.6 + np.array((right_complex_train.width/2 - 0.05, 0.0, 0.0)))/2),
      # gojo_fly.animate(rate_func=linear).move_to((right_complex_train.get_left()[0] - (right_complex_train.width * 0.5), right_complex_train.get_left()[1], right_complex_train.get_left()[2])),
      run_time=5,
    )

    # def fly_leg_journey(leg: int):

    #   pass

    # for leg in range(7):

    #   pass

    # Day 3: TODO: Work on the Hard Solution

    # Day 4: TODO: Record voiceover and work on half of the more complex solution

    # Day 5: TODO: Work on the other half of the more complex solution

    # Day 6: TODO: Finishihng touches and edit the animations

    # Day 7: TODO: Edit it Adobe After EFfects

    #---------------- EASY SOLUTION ----------------#
    # Save the state of the fly and remove it from the scene
    # gojo_fly.save_state()

    # self.play(Unwrite(gojo_fly))
