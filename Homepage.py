from logging import exception
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import threading
import Tower_Of_Hanoi  # This file contains your turtle game

# ---------------- Tkinter ----------------
r = Tk()
r.title("Tower Of Hanoi")
r.geometry("1000x600")
r.configure(bg="#111827")

# Leaderboard
leaderboard = Frame(r, bg="#1F2937", borderwidth=5)
leaderboard.pack(side="right", fill="both", padx=30, pady=50)
Label(leaderboard, text="Leaderboard", font="Arial 25 bold", bg="silver").pack(fill=X, pady=10)

columns = ("Rank", "Name", "Score")
tree = ttk.Treeview(leaderboard, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")
tree.pack(fill="both", expand=True, pady=10)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#1F2937", foreground="#F9FAFB", rowheight=25, fieldbackground="#1F2937")
style.configure("Treeview.Heading", background="silver", foreground="black", font=("Arial", 12, "bold"))
style.map("Treeview", background=[("selected", "gold")], foreground=[("selected", "black")])

# Main Frame
window = Frame(r, bg="#273549", borderwidth=5)
window.pack(side="left", fill="both", expand=True, padx=30, pady=50)
Label(window, text="Welcome To Tower Of Hanoi Tactics!", font=("Arial 15 bold"), bg="silver").pack(pady=15, fill=X)

# Player type
player = StringVar()
player.set("new")
playertype = Frame(window, bg="#273549")
playertype.pack(pady=20)
Radiobutton(playertype, text="New Player", bg="#273549", fg="#F9FAFB", variable=player, value="new",
            indicatoron=0, width=15, selectcolor="#60A5FA", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=20, pady = 15)
Radiobutton(playertype, text="Existing Player", bg="#273549", fg="#F9FAFB", variable=player, value="exist",
            indicatoron=0, width=15, selectcolor="#60A5FA", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=20, pady = 15)

# Name Entry
name_frame = Frame(window, bg="#273549")
name_frame.pack(pady=20)
Label(name_frame, text="Enter Name:", bg="#273549", fg="#F9FAFB", font=("Arial", 13, "bold")).grid(row=0, column=0, padx=5)
entry = Entry(name_frame, width=30, font=("Arial", 14))
entry.grid(row=0, column=1, padx=5)

# ---------------- Functions ----------------
def update_leaderboard(highlight_name=None):

    try:
        # ---------------- Database ----------------
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Tanay@Rai1",
            database="TowerOfHanoi"
        )
        cursor = conn.cursor()

        for row in tree.get_children():
            tree.delete(row)

        cursor.execute("SELECT PlayerName, Score FROM leaderboard ORDER BY Score DESC")
        results = cursor.fetchall()

        for rank, (pname, score) in enumerate(results, start=1):
            tree.insert("", "end", values=(rank, pname, score))

        if highlight_name:
            for item in tree.get_children():
                if tree.item(item, "values")[1] == highlight_name:
                    tree.selection_set(item)
                    tree.see(item)
                    break

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error updating leaderboard: {e}")


def refresh_leaderboard():
    update_leaderboard()
    r.after(2000, refresh_leaderboard)

def start_game_func():
    """Handle Start Game button."""
    pname = entry.get().strip()
    if not pname:
        messagebox.showwarning("Input Error", "Please enter a name.")
        return

    # Create a new database connection for this function
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Tanay@Rai1",
        database="TowerOfHanoi"
    )
    cursor = conn.cursor()

    if player.get() == "new":
        cursor.execute("SELECT PlayerName FROM leaderboard WHERE PlayerName=%s", (pname,))
        if cursor.fetchone():
            messagebox.showinfo("Duplicate Entry", "Player already exists. Select existing player.")
        else:
            cursor.execute("INSERT INTO leaderboard (PlayerName, Score) VALUES (%s, %s)", (pname, 0))
            conn.commit()
            update_leaderboard(highlight_name=pname)
            messagebox.showinfo("Success", f"New player '{pname}' added. Select existing to play.")

    elif player.get() == "exist":
        cursor.execute("SELECT Score FROM leaderboard WHERE PlayerName=%s", (pname,))
        result = cursor.fetchone()
        if result:
            update_leaderboard(highlight_name=pname)
            entry.delete(0, END)
            score = result[0]

            def run_game_and_refresh():
                try:
                    Tower_Of_Hanoi.start_game(pname, score)
                    update_leaderboard(highlight_name=pname)
                except Exception as e:
                    import traceback
                    print("Error in game:", e)
                    traceback.print_exc()

            # Run safely in main thread
            r.after(200, run_game_and_refresh)
        else:
            messagebox.showerror("No Results", f"No player named '{pname}' found.")

    cursor.close()
    conn.close()

# Buttons
Button(window, text="Start Game", font=("Arial", 14, "bold"), bg="gold", fg="darkblue", command=start_game_func).pack(pady=15)
Button(window, text="Quit Game", font=("Arial", 14, "bold"), bg="gold", fg="darkblue", command=r.destroy).pack(pady=10)

# Initial leaderboard
update_leaderboard()
refresh_leaderboard()
r.mainloop()
