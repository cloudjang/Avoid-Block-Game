from tkinter import *
from tkinter import Tk, PhotoImage, Canvas, Label
from tkinter.simpledialog import askstring
import random
import time

window = Tk()

# Values
global colors, window_w, window_h, place_x, place_y, screen_w, screen_h, player_speed, score, boundary, Running, left_key, right_key
colors = ["red", "green", "blue", "yellow", "pink"]
window_w, window_h = (1280, 720)
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()
place_x = (screen_w - window_w) / 2
place_y = (screen_h - window_h) / 2
player_speed = 15
score = 0
boundary = 10
Running = False
left_key = "Left"
right_key = "Right"

# Making Bricks class
class OB:
    def __init__(self, canvas, color, size, x, y, xspeed, yspeed):
        self.canvas = canvas
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.ob = canvas.create_rectangle(x, y, x + size, y + size, fill=color)

    def Move(self):
        self.canvas.move(self.ob, self.xspeed, self.yspeed)
        (x1, y1, x2, y2) = self.canvas.coords(self.ob)
        (self.x, self.y) = (x1, y1)

    def Delete(self):
        self.canvas.delete(self.ob)

    def Get_position(self):
        return self.canvas.coords(self.ob)


# Key events system
def Press(event):
    global player, key_info, boss_img, player_speed
    # Player moves left
    if event.keysym == left_key:
        canvas.move(player, -player_speed, 0)
    # Player moves right
    if event.keysym == right_key:
        canvas.move(player, player_speed, 0)
    # Start key
    if event.keysym == "Return":
        key_info.destroy()
        player = canvas.create_image(window_w / 2, 600, image=main_resized, anchor="nw")
        Main_ob()
        main_game_loop()
    # Boss key
    if event.keysym == "b":
        Stop()
        boss_win = Toplevel(window, takefocus=True)
        boss_win.title("Program Loading...")
        boss_win.geometry(f"{screen_w}x{screen_h}")
        boss_lab = Label(boss_win, image=boss_img)
        boss_lab.pack()
    # Pause key
    if event.keysym == "BackSpace":
        Stop()
    # Resume key
    if event.keysym == "r":
        Resume()
    # Load cheat code
    if event.keysym == "c":
        Cheat()
    # Save key
    if event.keysym == "s":
        Stop()
        Save()
    # Load key
    if event.keysym == "l":
        Load()
    # Customise key
    if event.keysym == "k":
        Customise()


# Stop game system
def Stop():
    global Running, player_speed
    Running = False
    player_speed = 0


# Resume game system
def Resume():
    global Running, player_speed
    Running = True
    player_speed = 15
    main_game_loop()


# Cheat system
def Cheat():
    global cheat_code, player_speed, score, boundary
    cheat_code = askstring(
        "Cheat Code",
        (
            "ps2: double player speed" + "\n"
            "s2: double score" + "\n"
            "b-2: shrink collision area of player" + "\n"
        ),
    )
    if cheat_code == "ps2":
        player_speed += player_speed
    elif cheat_code == "s2":
        score += score
    elif cheat_code == "b-2":
        boundary = 0


# Save system: save coordinate of player, boundary, score and the bricks info like color, coordinates, size and speed.
def Save():
    with open("Savefile.txt", "w") as save_file:
        save_file.write(
            str([rand_color1, rand_size1, b1_box[0], b1_box[1], rand_speed1]) + "\n"
        )
        save_file.write(
            str([rand_color2, rand_size2, b2_box[0], b2_box[1], rand_speed2]) + "\n"
        )
        save_file.write(
            str([rand_color3, rand_size3, b3_box[0], b3_box[1], rand_speed3]) + "\n"
        )
        save_file.write(
            str([rand_color4, rand_size4, b4_box[0], b4_box[1], rand_speed4]) + "\n"
        )
        save_file.write(str(player_box[0]) + "\n")
        save_file.write(str(boundary) + "\n")
        save_file.write(str(score) + "\n")


