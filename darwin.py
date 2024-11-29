from manim import *
import random
import math

class NextTo(Scene):
  def construct(self):
    circle_array = [Circle(radius=0.5, color=WHITE)
                      for _ in range(4)]

    rectangle = Rectangle(width=5, height=3)

    # Using Python's equivalent of Javascript's spread syntax, --> "*"
    self.play(*[Create(mobject) for mobject in [*circle_array, rectangle]])

    positions_to_move_to = [LEFT, UP, RIGHT, DOWN]

    # move the circles such that they surround the rectangle
    self.play(
      *[circle_array[i].animate.next_to(rectangle, positions_to_move_to[i]) for i in range(len(circle_array))]
    )

class MoveTo(Scene):
  def construct(self):
    s1, s2, s3 = [Square() for _ in range(3)]

    self.play(*[Create(mob) for mob in [s1, s2, s3]])

    # align the square next to each other
    self.play(
      s1.animate.next_to(s2, LEFT),
      s3.animate.next_to(s2, RIGHT)
    )

    # create number for each of them
    t1, t2, t3 = [Tex(f"${i}$").scale(3) for i in range(3)]

    # move the numbers on top of the squares
    t1.move_to(s1)
    t2.move_to(s2)
    t2.move_to(s3)

    self.play(*[Write(mob) for mob in [t1, t2, t3]])

class TextAndMath(Scene):
  # Tex is being used for setting text, while MathTex for setting math
  def construct(self):
    text = Tex("Hello Manim!").shift(LEFT * 2.5)

    # Note the use of Python's r-strings for cleaner code
    formula = MathTex(r"\sum_{i=0}^\infty\frac{1}{2^i} = 2").shift(RIGHT * 2.5)

    self.play(Write(formula), Write(text))

    self.play(FadeOut(formula), FadeOut(text))

# All these notes and tasks in the comments would be transferred to Obsidian for later consumption

#--- TASKS ---#
# Shuffling animation
# Ideal pre-requisite below - swap animation
# The swap animation is, as the name suggests, used for swapping the position of two mobjects
# It possesses an optional parameter, path_arc, which determines the angle under which they are
# swapped

class Shuffle(Scene):
  def construct(self):
    # Create an array of 5 circles
    circle_list = [Circle(color=WHITE, radius=.5).shift(LEFT * -0.85 * (2*i - 4)) for i in range(5)]

    # Play a staggered animation of the creation of the circles
    self.play(
      LaggedStart(
        *[Write(o) for o in circle_list],
        lag_ratio=0.05,
        run_time=2
      )
    )

    self.play(*[o.animate.set_fill(WHITE, .5) for o in circle_list])

    # Now randomly highlight a circle and set a color, then fade out the color
    random_circle = random.choice(circle_list)
    self.play(random_circle.animate.set_color(RED_C))
    self.play(random_circle.animate.set_color(WHITE))

    # Now time to begin the random shuffling of the circles
    # There should be six shuffling cycles
    for _ in range(6):
      # randomly select two circles from the array and swap them
      circle_positions = [i for i in range(5)]
      first_rand_circle_choice = random.choice(circle_positions)
      circle_positions.pop(first_rand_circle_choice)
      second_rand_circle_choice = random.choice(circle_positions)

      # Get the two mobjects
      first_circle = circle_list[first_rand_circle_choice]
      second_circle = circle_list[second_rand_circle_choice]
      self.play(Swap(first_circle, second_circle, path_arc=130 * DEGREES))

      # Revert the circle array back to original state
      circle_positions.append(first_rand_circle_choice)

    # Now that animation is done, show the initially highlighted circle
    self.play(random_circle.animate.set_color(RED_C))


