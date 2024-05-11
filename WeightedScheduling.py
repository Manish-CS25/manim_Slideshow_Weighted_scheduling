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


class intro(Slide):
    def construct(self):
        header = Text(
            "Dynamic Programming: Weighted Scheduling",
            font_size=45,
            stroke_width=2,
            color=GREEN,
        )
        self.play(Write(header))
        self.next_slide()
        self.play(FadeOut(header))

        l0 = NumberLine(
            x_range=[0, 48, 1],
            length=12,
            color=BLUE,
        )
        # Move the number line down

        self.play(Create(l0))

        startingx = [-6, -5.75, -4.25, -3.25, -0.8, -1, 1.75, 2]
        startingy = [
            2.5,
            1.5,
            2.5,
            1.5,
            2.5,
            1.5,
            2.5,
            1.5,
        ]
        wid = [
            1.25,
            2,
            2.25,
            1.10,
            1.15,
            2.25,
            2,
            2.5,
        ]
        weights = [
            2,
            4,
            3,
            5,
            4,
            2,
            1,
            2,
        ]

        rgroup = VGroup()
        for i in range(len(startingx)):
            rect = Rectangle(height=0.40, width=wid[i])
            rect.align_to(np.array([startingx[i], startingy[i], 0]), LEFT + UP)
            # Create a class number label for each rectangle
            class_number_label = Text(f"C {i+1}", font_size=15, color=BLUE)
            # Create a new weight label for each rectangle
            weight_label = Text(str(weights[i]), font_size=15)
            # Position the weight label at the center of the rectangle
            weight_label.move_to(rect.get_center())
            # Position the class number label above the rectangle
            class_number_label.next_to(rect, 0.5 * UP)
            rect_with_weight = VGroup(rect, weight_label)
            rect_with_labels = VGroup(rect, class_number_label)
            rgroup.add(rect_with_weight, class_number_label)

        self.play(Create(l0), *[Create(r) for r in rgroup], run_time=3)
        self.next_slide()
        text = Tex(
            "You are given $n$ classes $C_1,C_2, \dots, C_n$ such that each class $C_i$ has credit associated with it.You have just one room to schedule the classes. Design an algorithm to schedule non-overlapping classes in a single classroom that maximize the no. of credit.",
            font_size=50,
        )
        text.align_to(l0, 2 * UP)
        text.scale(0.6)
        self.play(Write(text), run_time=3)

        self.next_slide()
        text2 = (
            Tex("Greedy strategy: Pick the class that ends first", font_size=25)
            .align_to(text, LEFT + DOWN)
            .shift(DOWN)
        )
        self.play(Write(text2))
        self.next_slide()
        text3 = Tex("Greedy strategy: Does not work", font_size=25, color=RED).next_to(
            text2, DOWN
        )
        self.play(Write(text3))

        self.next_slide()
        self.wait(2)


