from manim import *
from curses.textpad import Textbox
from pickle import TRUE
from re import S
from turtle import fillcolor

import numpy as np
import random
from manim_slides import Slide

import sys

sys.path.append("../../src/")
from Util import Util


class Algo(Slide):
    def construct(self):
        title = Title("Implementing the Dynamic Algorithm")
        self.play(Write(title))
        self.next_slide()
        Util.cleanUp(self)
        code_scale = 0.8
        buffer = 0.5
        map = {
            "$L(1)$": YELLOW,
            "$n$": WHITE,
            "$S$": GOLD,
            "$\leftarrow$": GREEN,
            "$L(1)$": WHITE,
            ";": WHITE,
            "max_{(i, j)": YELLOW,
            "return": WHITE,
            "$i$": WHITE,
            "\{": WHITE,
            "\}": WHITE,
            "\cup": GREEN,
            "while": RED_D,
            "if": RED_D,
        }
        code = [
            "\\textbf{Schedule()}",
            "\\{",
            "  $L(1) \\leftarrow \\text{Credit}(1);$",
            "  \\textbf{for} $i \\leftarrow 2$ \\textbf{to} $n$",
            "  \\{",
            "    $L(i) \\leftarrow \\text{Credit}(i) + \\max_{(j, i) \\in E, j < i} L[j];$",
            "  \\}",
            "  \\text{return} $\\max_{(j, i) \\in E, i \\leq j \\leq n} L[j];$",
            "\\}",
        ]

        code_objs = [None] * len(code)
        linenumber_objs = [None] * len(code)
        surround_objs = [None] * len(code)

        for i in range(len(code)):
            code_objs[i] = Tex(code[i]).scale(code_scale)
            code_objs[i].set_color_by_tex_to_color_map(map)

            linenumber_objs[i] = Tex(str(i + 1)).scale(code_scale * 0.7)

            if i == 0:
                linenumber_objs[i].shift(np.array([-4, 3, 0])).to_edge(LEFT)
                code_objs[i].shift(np.array([-4, 3, 0])).to_edge(LEFT).shift(
                    RIGHT * 0.5
                )
            else:
                linenumber_objs[i].align_to(linenumber_objs[i - 1], LEFT + DOWN).shift(
                    DOWN * buffer
                ).to_edge(LEFT)

                code_objs[i].align_to(code_objs[i - 1], LEFT + DOWN).shift(
                    DOWN * buffer
                ).shift(RIGHT * 0.5)

            surround_objs[i] = SurroundingRectangle(
                VGroup(linenumber_objs[i], linenumber_objs[i]),
                corner_radius=0.1,
                color=PINK,
            )

        self.play(
            *[Write(code_objs[i]) for i in range(len(code))],
            *[Create(linenumber_objs[i]) for i in range(len(code))],
            *[Create(surround_objs[i]) for i in range(len(code))]
        )
        self.wait(3)
        self.next_slide()
        q1 = (
            Text("What is the running time of the algorithm?", color=RED, font_size=30)
            .align_to(code_objs[8], LEFT + DOWN)
            .shift(DOWN)
        )
        self.play(Write(q1))
        self.wait(2)
        self.next_slide()

        ans1 = (
            Tex("$O(n^{2})$", color=YELLOW, font_size=45)
            .align_to(q1, LEFT + DOWN)
            .shift(DOWN * 0.5)
        )
        self.next_slide()
        self.play(Write(ans1))
