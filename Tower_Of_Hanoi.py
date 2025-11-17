from turtle import Screen, Turtle
from Disk import Disc
from Rods import Rod
from Autoplay import Autoplay
from Status import Status
import mysql.connector
import turtle

def start_game(player_name, score):
    # ✅ Clean up any previous turtle window before creating a new one
    try:
        turtle.bye()
    except:
        pass
    turtle.TurtleScreen._RUNNING = True  # Reset internal flag so new Screen() works


    # --- Screen Setup ---
    s = Screen()
    s.setup(1000, 600)
    s.bgcolor("Black")
    s.colormode(1)
    s.tracer(0)

    # --- Rod and Disc Creation ---
    R = Rod()
    R.create()
    R.label()

    disc = Disc(R, s, score)
    disc.create_disc()
    status = Status()

    # --- Disc & Rod Settings ---
    disc_height = 20
    rod_positions = {"src": -350, "hlp": 0, "dest": 350}
    rods = {"src": [], "hlp": [], "dest": []}

    num_disc = disc.discs
    disc_list = disc.disc_list
    level = num_disc - 1

    # Place initial discs
    for i, d in enumerate(disc_list):
        rods["src"].append(d)
        d.og_color = d.fillcolor()
        d.goto(rod_positions["src"], -185 + i * disc_height)
        d.showturtle()
    s.update()

    autoplay = Autoplay(len(disc_list), s, rods, rod_positions, status)
    t = Turtle()
    t.penup()
    t.hideturtle()
    t.goto(0, 230)

    # --- Replay Game ---
    def replay_game():
        for rod_stack in rods.values():
            rod_stack.clear()

        for i, d in enumerate(disc_list):
            rods["src"].append(d)
            d.goto(rod_positions["src"], -185 + i * disc_height)
            d.fillcolor(d.og_color)

        t.clear()
        t.color("yellow")
        t.write(f"Level: {level}", align="center", font=("Arial", 15, "bold"))
        status.remaining = status.total_step
        s.update()

    def reset_game():
        for rod_stack in rods.values():
            rod_stack.clear()

        for i, d in enumerate(disc_list):
            rods["src"].append(d)
            d.goto(rod_positions["src"], -185 + i * disc_height)
            d.fillcolor(d.og_color)

        t.clear()
        t.color("red")
        t.write("You Lose: Solution", align="center", font=("Arial", 15, "bold"))
        status.remaining = status.total_step
        autoplay.move(len(disc_list), rods["src"], rods["hlp"], rods["dest"])
        s.update()

    def hint():
        reset_game()

    def quit_game():
        s.bye()  # ✅ correctly closes the turtle window
        turtle.TurtleScreen._RUNNING = True  # ✅ allow a new one later

    # --- Database Update ---
    def update_score_in_db(pname):
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Tanay@Rai1",
                database="TowerOfHanoi"
            )
            cursor = conn.cursor()
            cursor.execute("UPDATE leaderboard SET Score = Score + 1 WHERE PlayerName = %s", (pname,))
            conn.commit()
            cursor.execute("SELECT Score FROM Leaderboard where PlayerName = %s", (pname,))
            new_score = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            print(f"✅ Score updated for {pname}")
            return new_score

        except Exception as e:
            print(f"❌ Error updating score: {e}")
            return 0

    # --- Next Level ---
    def next_level(current_score):
        nonlocal level, num_disc, disc, disc_list, rods, autoplay

        level += 1
        num_disc += 1

        # Hide old discs
        for d1 in disc_list:
            d1.hideturtle()

        # Clear rods without replacing the dict
        for rod_stack in rods.values():
            rod_stack.clear()

        # Recreate discs
        disc = Disc(R, s, current_score)
        disc.discs = num_disc
        disc.create_disc()
        disc_list = disc.disc_list

        # Place discs on source rod
        for i, d in enumerate(disc_list):
            rods["src"].append(d)
            x = rod_positions["src"]
            y = -185 + i * disc_height
            d.goto(x, y)
            d.og_color = d.fillcolor()
            d.showturtle()

        # Update status
        status.num_disc = num_disc
        status.total_step = (2 ** num_disc) - 1
        status.remaining = status.total_step

        # --- Autoplay ---
        autoplay = Autoplay(len(disc_list), s, rods, rod_positions, status)

        # Show level text
        t.clear()
        t.color("yellow")
        t.write(f"Level: {level}", align="center", font=("Arial", 15, "bold"))

        s.update()
        s.listen()
        s.onkey(key="h", fun=hint)
        s.onkey(key="r", fun=replay_game)
        s.onkey(key="q", fun=quit_game)

    def get_disk_size(disk):
        return disk.shapesize()[1]

    selected_rod = None

    def handle_click(x, y):
        nonlocal selected_rod

        clicked_rod = None
        for rod, xpos in rod_positions.items():
            if xpos - 80 < x < xpos + 80:
                clicked_rod = rod
                break
        if not clicked_rod:
            return
        if selected_rod is None:
            if rods[clicked_rod]:
                selected_rod = clicked_rod
            return
        if selected_rod != clicked_rod and rods[selected_rod]:
            src = rods[selected_rod]
            dest = rods[clicked_rod]
            if (not dest) or (get_disk_size(src[-1]) <= get_disk_size(dest[-1])):
                disc_to_move = src.pop()
                rod_x = rod_positions[clicked_rod]
                rod_y = -185 + len(dest) * disc_height
                autoplay.move_turtle(disc_to_move, rod_x, rod_y)
                dest.append(disc_to_move)
                status.decrease()

                if status.remaining <= 0:
                    if len(rods["dest"]) == len(disc_list):
                        t.clear()
                        t.color("yellow")
                        t.write("🎉 You Win! Level Cleared!", align="center", font=("Arial", 15, "bold"))
                        scr = update_score_in_db(player_name)
                        s.ontimer(lambda: next_level(scr), 2000)

                    else:
                        reset_game()
        selected_rod = None


    # --- Bind keys and clicks ---
    s.listen()
    s.onkey(key="h", fun=hint)
    s.onkey(key="r", fun=replay_game)
    s.onkey(key="q", fun=quit_game)
    s.onscreenclick(handle_click)
    s.update()
    s.mainloop()

# start_game("bhardwaj", 1)