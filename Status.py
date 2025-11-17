from turtle import Turtle
from Disk import Disc

Align = "center"
Font2 = ("Arial", 15, "bold")

class Status:
    def __init__(self):
        self.num_disc = Disc.discs
        self.total_step = (2 ** self.num_disc) - 1
        self.remaining = self.total_step
        self.steps = Turtle()
        self.steps.color("cyan")
        self.steps.hideturtle()
        self.steps.penup()
        self.steps.goto(-430, 260)
        self.update_status()

        self.hint = Turtle()
        self.hint.color("cyan")
        self.hint.hideturtle()
        self.hint.penup()
        self.hint.goto(430, 260)
        self.hint.write("Hint: H", align= Align, font= Font2)

        self.replay = Turtle()
        self.replay.color("cyan")
        self.replay.hideturtle()
        self.replay.penup()
        self.replay.goto(430, 230)
        self.replay.write("Replay: R", align=Align, font=Font2)

        self.Quit = Turtle()
        self.Quit.color("cyan")
        self.Quit.hideturtle()
        self.Quit.penup()
        self.Quit.goto(430, 200)
        self.Quit.write("Quit: Q", align=Align, font=Font2)

    def update_status(self):
        self.steps.clear()
        self.steps.write(f"Steps: {self.remaining}", align= Align, font= Font2)

    def decrease(self):
        self.remaining -= 1
        self.update_status()