# Load system: load all information saved and put all objects on the canvas according to the information.
def Load():
    global player, score, boundary, b1, b2, b3, b4
    key_info.destroy()
    load_file = open("Savefile.txt", "r")
    load_file_contents = load_file.readlines()
    contents = []
    for content in load_file_contents:
        contents.append(content.strip())
    load_player_x = int(float(contents[4]))
    player = canvas.create_image(load_player_x, 600, image=main_resized, anchor="nw")
    list_1 = contents[0].strip('[]"').split(",")
    list_2 = contents[1].strip('[]"').split(",")
    list_3 = contents[2].strip('[]"').split(",")
    list_4 = contents[3].strip('[]"').split(",")
    b1 = OB(
        canvas,
        str(list_1[0].strip("'")),
        int(list_1[1].strip(" ")),
        int(float(list_1[2].strip(" "))),
        int(float(list_1[3].strip(" "))),
        0,
        int(list_1[4].strip(" ")),
    )
    b2 = OB(
        canvas,
        str(list_2[0].strip("'")),
        int(list_2[1].strip(" ")),
        int(float(list_2[2].strip(" "))),
        int(float(list_2[3].strip(" "))),
        0,
        int(list_2[4].strip(" ")),
    )
    b3 = OB(
        canvas,
        str(list_3[0].strip("'")),
        int(list_3[1].strip(" ")),
        int(float(list_3[2].strip(" "))),
        int(float(list_3[3].strip(" "))),
        0,
        int(list_3[4].strip(" ")),
    )
    b4 = OB(
        canvas,
        str(list_4[0].strip("'")),
        int(list_4[1].strip(" ")),
        int(float(list_4[2].strip(" "))),
        int(float(list_4[3].strip(" "))),
        0,
        int(list_4[4].strip(" ")),
    )
    boundary = int(contents[-2])
    score = int(contents[-1])


# Leader board system: when this game is over, program will ask user's name and show leader board.
def Leader_board():
    name = askstring("Name", "Enter your name here.")
    with open("Leaderboard.txt", "a+") as lead_board:
        lead_board.write(str([name, score]) + "\n")
    read_board = open("Leaderboard.txt", "r")
    read_content = read_board.read()
    rank = Label(
        canvas,
        text="This is leader board\n" + str(read_content),
        font=("Arial", 20),
        fg="#FFFFFF",
        bg="#000000",
        justify="left",
    )
    b1.Delete()
    b2.Delete()
    b3.Delete()
    b4.Delete()
    rank.place(x=window_w / 3, y=window_h / 3)


# Score board system
def Score_board():
    global s_board
    s_board = Label(
        canvas,
        text="Score: %s" % (score),
        font=("Arial", 15),
        fg="#FFFFFF",
        bg="#000000",
        justify="center",
    )
    s_board.place(x=0, y=0)


# Customise key system: it can make user customise keys that player moves.
def Customise():
    global left_key, right_key
    left_key = askstring(
        "Left",
        (
            "Set up key moving left, except r, b, c, s, l and k" + "\n"
            "If you want to go back to Left key, enter 1"
        ),
    )
    if left_key == "1":
        left_key = "Left"
    right_key = askstring(
        "Right",
        (
            "Set up key moving right, except r, b, c, s, l and k" + "\n"
            "If you want to go back to Right key, enter 1"
        ),
    )
    if right_key == "1":
        right_key = "Right"


# Main initial bricks: Initially program make bricks with random color, size, coordinate and speed.
def Main_ob():
    global b1, b2, b3, b4, rand_color1, rand_color2, rand_color3, rand_color4
    global rand_size1, rand_size2, rand_size3, rand_size4, rand_speed1, rand_speed2, rand_speed3, rand_speed4

    rand_color1 = random.choice(colors)
    rand_size1 = random.randint(100, 200)
    rand_x1 = random.randint(0, 1080)
    rand_speed1 = random.randint(10, 20)
    b1 = OB(canvas, rand_color1, rand_size1, rand_x1, 0, 0, rand_speed1)

    rand_color2 = random.choice(colors)
    rand_size2 = random.randint(100, 200)
    rand_x2 = random.randint(0, 1080)
    rand_speed2 = random.randint(10, 20)
    b2 = OB(canvas, rand_color2, rand_size2, rand_x2, 0, 0, rand_speed2)

    rand_color3 = random.choice(colors)
    rand_size3 = random.randint(100, 200)
    rand_x3 = random.randint(0, 1080)
    rand_speed3 = random.randint(10, 20)
    b3 = OB(canvas, rand_color3, rand_size3, rand_x3, 0, 0, rand_speed3)

    rand_color4 = random.choice(colors)
    rand_size4 = random.randint(100, 200)
    rand_x4 = random.randint(0, 1080)
    rand_speed4 = random.randint(10, 20)
    b4 = OB(canvas, rand_color4, rand_size4, rand_x4, 0, 0, rand_speed4)


