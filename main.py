import tkinter as tk
from tkinter import *

from coref_resolution import coref

from clausIE import refactor_sv, sv, weather_extraction

from animation import animate

def pipeline():
    #extracting the story from the gui
    # Default story:
    """
        A cat is walking on a snowy day. It jumped over a stone. It died. Dog is walking in the opposite direction. It ran. The dog said "Hello world, the cat is going to die hahaha".
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


root = tk.Tk()
root.title("StoryTube")
lbl1 = Label(root, text="Welcome to StoryTube !!\n\n").grid(column=0, row=0)
lbl2 = Label(root, text="Here are some points to note when making your story!\n").grid(column=0, row=1)
lbl3 = Label(root, text="1. The available characters are :\nAdventure girl, boy, cat, detective, dinosaur, dog, girl, jack-o-lantern, kid, knight, ninja boy, ninja girl, robot, santa, female zombie, male zombie.\n\n").grid(column=0, row=2)
lbl4 = Label(root, text="Write down your amazing story below using the available characters :) \n\n").grid(column=0, row=1)

txt1 = Text(root, height = 10, width = 80, bg = "light yellow")
txt1.grid(column=0, row=3)

print(txt1.get(1.0, "end-1c"))

lbl5 = Label(root, text="\n\n").grid(column=0, row=4)
btn2 = Button(root, text="Submit story",fg="red", command=pipeline).grid(column=0, row=7)
lbl7 = Label(root, text="\n\n").grid(column=0, row=8)

root.mainloop()


