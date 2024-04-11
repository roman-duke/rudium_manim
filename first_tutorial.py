from manim import *

# class CreateCircle(Scene):
#   def construct(self):
#     circle = Circle()                         # create a circle
#     circle.set_fill(PINK, opacity=0.5)        # set color and transparency

#     square = Square()                         # create a square
#     square.rotate(PI / 4)                     # rotate a certain amount

#     self.play(Create(square))                 # animate the creation of the square
#     self.play(Transform(square, circle))      # interpolate the square into the circle
#     self.play(FadeOut(square))                # fade out animation

## POSITIONING Mobjects
class SquareAndCircle(Scene):
  def construct(self):
    circle = Circle()                           # create a circle
    circle.set_fill(PINK, opacity=0.5)          # set the color and transparency

    square = Square()                           # create a square
    square.set_fill(BLUE, opacity=0.5)          # set the color and transparency

    square.next_to(circle, RIGHT, buff=.5)     # set the position
    self.play(Create(circle), Create(square))   # show the shapes on screen


## Using .animate syntax to animate methods
class AnimatedSquareToCircle(Scene):
  def construct(self):
    circle = Circle()                           # create a circle
    square = Square()                           # create a square

    self.play(Create(square))                   # show the square on the screen
    self.play(square.animate.rotate(PI / 4))    # rotate the square
    self.play(
      ReplacementTransform(square, circle)
    ) # transform the square into a circle
    self.play(
      circle.animate.set_fill(PINK, opacity=0.5)
    ) # color the circle on the screen


## Dealing with sections
class Sections(Scene):
  def construct(self):
    circle = Circle()
    square = Square()

    square.next_to(circle, UP, buff=.5)

    self.play(Create(circle))
    self.play(
      ReplacementTransform(circle, square)
    )

    self.next_section()

    triangle = Triangle()

    self.play(
      triangle.animate.rotate(PI / 4)
    )


## Deep dive into Manim's internals
class ToyExample(Scene):
  def construct(self):
    orange_square = Square(color=ORANGE, fill_opacity=0.5)
    blue_circle = Circle(color=BLUE, fill_opacity=0.5)
    self.add(orange_square)
    self.play(ReplacementTransform(orange_square, blue_circle, run_time=3))
    small_dot = Dot()
    small_dot.add_updater(lambda mob: mob.next_to(blue_circle, DOWN))
    self.play(Create(small_dot))
    self.play(blue_circle.animate.shift(RIGHT))
    self.wait()
    self.play(FadeOut(blue_circle, small_dot))


## VMobjects
class VMobjectDemo(Scene):
  def construct(self):
    plane = NumberPlane()
    my_vmobject = VMobject(color=GREEN)
    my_vmobject.points = [
      np.array([-2, -1, 0]),                    # start of first curve
      np.array([-3, 1, 0]),
      np.array([0, 3, 0]),
      np.array([1, 3, 0]),                      # end of first curve
      np.array([1, 3, 0]),                      # start of second curve
      np.array([0, 1, 0]),
      np.array([4, 3, 0]),
      np.array([4, -2, 0]),                     # end of second curve
    ]
    handles = [
      Dot(point, color=RED) for point in 
      [[-3, 1, 0], [0, 3, 0], [0, 1, 0], [4, 3, 0]]
    ]
    handle_lines = [
      Line(
        my_vmobject.points[ind],
        my_vmobject.points[ind+1],
        color=RED,
        stroke_width=2
      ) for ind in range(0, len(my_vmobject.points), 2)
    ]
    self.add(plane, *handles, *handle_lines, my_vmobject)
