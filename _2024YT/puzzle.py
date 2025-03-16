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
    self.infinite_roam = False
    self.roam_trips = 0
    self._roam_count = 0
    self.roam_current_trip = False

  def get_obstacle_point_tracker(self, obstacle1: VMobject, obstacle2: VMobject) -> dict[int, float]:
    """Gets the current points of the obstacles we actually need only the x coord"""
    p1 = obstacle1.get_right()[0]
    p2 = obstacle2.get_left()[0]

    return {
      -1: p1,
      1: p2
    }

  def get_relevant_extreme(self):
    """Gets the relevant coord of the fly mobject"""
    p1 = self.fly.get_left()[0]
    p2 = self.fly.get_right()[0]

    return {
      -1: p1,
      1: p2
    }

  def set_infinite_roam(self, should_roam: bool):
    """Sets the infinite roam property of the fly"""
    self.infinite_roam = should_roam

  def set_roam_trips(self, roam_trips):
    self.roam_trips = roam_trips

  def roam_update(self):
    """Updates the number of trips that the fly has taken"""
    self._roam_count += 1
    if self._roam_count == self.roam_trips:
      self.infinite_roam = True

  def update_direction(self, dir: int):
    """Updates the direction of the fly"""
    self.direction = dir

  def restore_position(self):
    return super().restore()

  def set_force_roam_trip(self, roam_current_trip):
    self.roam_current_trip = roam_current_trip

  def roam(self, ob1: VMobject, ob2: VMobject, infiniteRoam=True, roam_trips=0):
    """Allows the fly to roam horizontally, changing direction if a collision is detected"""
    self.set_infinite_roam(infiniteRoam)
    self.set_roam_trips(roam_trips)
    # Add an updater to track the motion of the left and right trains
    def obstacle_updater(mob: VMobject, dt):
      # if self.direction == 1:
      has_not_collided = (self.get_obstacle_point_tracker(ob1, ob2)[self.direction] - self.get_relevant_extreme()[self.direction]) * self.direction >= ((mob.width/2 - SMALL_BUFF) * self.direction)

      has_collided = not has_not_collided

      if (has_not_collided):
        mob.move_to(
          np.array((
            mob.get_center()[0] + .0625 * self.direction,
            mob.get_center()[1],
            0
          )),
        )

      elif has_collided and (self.infinite_roam or self.roam_current_trip):
        self.flip()
        self.update_direction(self.direction * -1)
        self.set_force_roam_trip(False)

      else:
        self.suspend_roaming()

    self.add_updater(obstacle_updater)

  def resume_roaming(self):
    # self.set_infinite_roam(True)
    self.resume_updating()

  def suspend_roaming(self):
    """We need this to basically suspend running the updater function, but update a go-ahead flag to be used when the updates resume"""
    self.set_force_roam_trip(True)
    self.roam_update()
    self.suspend_updating()

  def clear_all_updaters(self):
    self.clear_updaters()

