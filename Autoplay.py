import time

disc_height = 20

class Autoplay:
    def __init__(self, num_disc, screen, rods, rod_position, status):
        self.num_disc = num_disc
        self.s = screen
        self.rod_list = rods
        self.rod_position = rod_position
        self.status = status

    # move the discs to the target x and y coordinates
    def move_turtle(self, discs, x_target, y_target):
        # get the current coordinates of the discs
        current_x, current_y = discs.position()

        # disc moves 20 steps at a time
        steps = 20
        # disc has to travel across the rod to come oout of it
        move_up = 150
        travel_y = (move_up - current_y) / steps
        for i in range(20):
            current_y += travel_y
            discs.goto(current_x, current_y)
            self.s.update()
            time.sleep(0.05)

        # Travel to Target x coordinate
        travel_x = (x_target - current_x) / steps
        for i in range(20):
            current_x += travel_x
            discs.goto(current_x, current_y)
            self.s.update()
            time.sleep(0.05)

        # disc align itself to the lowest space of the destination rod
        travel_y = (y_target - current_y) / steps
        for i in range(20):
            current_y += travel_y
            discs.goto(current_x, current_y)
            self.s.update()
            time.sleep(0.05)

    # main logic that recurse the movement and all the disc reach the destination from source
    def move(self, num_discs, source, helper, destination):
        # base case
        if num_discs == 0:
            return

        # recursive call
        self.move(num_discs - 1, source, destination, helper)

        # pop the topmost disc
        discs = source.pop()

        # sets the x coordinate of the destination
        if destination is self.rod_list["src"]:
            rod_x_coord = self.rod_position["src"]
        elif destination is self.rod_list["hlp"]:
            rod_x_coord = self.rod_position["hlp"]
        else:
            rod_x_coord = self.rod_position["dest"]

        # sets y coordinate ==>> -185 is the bottom most position of the rod
        rod_y_coord = -185 + len(destination) * disc_height

        # moves the disc
        self.move_turtle(discs, rod_x_coord, rod_y_coord)
        destination.append(discs)

        # update steps
        self.status.decrease()
        self.s.update()

        # recursive call
        self.move(num_discs - 1, helper, source, destination)