# Main game loop
# Program make the bricks move, getting their coordinates
# Because player is image, program needs to check collision in different way
# Check if the bricks is lower than player and check collision between sides of player and sides of bricks
# If not, user will get 10 points
# If the bricks reach at the ground, they are deleted and re-made randomly
def main_game_loop():
    global score, Running, colors, b1, b2, b3, b4, boundary, b1_box, b2_box, b3_box, b4_box, player_box
    global rand_size1, rand_size2, rand_size3, rand_size4, rand_speed1, rand_speed2, rand_speed3, rand_speed4
    global rand_color1, rand_color2, rand_color3, rand_color4
    Running = True
    Score_board()
    while Running:
        player_box = canvas.coords(player)
        b1_box = b1.Get_position()
        b2_box = b2.Get_position()
        b3_box = b3.Get_position()
        b4_box = b4.Get_position()
        b1.Move()
        b2.Move()
        b3.Move()
        b4.Move()
        window.update()
        time.sleep(0.03)
        if (player_box[1] - boundary) <= b1_box[3]:
            if (
                b1_box[0] < (player_box[0] - boundary) < b1_box[2]
                or b1_box[0] < (player_box[0] + boundary) < b1_box[2]
            ):
                Stop()
                Leader_board()
            elif (b1.y + b1.size) >= window_h:
                score += 10
                Score_board()
                b1.Delete()
                rand_color1 = random.choice(colors)
                rand_size1 = random.randint(100, 200)
                rand_x1 = random.randint(0, 1080)
                rand_speed1 = random.randint(10, 20)
                b1 = OB(canvas, rand_color1, rand_size1, rand_x1, 0, 0, rand_speed1)
        if (player_box[1] - boundary) <= b2_box[3]:
            if (
                b2_box[0] < (player_box[0] - boundary) < b2_box[2]
                or b2_box[0] < (player_box[0] + boundary) < b2_box[2]
            ):
                Stop()
                Leader_board()
            elif (b2.y + b2.size) >= window_h:
                score += 10
                Score_board()
                b2.Delete()
                rand_color2 = random.choice(colors)
                rand_size2 = random.randint(100, 200)
                rand_x2 = random.randint(0, 1080)
                rand_speed2 = random.randint(10, 20)
                b2 = OB(canvas, rand_color2, rand_size2, rand_x2, 0, 0, rand_speed2)
        if (player_box[1] - boundary) <= b3_box[3]:
            if (
                b3_box[0] < (player_box[0] - boundary) < b3_box[2]
                or b3_box[0] < (player_box[0] + boundary) < b3_box[2]
            ):
                Stop()
                Leader_board()
            elif (b3.y + b3.size) >= window_h:
                score += 10
                Score_board()
                b3.Delete()
                rand_color3 = random.choice(colors)
                rand_size3 = random.randint(100, 200)
                rand_x3 = random.randint(0, 1080)
                rand_speed3 = random.randint(10, 20)
                b3 = OB(canvas, rand_color3, rand_size3, rand_x3, 0, 0, rand_speed3)
        if (player_box[1] - boundary) <= b4_box[3]:
            if (
                b4_box[0] < (player_box[0] - boundary) < b4_box[2]
                or b4_box[0] < (player_box[0] + boundary) < b4_box[2]
            ):
                Stop()
                Leader_board()
            elif (b4.y + b4.size) >= window_h:
                score += 10
                Score_board()
                b4.Delete()
                rand_color4 = random.choice(colors)
                rand_size4 = random.randint(100, 200)
                rand_x4 = random.randint(0, 1080)
                rand_speed4 = random.randint(10, 20)
                b4 = OB(canvas, rand_color4, rand_size4, rand_x4, 0, 0, rand_speed4)


# Window info: place window at middle of screen
window.title("Avoid Bricks")
window.geometry("%dx%d+%d+%d" % (window_w, window_h, place_x, place_y))
window.resizable(0, 0)

# Canvas info
canvas = Canvas(
    window, highlightthickness=0, width=window_w, height=window_h, bg="black"
)
# bosskey image
boss_img = PhotoImage(file="boss_img.png")

# Main character image
global main_img, main_resized
main_img = PhotoImage(file="./main_character.png")
main_resized = main_img.subsample(8)

# Key info label
global key_info
key_info = Label(
    canvas,
    text="<RETURN> to start\n<BackSpace> to pause\n<R> to resume\n<B> for Boss key\n<S> to save\n<L> to load\n<K> to customise key",
    font=("Arial, 25"),
    fg="#FFFFFF",
    bg="#000000",
    justify="left",
)
key_info.place(x=window_w / 3, y=window_h / 3)

# Connect keys to the function, Press
window.bind("<KeyPress>", Press)

canvas.pack()
window.mainloop()
