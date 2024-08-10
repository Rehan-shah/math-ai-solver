from manim import *

class S1S(Scene):
    def construct(self):
        vec_title = Tex("Vectors", font_size=40, color=YELLOW).to_edge(UP)
        self.play(Write(vec_title))

        def_title = Tex("Definition: A vector is a quantity with both magnitude (length) and direction.", 
                        font_size=25, color=GREEN).shift(UP)
        self.play(Write(def_title))
        self.wait(2)

        self.play(FadeOut(def_title))

        prop_title = Tex("Properties of Vectors:", font_size=30, color=YELLOW).shift(UP)
        self.play(Write(prop_title))

        prop1 = Tex(r"1. $\vec{A} + \vec{B} = \vec{B} + \vec{A}$", font_size=25, color=GREEN).shift(UP*0.5)
        self.play(Write(prop1))
        self.wait(2)

        self.play(FadeOut(prop1))

        prop2 = Tex(r"2. $(c \vec{A}) + \vec{A} = (c+1) \vec{A}$", font_size=25, color=GREEN).shift(UP*0.5)
        self.play(Write(prop2))
        self.wait(2)

        self.play(FadeOut(prop_title, prop2))

        op_title = Tex("Operations with Vectors:", font_size=30, color=YELLOW).shift(UP)
        self.play(Write(op_title))

        op1 = Tex(r"Addition: $\vec{A} + \vec{B} = (\vec{A}_x + \vec{B}_x, \vec{A}_y + \vec{B}_y)$", 
                  font_size=25, color=GREEN).shift(UP*0.5)
        self.play(Write(op1))
        self.wait(2)

        self.play(FadeOut(op1))

        op2 = Tex(r"Scalar Multiplication: $c \vec{A} = (c\vec{A}_x, c\vec{A}_y)$", 
                  font_size=25, color=GREEN).shift(UP*0.5)
        self.play(Write(op2))
        self.wait(2)

        self.play(FadeOut(op_title, op2))
