from manim import *
import numpy as np

class Util:
    def createWordThenFade(manim,text):
        t = Text(text,font_size=40,stroke_width=2)
        manim.play(Write(t), rum_time = 2)
        manim.wait(2)
        manim.play(FadeOut(t))
    
    def createSentence(manim,text,obj,where,time):
        t = Text(text,font_size=30,stroke_width=2).next_to(obj,where)
        manim.play(Write(t),run_time=time)
        return t

    def moveViaArrayAnimation(manim,obj,arr,time):
        manim.play(obj.animate.move_to(np.array(arr)),run_time=time)

    def cleanUp(manim):
        manim.play(
            *[FadeOut(mob)for mob in manim.mobjects]
            # All mobjects in the screen are saved in self.mobjects
        )
    
    def stop(manim):
        reddot= Dot(np.array([6.8,3.8,0]),color=RED)
        manim.play(FadeIn(reddot))
        manim.wait()
        manim.play(FadeOut(reddot))
        manim.pause()

    def pause(manim):
        manim.pause()