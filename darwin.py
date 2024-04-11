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
