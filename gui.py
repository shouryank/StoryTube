import os
import pygame
import tkinter as tk
from tkinter import *
from tkinter import ttk

# def submit_clear(root):
#     root.quit

def delete():
    text = txt1.get(1.0, "end-1c")
    print(text)
    txt1.delete("1.0","end")

root = tk.Tk()
root.title("StoryTube")
global txt1

def click():
    print("Story entered\n")

lbl1 = Label(root, text="Welcome to StoryTube !!\n\n").grid(column=0, row=0)
lbl2 = Label(root, text="Here are some points to note when making your story!\n").grid(column=0, row=1)
lbl3 = Label(root, text="1. The available characters are :\nAdventure girl, boy, cat, detective, dinosaur, dog, girl, jack-o-lantern, kid, knight, ninja boy, ninja girl, robot, santa, female zombie, male zombie.\n\n").grid(column=0, row=2)
lbl4 = Label(root, text="Write down your amazing story below using the available characters :) \n\n").grid(column=0, row=1)

txt1 = Text(root, height = 10, width = 80, bg = "light yellow")
txt1.grid(column=0, row=3)


lbl5 = Label(root, text="\n\n").grid(column=0, row=4)
# btn1 = Button(root, height = 1, width = 10, text ="Submit Story", command=click).grid(column=0, row=5)
# lbl6 = Label(root, text="\n\n").grid(column=0, row=6)
btn2 = Button(root, text="Submit story",fg="red", command=delete).grid(column=0, row=7)
lbl7 = Label(root, text="\n\n").grid(column=0, row=8)

root.mainloop()
