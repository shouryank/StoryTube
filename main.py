import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from coref_resolution import coref
from utils import char_action_set_getter, delete_files
from clausIE import refactor_sv, sv
from dialogue import dialogue_maker_file
import os, glob
from pathlib import Path
from constants import dialogues_path, screenshots_path
import sys
from animation import animate
import time

os.environ["TOKENIZERS_PARALLELISM"] = "false"

NUM_LABELS = 0
labels = []

def pipeline():
    #extracting the story from the gui
    # Default story:
    """
        A cat is walking on a snowy day. It jumped over a stone. It died. Dog is walking. It ran. The dog said "Hello world, the cat is going to die hahaha".
        this is sus : A detective was running on a sunny day. He saw a ninja boy. The ninja boy was attacking. The detective said "You are caught for attacking. Now die.". The ninja boy said "Catch me if you can".
        A boy is walking on a rainy day. The ninja boy attacks him. He runs for his life. The boy dies. The male zombie said "Now its time for revenge and to kill ugwal".
        An adventure girl is walking on a sunny day. A robot is walking on a rainy day. A robot says "Hi, I am AI, nice to meet you". The adventure girl says "oh my god! let's play together". The adventure girl runs.
    """

    for _ in range(NUM_LABELS):
        labels[0].destroy()
        labels.pop(0)

    txtbx.delete("1.0", "end")

    text = txt1.get(1.0, "end-1c")

    start = time.time()

    # Coref resolution
    corefed_text = coref.resolve_coref(text)    

    # Get svs
    svs = sv.extract_sv(text, corefed_text)

    # Assign char to action
    svs, characters = refactor_sv.refactor_sv(svs)

    # Delete all saved dialogues
    delete_files.delete_all_files(dialogues_path)

    # Delete all screenshots
    delete_files.delete_all_files(screenshots_path)

    # Save dialogues to be used
    line_no = 0
    for line_no, line in enumerate(svs):
        for SV in line:
            if len(SV) != 3 or SV[1] not in ["said", "say", "says"]:
                continue

            character = SV[0]
            dialogue = SV[2]

            dialogue_maker_file.create_dialogue(char=character, line_no=line_no, dialogue=dialogue)

            break

    animate.animate(characters, svs, text)

    display_pics()

    end = time.time()

    time_taken = end - start

    redirector(svs, time_taken)

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

def display_pics():
    
    global NUM_LABELS
    
    NUM_LABELS = min(len([name for name in os.listdir(screenshots_path) \
    if os.path.isfile(os.path.join(screenshots_path, name))]), 6)

    temp_x, temp_y = 250, 150
    images = [img for img in glob.glob(str(screenshots_path / "*.jpg"))]
    pics = []

    for i in range(NUM_LABELS):
        pic = ImageTk.PhotoImage((Image.open(images[i])).resize((200,125)))

        labels.append(Label(root))
        labels[i].image = pic
        labels[i].configure(image = pic)
        labels[i].pack()

        if i % 2 :
            labels[i].place(x=1050+temp_x, y=temp_y)
            temp_y += 150
        else:
            labels[i].place(x=1050, y=temp_y)

        pics.append(pic)

root = tk.Tk()
root.title("StoryTube")
root.geometry("1800x920")

bg = ImageTk.PhotoImage(Image.open('assets/background.png'))
label = Label( root, image = bg)
label.place(relx = 0, rely = 0)

# FIRST PARTITION

lbl1 = Label(root, bg = "#eae9d2", text="Welcome to StoryTube !!\n\n")
lbl1.place(x=100, y=10)
lbl1.config(font=('Times New Roman',20))
lbl2 = Label(root, bg = "#eae9d2", text="Write down your amazing story below :) \n\n")
lbl2.place(x=90, y=70)
lbl2.config(font=('Times New Roman',15))


txt1 = Text(root, height = 25, width = 45, bg = "light yellow")
txt1.place(x=30, y=150)
txt1.config(font=('Times New Roman',15))

print(txt1.get(1.0, "end-1c"))

ttk.Separator(master=root, orient=VERTICAL, style='red.TSeparator', class_= ttk.Separator, takefocus= 1, cursor='man').place(relx = 0.33, rely = 0, relheight=1)


# SECOND PARTITION

lbl3 = Label(root, bg = "#eae9d2", text="Intermediate Steps to the Animation\n")
lbl3.place(x=625, y=40)
lbl3.config(font=('Times New Roman',15))

txtbx = Text(root, height = 25, width = 45, bg = "light yellow")
txtbx.place( x = 550, y = 150)
txtbx.config(font=('Times New Roman',15))

def redirector(svs, time_taken):  

    string = str()
    for sv in svs:
        for tuple in sv:
            string += tuple[0] + "  " + tuple[1] + " "
            if len(tuple) > 2:
                string += '"'  + tuple[2] + '"'
            string += '\n'

    string += "\nEXECUTION FINISHED.\nTIME TAKEN: " + str(time_taken)
    
    txtbx.insert(INSERT, string)

btn1 = Button(root, bg = "#eae9d2", text="Submit story",fg="red", command=pipeline).place(x=225, y=725)

click_btn = PhotoImage(file='assets/help_icon.png')
img_label = Label(image=click_btn)
btn2 = Button(root, bg = "#eae9d2", image=click_btn,command= clicked_help, borderwidth=0).place(x=235, y=760)

ttk.Separator(master=root, orient=VERTICAL, style='red.TSeparator', class_= ttk.Separator, takefocus= 1, cursor='man').place(relx = 0.67, rely = 0, relheight=1)


# THIRD PARTITION


lbl4 = Label(root, bg = "#eae9d2", text="Frames of the output animation\n")
lbl4.place(x=1150, y=40)
lbl4.config(font=('Times New Roman',15))

root.mainloop()