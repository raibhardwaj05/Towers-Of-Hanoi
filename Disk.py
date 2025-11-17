import random
from turtle import Turtle

class Disc:
    # makes the "discs" as Attribute of the class Disc
    discs = 0

    # create Disc object with the rod and main screen parameters
    def __init__(self, rod, screen, num_disc):
        self.s = screen
        self.R = rod
        # get the number of disc to solve
        # self.level = self.s.textinput("Tower of Hanoi", "Enter Level")
        Disc.discs = num_disc + 1
        self.disc_height = 20
        self.disc_list = [] # List of discs

    # To Give Random Colors to the discs
    def random_color(self):
        r = random.uniform(0.4, 0.9)
        g = random.uniform(0.4, 0.9)
        b = random.uniform(0.4, 0.9)
        return r, g, b

    # Create Disc
    def create_disc(self):
        # Create the largest disk first and decrease the number of disc to be created one by one
        for i in range(Disc.discs, 0, -1):
            t = Turtle("square")
            t.color(self.random_color())
            t.shapesize(stretch_len= i*1.5, stretch_wid= 1)
            t.penup()
            # location of the disc
            t.goto(self.R.rod[0].xcor(), self.R.y_cord + 15 + (self.discs - i) * self.disc_height)
            self.disc_list.append(t)
