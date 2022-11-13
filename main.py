import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from coref_resolution import coref
from utils import char_action_set_getter
from clausIE import refactor_sv, sv, weather_extraction
from dialogue import dialogue_maker_file
import os
from pathlib import Path
from constants import dialogues_path
import sys
from animation import animate

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def pipeline():
    #extracting the story from the gui
    # Default story:
    """
        A cat is walking on a snowy day. It jumped over a stone. It died. Dog is walking in the opposite direction. It ran. The dog said "Hello world, the cat is going to die hahaha".
        A detective was running on a sunnny day. He saw a ninja boy. The ninja boy was attacking. The detective said "You are caught for attacking. Now die.". The ninja boy said "Catch me if you can".
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

    redirector(svs.__repr__())

    # Delete all saved dialogues
    dialogue_maker_file.delete_all_dialogues(dialogues_path)

    # Save dialogues to be used
    line_no = 0
    for line in svs:

        for SV in line:
            if len(SV) != 3 or SV[1] not in ["said", "say"]:
                continue

            character = SV[0]
            dialogue = SV[2]

            dialogue_maker_file.create_dialogue(char=character, line_no=line_no, dialogue=dialogue)

            break

        line_no += 1

    animate.animate(characters, svs, weather)


def clicked_help():
    help_window = Toplevel()
    help_window.title("Help")
    help_window.config(bg = "#eae9d2")
    lbl1 = Label(help_window, text="Here is your help !!", bg = "#eae9d2")
    lbl1.grid(column=0, row=0)
    lbl2 = Label(help_window, text="Here are some points to note when making your story!\n", bg = "#eae9d2")
    lbl2.grid(column=0, row=1)
    lbl3 = Label(help_window,bg = "#eae9d2", text="The available characters and their actions are as follows:\n\n" + char_action_set_getter.print_char_action_set(), justify=LEFT)# Adventure Girl : Dead, Idle, Jump, Melee, Run, Say, Shoot, Slide\n Boy : Dead, Hurt, Idle, Jump, Run, Say, Slide\n Cat : Die, Fall, Hurt, Idle, Jump, Run, Say, Slide, Walk\n Detective : Dead, Idle, Jump, Run, Say, Slide\n Dino : Dead, Idle, Jump, Run, Say, Walk\n Dog : Die, Fall, Hurt, Idle, Jump, Run, Say, Slide, Walk\n Girl : Dead, Idle, Jump, Run, Say, Walk\n Jack-o-lantern : Dead, Idle, Jump, Run, Say, Slide, Walk\n Kid : Dead, Idle, Jump, Run, Say, Walk\n Knight : Attack, Dead, Idle, Jump, Jumpattack, Run, Say, Walk\n Ninja Boy : Attack, Climb, Dead, Glide, Idle, Jump, Run, Say, Slide, Throw\n Ninja Girl : Attack, Climb, Dead, Glide, Idle, Jump, Run, Say, Slide, Throw\n Robot : Dead, Idle, Jump, Jumpmelee, Jumpshoot, Melee, Run, Runshoot, Say, Shoot, Slide\n Santa : Dead, Idle, Jump, Run, Say, Slide, Walk\n Zombie female : Attack, Dead, Idle, Say, Walk\n Zombie male : Attack, Dead, Idle, Say, Walk\n")
    lbl3.grid(column=0, row=2)
    lbl4 = Label(help_window, text="\n", bg = "#eae9d2")
    lbl4.grid(column=0, row=3)
    btn_exit = Button(help_window, text="Exit", fg="red", bg = "#eae9d2", command=help_window.destroy)
    btn_exit.grid(column=0, row=4)
    lbl5 = Label(help_window, text="\n\n", bg = "#eae9d2")
    lbl5.grid(column=0, row=5)
    help_window.mainloop()

# CHAR ACTION SET:  {'adventure girl': ['dead', 'idle', 'jump', 'melee', 'run', 'say', 'shoot', 'slide'], 'boy': ['dead', 'hurt', 'idle', 'jump', 'run', 'say', 'slide'], 'cat': ['die', 'fall', 'hurt', 'idle', 'jump', 'run', 'say', 'slide', 'walk'], 'detective': ['dead', 'idle', 'jump', 'run', 'say', 'slide'], 'dino': ['dead', 'idle', 'jump', 'run', 'say', 'walk'], 'dog': ['die', 'fall', 'hurt', 'idle', 'jump', 'run', 'say', 'slide', 'walk'], 'girl': ['dead', 'Idle', 'Jump', 'Run', 'say', 'Walk'], 'jack-o-latern': ['dead', 'idle', 'jump', 'run', 'say', 'slide', 'walk'], 'kid': ['dead', 'idle', 'jump', 'run', 'say', 'walk'], 'knight': ['attack', 'dead', 'idle', 'jump', 'jumpattack', 'run', 'say', 'walk'], 'ninja boy': ['attack', 'climb', 'dead', 'glide', 'idle', 'jump', 'run', 'say', 'slide', 'throw'], 'ninja girl': ['attack', 'climb', 'dead', 'glide', 'idle', 'jump', 'run', 'say', 'slide', 'throw'], 'robot': ['dead', 'idle', 'jump', 'jumpmelee', 'jumpshoot', 'melee', 'run', 'runshoot', 'say', 'shoot', 'slide'], 'santa': ['dead', 'idle', 'jump', 'run', 'say', 'slide', 'walk'], 'zombie female': ['attack', 'dead', 'idle', 'say', 'walk'], 'zombie male': ['attack', 'dead', 'idle', 'say', 'walk']}




root = tk.Tk()
root.title("StoryTube")
root.geometry("800x533")
bg = ImageTk.PhotoImage(Image.open('assets/background.png'))
label = Label( root, image = bg)
label.place(relx = 0, rely = 0)

lbl1 = Label(root, bg = "#eae9d2", text="Welcome to StoryTube !!\n\n").place(x=10, y=10)
lbl2 = Label(root, bg = "#eae9d2", text="Write down your amazing story below :) \n\n").place(x=10, y=40)

txt1 = Text(root, height = 20, width = 30, bg = "light yellow")
txt1.place(x=10, y=70)

print(txt1.get(1.0, "end-1c"))

ttk.Separator(master=root, orient=VERTICAL, style='red.TSeparator', class_= ttk.Separator, takefocus= 1, cursor='man').place(relx = 0.33, rely = 0, relheight=1)


lbl3 = Label(root, bg = "#eae9d2", text="Intermediate Steps to the Animation\n").place(x=300, y=40)

txtbx = Text(root, height = 20, width = 30, bg = "light yellow")
txtbx.place( x = 280, y = 70)

def redirector(inputStr):     
    txtbx.insert(INSERT, inputStr) 
    #txtbx.delete(0, END) clear tb after each story

# sys.stdout.write = redirector

btn1 = Button(root, bg = "#eae9d2", text="Submit story",fg="red", command=pipeline).place(x=90, y=420)

click_btn = PhotoImage(file='assets/help_icon.png')
img_label = Label(image=click_btn)
btn2 = Button(root, bg = "#eae9d2", image=click_btn,command= clicked_help, borderwidth=0).place(x=100, y=450)

# btn3 not working idk why
btn3 = Button(root, bg = "#eae9d2", text="Clear Text",fg="red",command= txtbx.delete("1.0","end")).place(x=370, y=450)


ttk.Separator(master=root, orient=VERTICAL, style='red.TSeparator', class_= ttk.Separator, takefocus= 1, cursor='man').place(relx = 0.67, rely = 0, relheight=1)



root.mainloop()
