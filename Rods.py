from turtle import Turtle

Align = "center"
Font = ("Arial", 10, "bold")

class Rod:
    def __init__(self):
        self.rod = [] # list that will store the rods
        self.x_cord = [-350, 0, 350] # x coordinates of the rods
        self.y_cord = -200 # y coordinates of the rods

    # create Rods
    def create(self):
        # create rods for all coordinates in the x_cord list
        for i, x in enumerate(self.x_cord):
            t = Turtle("square")
            t.color("white")
            t.shapesize(stretch_len= 0.5, stretch_wid= 15)
            t.penup()
            t.goto(x, self.y_cord + 150)
            self.rod.append(t)

        baseline = Turtle("square")
        baseline.color("white")
        baseline.hideturtle()
        baseline.pensize(10)
        baseline.penup()
        baseline.goto(-450, -200)
        baseline.pendown()
        baseline.goto(450, -200)

    def label(self):
        label = Turtle()
        label.hideturtle()
        label.penup()
        label.color("white")
        label.goto(self.x_cord[0], self.y_cord - 30)
        label.write("Source", align=Align, font=Font)
        label.goto(self.x_cord[1], self.y_cord - 30)
        label.write("Helper", align=Align, font=Font)
        label.goto(self.x_cord[2], self.y_cord - 30)
        label.write("Destination", align=Align, font=Font)