# BINARY SEARCH ANIMATION
class BinarySearch(Scene):
  def construct(self):
    # Creation of target number
    target = 5
    numbers_list = [i + 2 for i in range(10)]
    target_mobject = Tex(f"Target: ${target}$").scale(1).shift(UP * 2)

    squares_list = [Square(side_length=.65).shift(RIGHT * (1.11*i - 5)) for i in range(10)]

    self.play(*[Write(o) for o in squares_list])

    # create numbers for each of the sqaures and move them on top of the corresponding squares
    text_list = [Tex(f"${i + 2}$").scale(1).move_to(squares_list[i]) for i in range(10)]

    # now group them so that it is much easier to fade both the text and the square
    blocks = [VGroup(squares_list[i], text_list[i]) for i in range(len(squares_list))]

    # play the creation of the numbers on the squares
    self.play(*[Write(o) for o in text_list])

    # play the creation of the target text
    self.play(Write(target_mobject))

    # create three arrows --> two for local extremeties and one for guess position
    arrow_left = Arrow(start=DOWN, end=UP).next_to(squares_list[0], direction=DOWN, buff=0.075).scale(.75, True)
    arrow_right = Arrow(start=DOWN, end=UP).next_to(squares_list[-1], direction=DOWN, buff=0.15).scale(.75, True)
    arrow_guess = Arrow(start=DOWN, end=UP, stroke_color=RED_C).scale(.75, True)

    def binary_search():
      # the positions of the two initial extremeties
      min = 0
      max = len(squares_list) - 1

      # variable to know which index (min or max) changed. 0 indicates min changed, 1 indicated max changed

      # Animate the creation of the arrows only at initial extremeties
      self.play(Write(arrow_left), Write(arrow_right))

      def search_helper(min, max):
        nonlocal blocks

        # Generate random guess index and create target arrow at that location
        index = math.floor((min + max) / 2)
        self.play(Write(arrow_guess.next_to(squares_list[index], direction=DOWN, buff=.25)))

        # Check if guess is equal to target
        if (numbers_list[index] == target):
          self.play(
            FadeOut(arrow_guess),
            arrow_left.animate.next_to(squares_list[index], direction=DOWN),
            arrow_right.animate.next_to(squares_list[index], direction=DOWN),
            run_time=.5
          )
          self.play(squares_list[index].animate.set_color(GREEN_C))

        elif (numbers_list[index] < target):
          min_copy = min
          min = index + 1
          # Fix the left arrow under the left local extreme point,
          # fade the redundant blocks,
          # then fade out completely the guess arrow
          self.play(
            arrow_left.animate.next_to(squares_list[min], direction=DOWN),
            FadeOut(arrow_guess),
            *[blocks[i].animate.fade(.6) for i in range(min_copy, index + 1)]
          )

          search_helper(min, max)

        elif (numbers_list[index] > target):
          max_copy = max
          max = index - 1
          # Fix the right arrow under the right local extreme point,
          # fade the redundant blocks,
          # then fade out completely the guess arrow
          self.play(
            arrow_right.animate.next_to(squares_list[max], direction=DOWN),
            FadeOut(arrow_guess),
            *[blocks[i].animate.fade(.6) for i in range(index, max_copy + 1)]
          )

          search_helper(min, max)

      search_helper(min, max)

    binary_search()

class InscribedTriangle(Scene):
  def construct(self):
    label_list = ['x', 'y', 'z']
    # create three dots
    p1 = Dot(point=UP)
    p2 = Dot(point=DOWN + LEFT)
    p3 = Dot(point=DOWN + RIGHT)

    # create the three labels
    labels = [Tex(f"${label}$") for label in label_list]

    self.play(
      AnimationGroup(
        Write(p1),
        Write(p2),
        Write(p3),
        lag_ratio=.5
      )
    )

    def text_one_updater(t1: Tex):
      t1.next_to(p1, direction=UP, buff=.3)

    def text_two_updater(t2: Tex):
      t2.next_to(p2, direction=LEFT + .25*DOWN, buff=.3)

    def text_three_updater(t3: Tex):
      t3.next_to(p3, direction=RIGHT + .25*DOWN, buff=.3)

    def line_one_updater(line_one: Line):
      line_one.set_points_by_ends(p1.get_center(), p2.get_center())

    def line_two_updater(line_two: Line):
      line_two.set_points_by_ends(p2.get_center(), p3.get_center())

    def line_three_updater(line_three: Line):
      line_three.set_points_by_ends(p3.get_center(), p1.get_center())

    def circle_updater(circle: Circle):
      circle.replace(circle.from_three_points(p1.get_center(), p2.get_center(), p3.get_center()))

    # draw the initial lines
    line1 = Line(start=p1.get_center(), end=p2.get_center())
    line2 = Line(start=p2.get_center(), end=p3.get_center())
    line3 = Line(start=p3.get_center(), end=p1.get_center())

    line_one_updater(line1)
    line_two_updater(line2)
    line_three_updater(line3)

    self.play(
      AnimationGroup(
        Write(line1),
        Write(line2),
        Write(line3),
        lag_ratio=1,
        run_time=.85
      )
    )

    # create a circle from three points
    circle = Circle.from_three_points(p1.get_center(), p2.get_center(), p3.get_center())
    self.play(Write(circle))

    # Add the updater functions
    line1.add_updater(line_one_updater)
    line2.add_updater(line_two_updater)
    line3.add_updater(line_three_updater)

    circle.add_updater(circle_updater)

    # Now add the labels
    t1 = labels[0]
    t2 = labels[1]
    t3 = labels[2]

    text_one_updater(t1)
    text_two_updater(t2)
    text_three_updater(t3)

    self.play(
      FadeIn(t1, shift=UP * 0.5),
      FadeIn(t2, shift=UP*0.5),
      FadeIn(t3, shift=UP * 0.5)
    )

    t1.add_updater(text_one_updater)
    t2.add_updater(text_two_updater)
    t3.add_updater(text_three_updater)

    # Now move points two and three around
    self.play(
      p1.animate.shift(0.5 * RIGHT),
      p2.animate.shift(0.5 * LEFT),
    )


