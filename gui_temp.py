import os
import pygame
import tkinter as tk
from tkinter import *
from tkinter import ttk

root = tk.Tk()
embed = tk.Frame(root, width = 500, height = 500) #creates embed frame for pygame window
embed.grid(columnspan = (600), rowspan = 500) # Adds grid
embed.pack(side = TOP) #packs window to the left
buttonwin = tk.Frame(root, width = 75, height = 500)
buttonwin.pack(side = TOP)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
screen = pygame.display.set_mode((500,500))
screen.fill(pygame.Color(255,255,255))
pygame.display.init()
pygame.display.update()


def draw():
    pygame.draw.circle(screen, (0,0,0), (250,250), 125)
    pygame.display.update()

button1 = Button(buttonwin,text = 'Draw',  command=draw)
button1.pack(side=LEFT)
root.update()

while True:
    pygame.display.update()
    root.update()





# window = Tk()
# window.title("Welcome to TutorialsPoint")
# window.geometry('400x400')
# window.configure(background = "grey");
# a = Label(window ,text = "First Name").grid(row = 0,column = 0)
# b = Label(window ,text = "Last Name").grid(row = 1,column = 0)
# c = Label(window ,text = "Email Id").grid(row = 2,column = 0)
# d = Label(window ,text = "Contact Number").grid(row = 3,column = 0)
# a1 = Entry(window).grid(row = 0,column = 1)
# b1 = Entry(window).grid(row = 1,column = 1)
# c1 = Entry(window).grid(row = 2,column = 1)
# d1 = Entry(window).grid(row = 3,column = 1)
# def clicked():
#    res = "Welcome to " + txt.get()
#    lbl.configure(text= res)
# btn = ttk.Button(window ,text="Submit").grid(row=4,column=0)
# window.mainloop()
