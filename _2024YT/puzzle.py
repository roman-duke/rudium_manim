from manim import *

class Puzzle(Scene):
  def construct(self):
    gnuSVG = SVGMobject('./_2024YT/fly_2trains/assets/manim_svg_test.svg')

    self.play(Write(gnuSVG), run_time=3)