# I wasn't able to do the maze task successfully, I shall return to it later

# Hilbert's curve
class Path(Polygram):
  def __init__(self, points, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_points_as_corners(points)

  def get_important_points(self):
      """Returns the important points of the curve."""
      # shot explanation: Manim uses quadratic Bézier curves to create paths
      # > each curve is determined by 4 points - 2 anchor and 2 control
      # > VMobject's builtin self.points returns *all* points
      # > we, however, only care about the anchors
      # > see https://en.wikipedia.org/wiki/Bézier_curve for more details
      return list(self.get_start_anchors()) + [self.get_end_anchors()[-1]]

class HilbertCurve(Scene):
  def construct(self):
    # initial path to be passed to the hilbert_generator
    points = [LEFT + DOWN, LEFT + UP, RIGHT + UP, RIGHT + DOWN]

    # buff distance
    buff_dist = 1

    # path drawing runtime
    path_run_time = 1

    path, path_top_right, path_bottom_left, path_bottom_right = [Path([LEFT]) for _ in range(4)]

    animation_label = Tex("Hilbert's Curve")
    animation_label.shift(UP * 2.75)
    self.play(FadeIn(animation_label, shift=DOWN * 1.5))

    def hilbert_generator(n: int, points):
      nonlocal path_run_time
      nonlocal buff_dist
      nonlocal path
      nonlocal path_top_right
      nonlocal path_bottom_left
      nonlocal path_bottom_right

      # duplicate the path, so as to have something to show when you remove the inital path
      persistent_path = path.copy()
      self.add(persistent_path)
      self.remove(path)

      path = Path(points, color=WHITE)

      # Draw a path through these points
      self.play(Create(path), run_time=path_run_time)

      if (n == 0):
        # Stop recursion at this point
        return

      # self.play(path.animate.set_color(DARK_GRAY))

      # Remove all the pre-existing paths from the scene
      self.remove(persistent_path, path_top_right, path_bottom_left, path_bottom_right)

      # Create a copy of the path mobject and then move it to the right
      self.play(path.animate.scale(.5).shift(LEFT + UP).set_color(DARK_GRAY))
      path_top_right = path.copy()
      self.play(path_top_right.animate.next_to(path, RIGHT, buff=buff_dist))

      # create copies of the top left and top right paths
      path_bottom_left = path.copy()
      path_bottom_right = path_top_right.copy()

      # Now rotate them, while also shifting them downwards
      self.play(
        path_bottom_left.animate.rotate(-90 * DEGREES).next_to(path, DOWN, buff=buff_dist),
        path_bottom_right.animate.rotate(90 * DEGREES).next_to(path_top_right, DOWN, buff=buff_dist)
      )

      # Now swap the starting and ending points of both the bottom left and bottom right path mobjects
      pp_bottom_left = path_bottom_left.get_important_points()
      pp_bottom_left.reverse()
      # pp_bottom_left[0], pp_bottom_left[-1] = pp_bottom_left[-1], pp_bottom_left[0]
      pp_bottom_right = path_bottom_right.get_important_points()
      pp_bottom_right.reverse()
      # pp_bottom_right[0], pp_bottom_right[-1] = pp_bottom_right[-1], pp_bottom_right[0]

      # Retrieve the path points for the top left and top right
      pp_top_left = path.get_important_points()
      pp_top_right = path_top_right.get_important_points()

      # concatenate them
      path_points = pp_bottom_left + pp_top_left + pp_top_right + pp_bottom_right

      # Reduce the buff distance for the next execution
      buff_dist *= 0.5

      # Reduce run_time duration of path drawing for the next execution
      path_run_time *= 1.4

      hilbert_generator(n-1, path_points)

    hilbert_generator(5, points)

class StarrySky(Scene):
  def construct(self):
    random.seed(0xDEADBEEF)

    vertices = [i for i in range(1, 12)]
    edges = [(1, 2), (2, 3), (3, 4), (2, 4), (2, 5), (6, 5),
                 (1, 7), (5, 7), (2, 8), (1, 9), (10, 8), (5, 11)]

    def RandomStar():
      """Create a pretty random star."""
      return Star(
        random.randint(5, 7),
        fill_opacity=1,
        outer_radius=0.1,
        color=WHITE).rotate(random.uniform(0, 2 * PI)
      )

    def RandomSkyLine(u, v, z_index=None):
      return DashedLine(u, v, dash_length=random.uniform(0.03, 0.07), z_index=z_index)

    # custom graph with star vertices and dashed line edges
    g = Graph(vertices, edges,
              layout_config={"seed": 0},
              vertex_type=RandomStar,
              edge_type=RandomSkyLine,
              ).scale(2).rotate(-PI / 2)

    self.play(Write(g))

    self.play(FadeOut(g))

class MovingCameraExample(MovingCameraScene):
  def construct(self):
    square = Square()

    self.play(Write(square))

    self.camera.frame.save_state()

    # zoom for the square to fill in the entire view
    self.play(self.camera.frame.animate.set_height(square.height * 1.5))

    circle = Circle().next_to(square, LEFT)

    # move the camera to the new object
    self.play(
      AnimationGroup(
        self.camera.frame.animate.move_to(circle),
        Write(circle),
        lag_ratio=0.5
      )
    )

    self.wait(0.5)

    # zoom out (increasing frame size covers more of the screen)
    self.play(self.camera.frame.animate.scale(1.3))

    triangle = Triangle().next_to(square, RIGHT)

    # move the camera again
    self.play(
      AnimationGroup(
        self.camera.frame.animate.move_to(triangle),
        Write(triangle),
        lag_ratio=0.5
      )
    )

    self.wait(0.5)

    self.play(self.camera.frame.animate.restore())


class Fibonacci(MovingCameraScene):
  def construct(self):
    annotated_squares = VGroup()
    direction_array = [RIGHT, UP, LEFT, DOWN]
    fib_n2 = 1
    fib_n1 = 1

    # Create first square before the pattern kicks off
    square = Square()
    label = MathTex(f'{fib_n2}^2')
    label.scale(square.height/2).move_to(square)
    annotated_square = VGroup(square, label)

    annotated_squares.add(annotated_square)

    self.play(
      self.camera.frame.animate.scale(0.5),
      Write(annotated_squares)
    )

    self.camera.frame.save_state()

    # Create an array that stores all the points that would be used to anchor the fibonacci spiral
    square_anchors = [square.get_vertices()[0]]
    starting_point = square.get_vertices()[1]

    ## THIS FUNCTION IS SOOOO NOT PURE, lol
    def fib_pattern_generator(directions: list[Vector], fibSequenceIdx: int, fib_n2: int, fib_n1: int, square_group: VGroup, square_anchors: list[tuple[float, float, float]]):
      direction = directions[fibSequenceIdx%4-1]
      square = Square()

      if (direction == RIGHT).all() or (direction == LEFT).all():
        square.scale_to_fit_height(square_group.height)
      else:
        square.scale_to_fit_height(square_group.width)

      label = MathTex(f'{fib_n1}^2')


      label.scale(square.height / 2).move_to(square)
      annotated_square = VGroup(square, label)
      annotated_square.next_to(annotated_squares, direction=direction, buff=0)
      annotated_squares.add(annotated_square)

      square_anchors.append(square.get_vertices()[fibSequenceIdx%4])

      # Calculate the next fib number
      fib_n1, fib_n2 = (fib_n2 + fib_n1), fib_n1

      # Get the fibSequenceIdx
      fibSequenceIdx += 1

      self.play(
        AnimationGroup(
          # self.camera.frame.animate.scale(1 if (direction == RIGHT).all() or (direction == LEFT).all() else 2),
          self.camera.frame.animate.move_to(annotated_squares).scale(1 if (direction == RIGHT).all() or (direction == LEFT).all() else 2.5),
          FadeIn(annotated_square, shift=direction*1.25),
          lag_ratio=0.25,
        )
      )

      if fibSequenceIdx == 8:
        return

      else:
        fib_pattern_generator(directions, fibSequenceIdx, fib_n2, fib_n1, annotated_squares, square_anchors)

    fib_pattern_generator(direction_array, 1, fib_n2, fib_n1, annotated_squares, square_anchors)

    starting_dot = Dot().move_to(starting_point)
    moving_dot = Dot().move_to(starting_point)

    def follow_dot(camera: Camera):
      """An updater which continually makes the camera follow the movement of a point"""
      camera.move_to(moving_dot.get_center())

    self.camera.frame.add_updater(follow_dot)
    self.add(self.camera.frame)

    path = TracedPath(moving_dot.get_center)
    self.add(path)

    self.play(
      AnimationGroup(
        self.camera.frame.animate.restore().move_to(starting_point),
        Write(starting_dot),
        lag_ratio=1
      )
    )

    for p in square_anchors:
      self.play(
        Rotate(moving_dot, about_point=p, angle=PI/2),
        self.camera.frame.animate.scale(1.12),
        rate_func=linear
      )

    self.wait()

    # cleanup
    self.camera.frame.clear_updaters()

    self.play(
      AnimationGroup(
        self.camera.frame.animate.set_height(annotated_squares.height * 1.5).move_to(annotated_squares),
      )
      # FadeOut(annotated_squares),
      # Unwrite(path),
    )

# PLOTTING AND 3D SCENES
from math import sin, cos

class GraphExample(Scene):
  def construct(self):
    axes = Axes(x_range=[-10, 10], y_range=[-5, 5])
    labels = axes.get_axis_labels(x_label="x", y_label="y")

    def f1(t):
        """Parametric function of a circle."""
        return (cos(t) * 3 - 4.5, sin(t) * 3)

    def f2(t):
        """Parametric function of <3."""
        return (
            0.2 * (16 * (sin(t)) ** 3) + 4.5,
            0.2 * (13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)),
        )

    # the t_range parameter determines the range of the function parameter
    g1 = axes.plot_parametric_curve(f1, color=RED, t_range=[0, 2 * PI])
    g2 = axes.plot_parametric_curve(f2, color=BLUE, t_range=[-PI, PI])

    self.play(Write(axes), Write(labels))

    self.play(AnimationGroup(Write(g1), Write(g2), lag_ratio=0.5))

    self.play(Unwrite(axes), Unwrite(labels), Unwrite(g1), Unwrite(g2))


