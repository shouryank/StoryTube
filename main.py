import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from coref_resolution import coref
from utils import char_action_set_getter
from clausIE import refactor_sv, sv, weather_extraction

from animation import animate

def pipeline():
    #extracting the story from the gui
    # Default story:
    """
        A cat is walking on a snowy day. It jumped over a stone. It died. Dog is walking in the opposite direction. It ran. The dog said "Hello world, the cat is going to die hahaha".
        A detective was running on a sunnny day. He saw a ninja boy. The ninja boy was attacking. The detective said "You are caught for attacking". The ninja boy said "Catch me if you can".
    """
    text = txt1.get(1.0, "end-1c")

    # Coref resolution
    corefed_text = coref.resolve_coref(text)

    # Weather extraction
    weather = weather_extraction.get_weather(text)

    # Get svs
    svs = sv.extract_sv(text, corefed_text)

    # Assign char to action
    svs, characters = refactor_sv.refactor_sv(svs)

    animate.animate(characters, svs, weather)


def clicked_help():
    help_window = Toplevel()
    help_window.title("Help")
    lbl1 = Label(help_window, text="Here is your help !!")
    lbl1.grid(column=0, row=0)
    lbl2 = Label(help_window, text="Here are some points to note when making your story!\n")
    lbl2.grid(column=0, row=1)
    
    lbl3 = Label(help_window, text="The available characters and their actions are as follows:\n\n" + char_action_set_getter.print_char_action_set())# Adventure Girl : Dead, Idle, Jump, Melee, Run, Say, Shoot, Slide\n Boy : Dead, Hurt, Idle, Jump, Run, Say, Slide\n Cat : Die, Fall, Hurt, Idle, Jump, Run, Say, Slide, Walk\n Detective : Dead, Idle, Jump, Run, Say, Slide\n Dino : Dead, Idle, Jump, Run, Say, Walk\n Dog : Die, Fall, Hurt, Idle, Jump, Run, Say, Slide, Walk\n Girl : Dead, Idle, Jump, Run, Say, Walk\n Jack-o-lantern : Dead, Idle, Jump, Run, Say, Slide, Walk\n Kid : Dead, Idle, Jump, Run, Say, Walk\n Knight : Attack, Dead, Idle, Jump, Jumpattack, Run, Say, Walk\n Ninja Boy : Attack, Climb, Dead, Glide, Idle, Jump, Run, Say, Slide, Throw\n Ninja Girl : Attack, Climb, Dead, Glide, Idle, Jump, Run, Say, Slide, Throw\n Robot : Dead, Idle, Jump, Jumpmelee, Jumpshoot, Melee, Run, Runshoot, Say, Shoot, Slide\n Santa : Dead, Idle, Jump, Run, Say, Slide, Walk\n Zombie female : Attack, Dead, Idle, Say, Walk\n Zombie male : Attack, Dead, Idle, Say, Walk\n")
    


    lbl3.grid(column=0, row=2)
    btn_exit = Button(help_window, text="Exit", fg="red", command=help_window.destroy)
    btn_exit.grid(column=0, row=4)
    lbl4 = Label(help_window, text="\n\n")
    lbl4.grid(column=0, row=5)
    help_window.mainloop()

# CHAR ACTION SET:  {'adventure girl': ['dead', 'idle', 'jump', 'melee', 'run', 'say', 'shoot', 'slide'], 'boy': ['dead', 'hurt', 'idle', 'jump', 'run', 'say', 'slide'], 'cat': ['die', 'fall', 'hurt', 'idle', 'jump', 'run', 'say', 'slide', 'walk'], 'detective': ['dead', 'idle', 'jump', 'run', 'say', 'slide'], 'dino': ['dead', 'idle', 'jump', 'run', 'say', 'walk'], 'dog': ['die', 'fall', 'hurt', 'idle', 'jump', 'run', 'say', 'slide', 'walk'], 'girl': ['dead', 'Idle', 'Jump', 'Run', 'say', 'Walk'], 'jack-o-latern': ['dead', 'idle', 'jump', 'run', 'say', 'slide', 'walk'], 'kid': ['dead', 'idle', 'jump', 'run', 'say', 'walk'], 'knight': ['attack', 'dead', 'idle', 'jump', 'jumpattack', 'run', 'say', 'walk'], 'ninja boy': ['attack', 'climb', 'dead', 'glide', 'idle', 'jump', 'run', 'say', 'slide', 'throw'], 'ninja girl': ['attack', 'climb', 'dead', 'glide', 'idle', 'jump', 'run', 'say', 'slide', 'throw'], 'robot': ['dead', 'idle', 'jump', 'jumpmelee', 'jumpshoot', 'melee', 'run', 'runshoot', 'say', 'shoot', 'slide'], 'santa': ['dead', 'idle', 'jump', 'run', 'say', 'slide', 'walk'], 'zombie female': ['attack', 'dead', 'idle', 'say', 'walk'], 'zombie male': ['attack', 'dead', 'idle', 'say', 'walk']}


root = tk.Tk()
root.title("StoryTube")

bg = ImageTk.PhotoImage(Image.open('assets\\background.png'))
label = Label( root, image = bg)
label.place(x = 0,y = 0)

lbl1 = Label(root, bg = "#eae9d2", text="Welcome to StoryTube !!\n\n").grid(column=0, row=0)
lbl2 = Label(root, bg = "#eae9d2", text="Write down your amazing story below using the available characters :) \n\n").grid(column=0, row=2)

txt1 = Text(root, height = 10, width = 80, bg = "light yellow")
txt1.grid(column=0, row=3)

print(txt1.get(1.0, "end-1c"))

lbl3 = Label(root, bg = "#eae9d2", text="\n").grid(column=0, row=4)
btn1 = Button(root, bg = "#eae9d2", text="Submit story",fg="red", command=pipeline).grid(column=0, row=6)
lbl4 = Label(root, bg = "#eae9d2", text="\n").grid(column=0, row=7)

click_btn = PhotoImage(file='assets\help_icon.png')
img_label = Label(image=click_btn)
btn2 = Button(root, bg = "#eae9d2", image=click_btn,command= clicked_help, borderwidth=0).grid(column=0, row=8)

lbl5 = Label(root, bg = "#eae9d2", text="\n\n").grid(column=0, row=9)

# separator = ttk.Separator(root, orient='vertical')
# separator.place(relx=0.5, rely=0, relwidth=0.1, relheight=1)


root.mainloop()
