from manim import *
import random

class Birthday(MovingCameraScene):
  def construct(self):
    # birth_year = Tex("1993").shift(LEFT * 1.5)
    # birth_year = "1993"
    dummy = Tex("1")
    by0 = Tex("1").shift(LEFT * dummy.width * 2)
    by1 = Tex("9").next_to(by0, RIGHT, 0.05)
    by2 = Tex("8").next_to(by1, RIGHT, 0.05)
    by3 = Tex("2").next_to(by2, RIGHT, 0.05)
    age = Tex("43")
    post_fix = Tex("rd").scale(.45)
    happy = Tex("Happy").scale(.85)

    year_group = VGroup(by0, by1, by2, by3)

    self.play(Write(year_group))
    self.camera.frame.save_state()

    #zoom for the camera to fill in the entire view + a bit of space
    self.play(self.camera.frame.animate.set_height(year_group.height * 6))

    arrow = Arrow(start=LEFT, end=RIGHT).scale(0.35, True).next_to(year_group, RIGHT)

    curr_year = Tex("2025").next_to(arrow, RIGHT)

    self.play(
      AnimationGroup(
        self.camera.frame.animate.move_to(arrow),
        Write(arrow),
        Write(curr_year),
        lag_ratio=.5
      )
    )

    self.play(
      AnimationGroup(
        FadeOut(
          arrow,
          curr_year,
          lag_ratio=.5
        ),
        self.camera.frame.animate.move_to(year_group),
        lag_ratio=1
      )
    )

    self.play(year_group.animate.scale(.75))

    self.play(
      AnimationGroup(
        FadeOut(
          year_group[0],
          year_group[1],
        ),
      )
    )

    year_group.remove(year_group[0], year_group[1])

    self.play(
      ReplacementTransform(year_group, age),
    )

    self.play(
      year_group[0].animate.set_color("#0496FF"),
      year_group[1].animate.set_color("#0496FF"),
    )

    # self.play(
    #   Swap(year_group[-1], year_group[0], path_arc=120 * DEGREES),
    #   run_time=.75
    # )

    # self.play(
    #   year_group.animate.arrange(LEFT, .025),
    # )

    happy.next_to(year_group, LEFT, .15)

    post_fix.next_to(year_group, RIGHT, .075).align_to(year_group, DOWN)

    self.play(
      self.camera.frame.animate.shift(LEFT * happy.width/2),
      AnimationGroup(
        FadeIn(
          happy,
        ),
        FadeIn(
          post_fix,
        ),
        lag_ratio=.35
      )
    )

    self.play(
      self.camera.frame.animate.scale(1.5)
    )

    colors = [
      "#FF6392",
      "#FFBC42",
      "#006BA6",
      "#EEEBD0",
      "#FF6392",
    ]
    # colors = [
    #   "#FFD700", "#FF4500", "#00CED1", "#9932CC", "#32CD32"
    # ]

    frame_width = self.camera.frame_width
    frame_height = self.camera.frame_height

    num_points = 36

    points = [
      np.array([
        random.uniform(-frame_width / 2, frame_width / 2),
        random.uniform(-frame_height / 2, frame_height / 2),
        0,
      ])
      for _ in range(num_points)
    ]

    self.play(
      AnimationGroup(
        AnimationGroup(
          *[
            Flash(
              points[i],
              flash_radius=random.uniform(0.1, 0.35),
              line_length=random.uniform(.075, .15),
              line_stroke_width=random.uniform(1.5, 3),
              num_lines=random.uniform(10, 30),
              color=random.choice(colors))
            for i in range(0, int(len(points)/3))
          ],
        ),

        AnimationGroup(
          *[
            Flash(
              points[i],
              flash_radius=random.uniform(0.1, 0.35),
              line_length=random.uniform(.075, .15),
              line_stroke_width=random.uniform(1.5, 3),
              num_lines=random.uniform(10, 30),
              color=random.choice(colors))
            for i in range(int(len(points)/3), int(len(points) * 2 / 3))
          ],
        ),

        AnimationGroup(
          *[
            Flash(
              points[i],
              flash_radius=random.uniform(0.1, 0.35),
              line_length=random.uniform(.075, .15),
              line_stroke_width=random.uniform(1.5, 3),
              num_lines=random.uniform(10, 30),
              color=random.choice(colors))
            for i in range(int(len(points) * 2 / 3), len(points))
          ],
        ),

        lag_ratio=.35
      )
    )