class ComplexTrain(SVGMobject):
  def __init__(self, file_name, color, direction, **kwargs):
    super().__init__(file_name, **kwargs)
    self.train = SVGMobject(file_name).set_color(color)
    self.direction = direction
    self.roaming_suspended = False
    self.add(self.train)

  def roam_before_fly_contact(self, fly: GojoFly, target: SVGMobject):
    """
      Allows the train to basically keep moving till it comes in contact with the fly
      or till another of the target objects in the vicinity comes in contact with the fly.
    """
    def train_updater(mob: VMobject):
      train_relevant_extreme = mob.get_right() if self.direction == 1 else mob.get_left()
      fly_center = fly.get_center()
      buff_contact = -fly.width/2 if self.direction == 1 else fly.width/2

      has_not_collided = (train_relevant_extreme[0] - fly_center[0]) * self.direction <= self.direction * buff_contact

      if (has_not_collided):
        mob.move_to((
          np.array((
            mob.get_center()[0] + .03125 * self.direction,
            mob.get_center()[1],
            0
          ))
        ))

        if target.roaming_suspended:
          target.resume_roaming()

      elif not has_not_collided:
        target.pause_roaming()

    self.add_updater(train_updater)

  def pause_roaming(self):
    """Pauses update of the train with every frame"""
    self.roaming_suspended = True
    self.suspend_updating()

  def resume_roaming(self):
    """Resumes update of the train with every frame"""
    self.roaming_suspended = False
    self.resume_updating()

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
    # medium_title = VGroup()
    # medium_text = Text(r'The "Not So Easy" Solution', font="Brush Script MT")
    # medium_border = Rectangle(width=medium_text.width * 1.25, height=medium_text.height * 2.5)
    # medium_title.add(medium_text, medium_border)

    # self.play(
    #   AnimationGroup(
    #     Write(medium_title),
    #     lag_ratio=.75
    #   )
    # )

    # self.play(
    #   FadeOut(medium_title)
    # )

    # self.play(
    #   self.camera.frame.animate.set_width(track.width * .95),
    #   FadeIn(track.shift(DOWN).set_color("#6a6a6a"))
    # )

    # # Animate the creation of the complex trains.
    # left_complex_train = ComplexTrain('./_2024YT/fly_2trains/assets/complex_train.svg', WHITE, direction=1)\
    #   .scale(0.2)\
    #   .rotate(PI, UP)\
    #   .next_to(track, direction=UP, buff=0.02)\
    #   .set_z_index(2)

    # right_complex_train = ComplexTrain('./_2024YT/fly_2trains/assets/complex_train.svg', WHITE, direction=-1)\
    #   .scale(0.2)\
    #   .next_to(track, direction=UP, buff=0.02)\
    #   .set_z_index(2)

    # self.play(
    #   AnimationGroup(
    #     Write(left_complex_train.shift(LEFT * left_complex_train.width * 1.6)),
    #     Write(right_complex_train.shift(RIGHT * right_complex_train.width * 1.6)),
    #     lag_ratio=.75
    #   ),
    #   run_time=2
    # )

    # # Set the initital position of the Gojo Fly to be at the left complex train, then show the creation
    # gojo_fly.next_to(left_complex_train, direction=RIGHT, buff=0.025)

    # self.camera.frame.save_state()

    # self.play(
    #   AnimationGroup(
    #     self.camera.frame.animate.move_to(gojo_fly).set_height(gojo_fly.height * 3),
    #     Write(gojo_fly),
    #     lag_ratio=1
    #   )
    # )

    # # TODO: Create a method that allows the fly to oscillate in place.
    # self.play(
    #   self.camera.frame.animate.restore()
    # )

    # left_train_velocity_annot.next_to(left_complex_train, direction=UP)
    # right_train_velocity_annot.next_to(right_complex_train, direction=UP)
    # left_train_velocity_vector.scale(1.33 * 0.5, True)
    # right_train_velocity_vector.scale(1.33 * 0.5, True)

    # gojo_fly_velocity_vector = Arrow(start=LEFT, end=RIGHT).next_to(gojo_fly, direction=UP, buff=.1).scale(.75, True)
    # gojo_fly_velocity_label = MathTex("v_1 = 100 \, \mathrm{km/hr}").next_to(gojo_fly_velocity_vector, direction=UP, buff=.1).scale(.5)
    # gojo_fly_velocity_annot = VGroup(gojo_fly_velocity_vector, gojo_fly_velocity_label)

    # self.play(
    #   Write(gojo_fly_velocity_annot),
    #   Write(left_train_velocity_annot),
    #   Write(right_train_velocity_annot)
    # )

    # # Create box at the top of the screen for doing the calculations
    # self.play(
    #   self.camera.frame.animate.shift(UP * 1.5)
    # )

    # solution_demarcation = Line(start=UP * 6.5, end=DOWN * 0.5)
    # self.play(
    #   Write(solution_demarcation)
    # )

    # total_fly_distance_covered = MathTex(r"S_{\tiny \text{fly total}} =\ ?")\
    #     .next_to(solution_demarcation, direction=LEFT, buff=2)\
    #     .align_to(solution_demarcation, direction=UP)\
    #     .shift(DOWN * 0.65)

    # def get_distance_relationship_for_current_leg(leg_no="n"):
    #   s_leg = r"{{ s_{\tiny \text{leg}_" + f"{leg_no}" + r"} }}"
    #   s_fly = r"{{ s_{\tiny \text{fly}_" + f"{leg_no}" + r"} }}"
    #   s_train = r"{{ s_{\tiny \text{train}_" + f"{leg_no}" + r"} }}"
    #   return MathTex(rf"{s_leg} = {s_fly} + {s_train}")

    # def get_mildly_simplified_distance_relationship_for_current_leg(leg_no="n"):
    #   s_leg = r"{{ s_{\tiny \text{leg}_" + f"{leg_no}" + r"} }}"
    #   s_fly = r"{{ s_{\tiny \text{fly}_" + f"{leg_no}" + r"} }}"
    #   s_train = r"{{ \frac{1}{2}s_{\tiny \text{fly}_" + f"{leg_no}" + r"} }}"
    #   return MathTex(rf"{s_leg} = {s_fly} + {s_train}")

    # def get_overly_simplified_distance_relationship_for_current_leg(leg_no="n"):
    #   s_leg = r"{{ s_{\tiny \text{leg}_" + f"{leg_no}" + r"} }}"
    #   s_simplified = r"{{ \frac{3}{2}s_{\tiny \text{fly}_" + f"{leg_no}" + r"} }}"
    #   s_fly = r"{{ s_{\tiny \text{fly}_" + f"{leg_no}" + r"} }}"
    #   s_rearranged = r"{{ \frac{2}{3}s_{\tiny \text{leg}_" + f"{leg_no}" + r"} }}"

    #   return MathTex(rf"{s_leg} = {s_simplified} \\ {s_fly} = {s_rearranged}")

    # # This is a very impure function, but lol, what do I know about functional programming
    # def append_to_partial_sum(leg_no=1):
    #   partial_sum = ''
    #   for i in range(leg_no):
    #     partial_sum += r"{{ \frac{2}{3}s_{\tiny \text{leg}_" + f"{i + 1}" + r"} }}" + r" + "

    #   result = r"S_{\tiny \text{fly total}} = " + partial_sum + r"..."

    #   return MathTex(result)\
    #     .next_to(solution_demarcation, direction=LEFT, buff=2)\
    #     .align_to(solution_demarcation, direction=UP)\
    #     .shift(DOWN * 0.65)

    # total_distance_relationship_per_leg = get_distance_relationship_for_current_leg()\
    #     .next_to(solution_demarcation, direction=RIGHT, buff=2)\
    #     .align_to(solution_demarcation, direction=UP)\
    #     .shift(DOWN * 0.65)

    # self.play(
    #   Write(total_fly_distance_covered)
    # )

    # self.play(
    #   Write(
    #     total_distance_relationship_per_leg
    #   )
    # )

    # # Remove the velocity vectors from the scene
    # self.play(
    #   Unwrite(gojo_fly_velocity_annot),
    #   Unwrite(left_train_velocity_annot),
    #   Unwrite(right_train_velocity_annot)
    # )

    # self.remove(gojo_fly_velocity_annot, left_train_velocity_annot, right_train_velocity_annot)

    # #----------------------------- Display the total available initial distance -------------------------------------------------#
    # distance_brace = BraceBetweenPoints(left_complex_train.get_right(), right_complex_train.get_left()).next_to(track, direction=DOWN, buff=.2)
    # distance_between_trains = MathTex(r"s_{\text{leg.1}}").next_to(distance_brace, direction=DOWN, buff=.2)

    # self.play(
    #   Write(distance_brace),
    #   Write(distance_between_trains)
    # )

    # self.play(
    #   Unwrite(distance_brace),
    #   Unwrite(distance_between_trains)
    # )
    # #----------------------------- The animation of the first two leg trips -------------------------------------------------#
    # # Add a brace to illustrate the distance covered by the train
    # # Add a brace to illustrate the distance covered by the fly
    # initial_left_train_pos = left_complex_train.get_right()
    # initial_right_train_pos = right_complex_train.get_left()
    # initial_fly_pos = gojo_fly.get_left() if gojo_fly.direction == 1 else gojo_fly.get_right()

    # # Add markers to show the reference distance between the trains
    # left_train_marker = Dot(initial_left_train_pos, color=GRAY).shift(DOWN * 0.5)
    # right_train_marker = Dot(initial_right_train_pos, color=GRAY).shift(DOWN * 0.5)

    # self.play(
    #   Write(left_train_marker),
    #   Write(right_train_marker),
    # )

    # gojo_fly.roam(left_complex_train, right_complex_train, infiniteRoam=False, roam_trips=3)
    # left_complex_train.roam_before_fly_contact(gojo_fly.fly, right_complex_train)
    # right_complex_train.roam_before_fly_contact(gojo_fly.fly, left_complex_train)

    # self.play(
    #   self.camera.frame.animate.scale(1),
    #   run_time=8
    # )

    # left_train_brace = BraceBetweenPoints(initial_left_train_pos, left_complex_train.get_right()).shift(DOWN*.25)
    # left_complex_train_annot = MathTex(r"s_{\text{left train leg 1}}").next_to(left_train_brace, direction=DOWN, buff=.2)

    # right_train_brace = BraceBetweenPoints(right_complex_train.get_left(), initial_right_train_pos).shift(DOWN*.25)
    # right_complex_train_annot = MathTex(r"s_{\text{right train leg 1}}").next_to(right_train_brace, direction=DOWN, buff=.2)

    # # Distance covered by the fly
    # fly_distance_brace = BraceBetweenPoints(initial_fly_pos, gojo_fly.get_center(), direction=UP).shift(UP)
    # fly_distance_annot = MathTex(r"s_{\text{fly\_leg\_1}}").next_to(fly_distance_brace, direction=DOWN, buff=.2)

    # self.play(
    #   Write(left_train_brace),
    #   Write(right_train_brace),
    #   Write(left_complex_train_annot),
    #   Write(right_complex_train_annot),
    #   Write(fly_distance_brace),
    #   Write(fly_distance_annot)
    # )

    # # Indicate the respective distance braces
    # self.play(
    #   Indicate(left_train_brace)
    # )

    # self.play(
    #   Indicate(right_train_brace)
    # )

    # self.play(
    #   Indicate(fly_distance_brace)
    # )

    # # Visual illustration of the distance covered by the train and the fly
    # self.play(
    #   Unwrite(left_complex_train_annot),
    #   Unwrite(right_complex_train_annot),
    #   Unwrite(fly_distance_annot)
    # )

    # self.wait(1)

    # self.play(
    #   right_train_brace.animate.next_to(fly_distance_brace, direction=LEFT, buff=0)\
    #     .shift(DOWN*0.5 + RIGHT*right_train_brace.width),
    # )

    # # Honestly this could be more declarative, but at this point I am so tired of working on this project and I just
    # # want to try and wrap it up so I am going to leave things procedural
    # # besides what's the point of abstracting it into a method and trying to be declarative when the animation is only
    # # going to be repeated twice? Exactly

    # partial_sum = MathTex('')

    # for i in range(1, 4):
    #   current_distance_relationship = get_distance_relationship_for_current_leg(i)\
    #             .next_to(total_distance_relationship_per_leg, direction=DOWN, buff=.5)

    #   mildly_simplified_current_distance_relationship = get_mildly_simplified_distance_relationship_for_current_leg(i)\
    #             .next_to(current_distance_relationship, direction=DOWN, buff=.5)

    #   overly_simplified_distance_relationship = get_overly_simplified_distance_relationship_for_current_leg(i)\
    #             .next_to(mildly_simplified_current_distance_relationship, direction=DOWN, buff=.5)

    #   self.play(
    #     Write(current_distance_relationship)
    #   )

    #   self.play(
    #     TransformMatchingTex(
    #       current_distance_relationship,
    #       mildly_simplified_current_distance_relationship
    #     )
    #   )

    #   self.play(
    #     Write(overly_simplified_distance_relationship)
    #   )

    #   partial_sum = append_to_partial_sum(i)

    #   self.play(
    #     AnimationGroup(
    #       Unwrite(total_fly_distance_covered),
    #       Transform(
    #         overly_simplified_distance_relationship,
    #         partial_sum,
    #         replace_mobject_with_target_in_scene=True
    #       ),
    #       lag_ratio=.95
    #     )
    #   )

    #   self.play(
    #     Unwrite(left_train_brace),
    #     Unwrite(right_train_brace),
    #     Unwrite(fly_distance_brace),
    #   )

    #   gojo_fly.resume_roaming()
    #   left_complex_train.resume_roaming()
    #   right_complex_train.resume_roaming()

    #   self.play(
    #     self.camera.frame.animate.scale(1),
    #     run_time=(4/i)
    #   )

    #   # Remove expressions for the previous leg
    #   self.play(
    #     Unwrite(partial_sum) if i != 3 else partial_sum.animate.scale(1),
    #     Unwrite(mildly_simplified_current_distance_relationship)
    #   )

    # self.play(
    #   Indicate(partial_sum),
    # )

    # # Shift demarcation to create more room for the equation
    # self.play(
    #   AnimationGroup(
    #     Unwrite(total_distance_relationship_per_leg),
    #     solution_demarcation.animate.shift(RIGHT * 3),
    #     lag_ratio=1
    #   )
    # )

    # simplified_partial_sum = MathTex(r"= {{ \frac{2}{3}s_{\tiny \text{leg}_1} +\
    #                                   \frac{1}{3}(\frac{2}{3}s_{\tiny \text{leg}_1}) +\
    #                                  \frac{1}{3}(\frac{1}{3})(\frac{2}{3}s_{\tiny \text{leg}_1}) +\
    #                                  ... + \frac{1}{3}^{n-1}\frac{2}{3}s_{\tiny \text{leg}_1}}}"
    #                                  ).next_to(partial_sum, direction=DOWN, buff=.5)\
    #                                   .shift(RIGHT * 2.5)

    # self.play(
    #   Write(simplified_partial_sum)
    # )

    # infinite_geometric_sum = MathTex(
    #   r"\sum_{n=1}^\infty ar^n = \frac{a}{1 - r}, \quad \text{for } |r| < 1 \
    #   \\ \text{where } a = \frac{2}{3} \cdot s_{\text{leg}_1}, \quad r = \frac{1}{3} \
    #   \\ s_{\text{leg}_1} = 100\, \tiny \text{km}"
    # ).next_to(solution_demarcation, direction=RIGHT, buff=1)\
    #     .align_to(solution_demarcation, direction=UP)\
    #     .shift(DOWN * 0.65)

    # self.play(Write(infinite_geometric_sum))

    # final_expression = MathTex(r"= \frac{\frac{2}{3} \times 100}{1 - \frac{1}{3}} ").next_to(simplified_partial_sum, direction=DOWN, buff=1)

    # final_medium_answer = MathTex(r"100km").next_to(final_expression, direction=DOWN, buff=1)

    # self.play(Write(final_expression))


    # self.play(
    #   Write(final_medium_answer),
    # )

    # self.play(
    #   Indicate(final_medium_answer)
    # ),

    # self.wait(1)

    # self.clear()

    #=============================== THE "COMPLEX" SOLUTION SCENE ======================================#
    complex_text = Text(r'Complexity in Broader Contexts', font="Brush Script MT")

    self.play(
      Write(complex_text),
      run_time=3
    )

    self.play(
      FadeOut(complex_text)
    )

    frame_border =  Rectangle(width=self.camera.frame_width, height=self.camera.frame_height, color=BLUE_D)

    self.play(
      Write(frame_border),
      run_time=2
    )

    left_point = frame_border.get_critical_point(LEFT) + RIGHT * .5
    right_point = frame_border.get_critical_point(RIGHT) + LEFT * .5
    inner_border = Rectangle(width=(right_point - left_point)[0], height=0.005, color=LOGO_WHITE)
    complex_dot = Dot(color=LOGO_WHITE)

    self.play(
      Write(complex_dot)
    )

    self.play(
      Transform(complex_dot, inner_border, replace_mobject_with_target_in_scene=True)
    )

    self.play(
      inner_border.animate.stretch_to_fit_height(self.camera.frame_height * 0.85)
    )

    inner_border.set_fill(BLACK, 1)

    self.play(frame_border.animate.set_fill(BLUE_E, 1))
    self.wait(1)

    air_resistance = BulletedList(r"Air Resistance?", height=2, width=2)
    self.play(
      Write(air_resistance)
    )

    self.play(
      FadeOut(air_resistance)
    )

    air_resistance = Tex(r"{{ Air Resistance }} {{ }}").scale(.65)

    self.play(
      Write(air_resistance)
    )

    drag = Tex(r"{{ Air Resistance }} {{ (Drag) }}").scale(.65)

    self.play(
      TransformMatchingTex(air_resistance, drag)
    )

    self.play(
      drag.animate.shift(UP * 2.5)
    )

    # TODO: Show the equation of linear drag on the left hand-side and then
    # show the equation of quadratic drag on the right hand side in mini frames
    left_mini_frame = Rectangle(width=2.5, height=1.5).shift(LEFT*1.5 + DOWN)
    right_mini_frame = Rectangle(width=2.5, height=1.5).shift(RIGHT*1.5 + DOWN)

    left_branch = Arrow(start=drag.get_bottom(), end=left_mini_frame.get_top(), buff=SMALL_BUFF, stroke_width=3) \
        .scale(0.5, scale_tips=True).scale_to_fit_height(2)

    right_branch = Arrow(start=drag.get_bottom(), end=right_mini_frame.get_top(), buff=SMALL_BUFF, stroke_width=3) \
        .scale(0.5, scale_tips=True).scale_to_fit_height(2)

    self.play(
      Write(left_mini_frame),
      Write(right_mini_frame),
      Write(left_branch),
      Write(right_branch)
    )


    # Day 3: TODO: Work on the Hard Solution

    # Day 4: TODO: Record voiceover and work on half of the more complex solution

    # Day 5: TODO: Work on the other half of the more complex solution

    # Day 6: TODO: Finishihng touches and edit the animations

    # Day 7: TODO: Edit it Adobe After EFfects

    #---------------- EASY SOLUTION ----------------#
    # Save the state of the fly and remove it from the scene
    # gojo_fly.save_state()

    # self.play(Unwrite(gojo_fly))