class dag(Slide):
    def construct(self):
        # Define the number of circles
        num_circles = 8
        circle_radius = 0.3
        circle_distance = 1.2

        # Create circles
        circles = [Circle(radius=circle_radius, color=BLUE) for _ in range(num_circles)]

        # Set initial position for circles
        circles[0].next_to(LEFT * 8, RIGHT, buff=circle_distance)

        for i in range(1, num_circles):
            circles[i].next_to(circles[i - 1].get_right(), RIGHT, buff=circle_distance)

        # Add circles to the scene
        self.play(*[Create(circle) for circle in circles], run_time=2)
        self.wait(1)
        self.next_slide()
        # Create class number labels

        class_labels = [
            Text(f"C {i}", font_size=15, color=BLUE) for i in range(1, num_circles + 1)
        ]

        # Set labels in the center of each circle

        for i in range(num_circles):
            class_labels[i].move_to(circles[i].get_center())

        # Add labels to the scene
        self.play(*[Create(label) for label in class_labels], run_time=2)
        self.wait(1)
        self.next_slide()
        # Create curved arrows between circles
        arrow1 = [
            ArcBetweenPoints(
                circles[0].get_edge_center(RIGHT),
                circles[i].get_edge_center(LEFT),
                angle=-TAU / 3,
                tip_length=0.1,
                color=WHITE,
            ).add_tip(tip_length=0.2)
            for i in range(2, num_circles)
        ]
        self.play(*[Create(arrow) for arrow in arrow1])
        self.wait(3)
        # L(1) label
        weight = Tex("$L(1):{2}$", font_size=20, color=YELLOW)
        weight.next_to(circles[0], DOWN)
        self.play(Create(weight))

        q = (
            Tex("But Edge ($C_1$, $C_2$) does not exist", font_size=30, color=WHITE)
            .align_to(circles[0], LEFT + 2 * DOWN)
            .shift(DOWN)
        )
        self.play(Write(q))
        Wait(2)
        self.next_slide()

        idea = Tex(
            "A path from left to node $C_{k}$,: ($C_1$, $C_2$, ..., $C_k$) such that $\sum_{i=1}^{n} Credit(C_i)$ is the maximum",
            font_size=30,
            color=WHITE,
        )
        idea.align_to(q, LEFT + 1 * DOWN).shift(DOWN)
        self.play(Transform(q, idea))
        self.wait(5)
        self.next_slide()

        idea2 = (
            Tex(
                "L(i) $\leftarrow$ maximum credit you can receive by scheduling} non} overlapping classes in \ \{1,...i\}, the solution also contains i.",
                font_size=30,
                color=WHITE,
            )
            .align_to(q, LEFT + 1 * DOWN)
            .shift(DOWN)
        )

        s = Tex(
            "L(i) $\\leftarrow$ Credit(i) + $\\max_{(j, i) \\in E, j < i} L[j]$",
            font_size=35,
            color=YELLOW,
        ).next_to(idea2, DOWN)
        self.play(Transform(idea, idea2))

        self.play(Transform(idea2, s))
        self.wait(3)
        self.play(*[FadeOut(arrow) for arrow in arrow1])
        self.next_slide()

        # arrow 2
        arrow2 = [
            ArcBetweenPoints(
                circles[1].get_edge_center(RIGHT),
                circles[i].get_edge_center(LEFT),
                angle=-TAU / 3,
                tip_length=0.1,
                color=WHITE,
            ).add_tip(tip_length=0.2)
            for i in range(3, num_circles)
        ]

        # L(2) label
        weight = Tex("$L(2):{4}$", font_size=20, color=YELLOW)
        weight.next_to(circles[1], DOWN)
        self.play(Create(weight))
        # Add arrows to the scene
        self.play(*[Create(arrow) for arrow in arrow2])
        self.wait(5)
        self.play(*[FadeOut(arrow) for arrow in arrow2])

        # arrow13 = [
        #     ArcBetweenPoints(
        #         circles[0].get_edge_center(RIGHT),
        #         circles[2].get_edge_center(LEFT),
        #         angle=-TAU / 3,
        #         tip_length=0.1,
        #         color=WHITE,
        #     ).add_tip(tip_length=0.2)
        #     for i in range(4, num_circles)
        # ]

        arrow3 = [
            ArcBetweenPoints(
                circles[2].get_edge_center(RIGHT),
                circles[i].get_edge_center(LEFT),
                angle=-TAU / 3,
                tip_length=0.1,
                color=WHITE,
            ).add_tip(tip_length=0.2)
            for i in range(4, num_circles)
        ]

        # Add arrows to the scene
        # self.play(*[Create(arrow) for arrow in arrow1[1:]])
        self.play(Create(arrow1[0]))
        self.play(arrow1[0].animate.set_color(YELLOW))

        # L(2) label
        weight = Tex("$L(3):{5}$", font_size=20, color=YELLOW)
        weight.next_to(circles[2], DOWN)
        self.play(Write(weight))
        self.play(FadeOut(arrow1[0]))
        self.play(*[Create(arrow) for arrow in arrow3])
        self.wait(2)

        self.play(*[FadeOut(arrow) for arrow in arrow3])

        arrow4 = [
            ArcBetweenPoints(
                circles[3].get_edge_center(RIGHT),
                circles[i].get_edge_center(LEFT),
                angle=-TAU / 3,
                tip_length=0.1,
                color=WHITE,
            ).add_tip(tip_length=0.2)
            for i in range(4, num_circles)
        ]

        self.play(Create(arrow1[1]))
        self.play(Create(arrow2[0]))
        self.play(arrow2[0].animate.set_color(YELLOW))

        # L(2) label
        weight = Tex("$L(4):{9}$", font_size=20, color=YELLOW)
        weight.next_to(circles[3], DOWN)
        self.play(Write(weight))
        self.play(FadeOut(arrow1[1], arrow2[0]))
        # Add arrows to the scene
        # self.play(*[Create(arrow) for arrow in arrow1[1]])

        self.play(*[Create(arrow) for arrow in arrow4])
        self.wait(5)

        self.play(*[FadeOut(arrow) for arrow in arrow4])

        self.next_slide()

        arrow5 = [
            ArcBetweenPoints(
                circles[4].get_edge_center(RIGHT),
                circles[i].get_edge_center(LEFT),
                angle=-TAU / 3,
                tip_length=0.1,
                color=WHITE,
            ).add_tip(tip_length=0.2)
            for i in range(6, num_circles)
        ]

        # L(2) label
        self.play(Create(arrow1[2]))
        self.play(Create(arrow2[1]))
        self.play(Create(arrow3[0]))
        self.play(Create(arrow4[0]))
        self.play(arrow4[0].animate.set_color(YELLOW))
        weight = Tex("$L(5):{13}$", font_size=20, color=YELLOW)
        weight.next_to(circles[4], DOWN)
        self.play(Write(weight))
        self.play(FadeOut(arrow4[0], arrow3[0], arrow2[1], arrow1[2]))

        # Add arrows to the scene
        self.play(*[Create(arrow) for arrow in arrow5])
        self.wait(3)

        self.play(*[FadeOut(arrow) for arrow in arrow5])

        self.next_slide()

        arrow6 = [
            ArcBetweenPoints(
                circles[5].get_edge_center(RIGHT),
                circles[i].get_edge_center(LEFT),
                angle=-TAU / 3,
                tip_length=0.1,
                color=WHITE,
            ).add_tip(tip_length=0.2)
            for i in range(6, num_circles)
        ]
        self.play(Create(arrow1[3]))
        self.play(Create(arrow2[2]))
        self.play(Create(arrow3[1]))
        self.play(Create(arrow4[1]))
        self.play(arrow4[1].animate.set_color(YELLOW))

        weight = Tex("$L(6):{11}$", font_size=20, color=YELLOW)
        weight.next_to(circles[5], DOWN)
        self.play(Write(weight))
        self.play(FadeOut(arrow4[1], arrow3[1], arrow2[2], arrow1[3]))

        # Add arrows to the scene
        self.play(*[Create(arrow) for arrow in arrow6])
        self.wait(2)

        self.play(*[FadeOut(arrow) for arrow in arrow6])

        self.next_slide()

        self.play(Create(arrow1[4]))

        self.play(Create(arrow2[3]))
        self.play(Create(arrow3[2]))
        self.play(Create(arrow4[2]))
        self.play(Create(arrow5[0]))
        self.play(Create(arrow6[0]))
        self.play(arrow5[0].animate.set_color(YELLOW))

        weight = Tex("$L(7):{14}$", font_size=20, color=YELLOW)
        weight.next_to(circles[6], DOWN)
        self.play(Write(weight))
        self.play(
            FadeOut(arrow4[2], arrow3[2], arrow2[3], arrow1[4], arrow5[0], arrow6[0])
        )

        self.next_slide()
        self.play(Create(arrow1[5]))
        self.play(Create(arrow2[4]))
        self.play(Create(arrow3[3]))
        self.play(Create(arrow4[3]))
        self.play(Create(arrow5[1]))
        self.play(Create(arrow6[1]))
        self.play(arrow5[1].animate.set_color(YELLOW))
        self.play(
            FadeOut(arrow4[3], arrow3[3], arrow2[4], arrow1[5], arrow5[1], arrow6[1])
        )

        weight = Tex("$L(6):{15}$", font_size=20, color=YELLOW)
        weight.next_to(circles[7], DOWN)
        self.play(Write(weight))
        self.next_slide()


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
            *[Create(surround_objs[i]) for i in range(len(code))],
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