class Axes3DExample(ThreeDScene):
  def construct(self):
    axes = ThreeDAxes()

    x_label = axes.get_x_axis_label(Tex("x"))
    y_label = axes.get_y_axis_label(Tex("y").shift(1.8))

    # 3D variant of the Dot() object
    dot = Dot3D()

    # zoom out so we see the axes
    self.set_camera_orientation(zoom=0.5)

    self.play(FadeIn(axes), FadeIn(dot), FadeIn(x_label), FadeIn(y_label))

    self.wait(0.5)

    # animate the move of the camera to properly see the axes
    self.move_camera(phi=75 * DEGREES, theta=30*DEGREES, zoom=1, run_time=1.5)

    # built-in updater which begins camera rotation
    self.begin_ambient_camera_rotation(rate=0.15)

    # one dot for each direction
    upDot = dot.copy().set_color(RED)
    rightDot = dot.copy().set_color(BLUE)
    outDot = dot.copy().set_color(GREEN)

    self.wait(1)

    self.play(
      upDot.animate.shift(UP),
      rightDot.animate.shift(RIGHT),
      outDot.animate.shift(OUT),
    )

    self.wait(1)

    self.clear()

    cube = Cube(side_length=3, fill_opacity=1)
    self.begin_ambient_camera_rotation(rate=0.3)

    self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

    self.play(Write(cube), run_time=2)

    self.wait(3)

    self.play(Unwrite(cube), run_time=2)
