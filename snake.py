#! /bin/env python3
"""Snakes 1.0"""

import tkinter as tk
import random
from tkinter import messagebox

HEAD_COLOR = "#39FF14"
FACING = "e"
SNAKE = []
# ROOT window
ROOT = tk.Tk()
SCORE = tk.IntVar(ROOT, value=0)

# 100 = Pussy
# 60  = Normal
# 30  = Medium
# 0   = Hard
SPEED = 30  # in ms


def snakes():
    """A Snake game"""

    # main frame wxd
    main_width = 720
    main_height = 480

    # main frame
    main = tk.Frame(ROOT, bg="black")
    main.configure(width=main_width, height=main_height)
    main.focus_set()
    main.pack(fill=tk.BOTH, expand=True)

    # Score
    score = tk.Label(main, textvariable=SCORE, bg="black", fg="white")
    score.place(x=0, y=0)

    # sanke head wxh
    head_size = 15
    # Head
    SNAKE.append(tk.Frame(main, bg=HEAD_COLOR))
    SNAKE[0].configure(width=head_size, height=head_size, bd=0)
    SNAKE[0].place(x=0, y=0)

    # Food
    food = tk.Frame(main, bg="red")
    food.configure(width=head_size, height=head_size, bd=0)
    food.place(
        x=random.randrange(0, main_width, head_size),
        y=random.randrange(0, main_height, head_size)
    )

    def spawn():
        food.place(
            x=random.randrange(0, main_width, head_size),
            y=random.randrange(0, main_height, head_size)
        )

    def update_cord_x(cord, dx):
        cord = cord + dx
        if cord < 0:
            cord = main_width
        elif cord > main_width:
            cord = 0
        return cord

    def update_cord_y(cord, dy):
        cord = cord + dy
        if cord < 0:
            cord = main_height
        elif cord > main_height:
            cord = 0
        return cord

    def change_direction(cord_x, cord_y):
        if FACING == "e":
            return update_cord_x(cord_x, -head_size), cord_y
        if FACING == "w":
            return update_cord_x(cord_x, head_size), cord_y
        if FACING == "n":
            return cord_x, update_cord_y(cord_y, -head_size)
        if FACING == "s":
            return cord_x, update_cord_y(cord_y, head_size)

    def update_location():
        SNAKE[0].update()
        prev_x = SNAKE[0].winfo_x()
        prev_y = SNAKE[0].winfo_y()
        curr_x, curr_y = change_direction(prev_x, prev_y)
        for body in SNAKE:
            body.update()
            prev_x = body.winfo_x()
            prev_y = body.winfo_y()
            body.place(x=curr_x, y=curr_y)
            curr_x = prev_x
            curr_y = prev_y

    def update_score():
        SCORE.set(SCORE.get()+10)

    def check_overlap(head, obj):
        head.update()
        obj.update()
        if (head.winfo_x(), head.winfo_y()) == (obj.winfo_x(), obj.winfo_y()):
            return True
        return False

    def kill():
        for body in SNAKE[1:]:
            if check_overlap(SNAKE[0], body):
                return True
        return False

    def increase_tail():
        tail = SNAKE[-1]
        tail.update()
        cord_x = tail.winfo_x()
        cord_y = tail.winfo_y()
        SNAKE.append(tk.Frame(main, bg=HEAD_COLOR))
        tail = SNAKE[-1]
        tail.configure(width=head_size, height=head_size, bd=0)
        if FACING == "e":
            tail.place(x=update_cord_x(cord_x, head_size), y=cord_y)
        elif FACING == "w":
            tail.place(x=update_cord_x(cord_x, -head_size), y=cord_y)
        elif FACING == "n":
            tail.place(x=cord_x, y=update_cord_y(cord_y, head_size))
        elif FACING == "s":
            tail.place(x=cord_x, y=update_cord_y(cord_y, -head_size))

    def loop():
        update_location()
        if kill():
            ROOT.quit()
            messagebox.showwarning("You Suck", "GAME OVER!!!")
        if check_overlap(SNAKE[0], food):
            update_score()
            spawn()
            increase_tail()
        ROOT.after(SPEED, loop)

    def move(event):
        global FACING
        move_map = {
            "Left": "e", "a": "e",
            "Right": "w", "d": "w",
            "Up": "n", "w": "n",
            "Down": "s", "s": "s",
        }
        key = event.keysym
        direction = move_map.get(key)
        if direction:
            if FACING in ("e", "w") and key in ("Up", "Down", "w", "s"):
                FACING = direction
            elif FACING in ("n", "s") and key in ("Left", "a", "Right", "d"):
                FACING = direction

    main.bind("<KeyPress>", move)
    loop()
    ROOT.mainloop()


if __name__ == "__main__":
    print("Starting game ...")
    snakes()
    print("Game Over")
