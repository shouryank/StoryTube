from numpy import character
import pygame
import glob
from time import sleep
from gtts import gTTS
import os
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import audioread

language = 'en'

SIZE = WIDTH, HEIGHT = 1280, 720 #the width and height of our screen
FPS = 7 #Frames per second

screen = pygame.display.set_mode(SIZE)
character_path = r'assets/characters/'
weather_path = r'assets/weather/'

dir_list = {'r' : 200, 'l' : 400} #moving towards which direction

dialogues = []
dialogue_count = 0

# Get actions_movement
actions_movement = {'die' : 0, 'fall' : 0, 'hurt' : 0, 'idle' : 0, 'jump' : 1, 'run' : 1, 'slide' : 1, 'walk' : 1, 'say': 0}

class MySprite(pygame.sprite.Sprite):

    def __init__(self, char, x, y, dir):
        super(MySprite, self).__init__()
        
        self.images = {}
        self.actions = []
        self.char = char
        self.index = 0
        self.action_count = 0
        self.dir = dir
        self.x = x
        self.y = y
        self.prev_action = None  

    def play_dialogue(self, dialogue):
        myobj = gTTS(text=self.char + " said " + dialogue, lang=language, slow=False)
        myobj.save("dialogue.mp3")
        with audioread.audio_open('dialogue.mp3') as f:
            totalsec = f.duration

        pygame.mixer.init()
        pygame.mixer.music.load("dialogue.mp3")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()
        sleep(totalsec)
        
        pygame.mixer.music.unload()

        
    def movement_update(self, fps = FPS):
        if self.dir == 'r':                        
            self.x += fps
        else:
            self.image = pygame.transform.flip(self.image, True, False)
            self.x -= fps
        screen.blit(self.image, (self.x, self.y))
 
    def update(self, action):
        # Get images that are used to animate the given action
        flag = 0
        if action not in self.images or len(self.images[action]) == 0:
            print("Adding images for char ", self.char, " for action ", action)
            self.images[action] = [pygame.transform.scale(pygame.image.load(img) , (200,200)) for img in glob.glob("assets\\characters\\" + self.char + "\\" + action + "\\*.png")]

        if self.index >= len(self.images[action]):
            flag = 1
            self.index = 0
            self.prev_action = action

        if not flag:
            self.image = self.images[action][self.index]
            self.index += 1

            self.movement_update(FPS if actions_movement[action] else 0)
        else:
            self.prev_action = action
            self.play_prev_frame()
        

        print("self.index: ", max(self.index - 1, 0))

        return flag

    def play_prev_frame(self):
        if self.prev_action is None:
            return
        try:
            self.image = self.images[self.prev_action][-1]
        except:
            print("character: ", self.char)
            exit(1)

        print("PLAYING PREVIOUS ACTION ", self.prev_action, " OF ", self.char, " IMAGE ", self.image)

        self.movement_update(0)
        

def animate(characters, SVs, extracted_weather):
    bg = pygame.transform.scale(pygame.image.load(weather_path + extracted_weather + '.jpg') , SIZE)

    pygame.init()
    pygame.display.set_caption("Trace")

    char_objects = dict()

    for i, character in enumerate(characters):
        dir = list(dir_list.keys())[i % 2]
        char_objects[character] = MySprite(character, dir_list[dir] * ((i % 2) + 1), 480, dir)

    clock = pygame.time.Clock()
    i = 1
    # svs is a list of lists. Each list refers to a line. Each line has a list of tuples if svos
    for line in SVs:
        print("\n-----LINE ", i, "-----\n")
        i += 1
        flag = 0
        dialogues = {}
        characters_in_line = [sv[0] for sv in line]
        
        while not flag:
            pygame.event.get()

            screen.fill((0,0,0))        
            screen.blit(bg, (0, 0))

            for sv in line:
                character = sv[0]
                action = sv[1]
                dialogue = ""

                if(len(sv) == 3):
                    dialogue = sv[2]

                flag = char_objects[character].update(action)

                if not flag:
                    dialogues[character] = dialogue

                for char in char_objects:
                    if char not in characters_in_line:
                        char_objects[char].play_prev_frame()

            pygame.display.update()
            clock.tick(FPS)

            for character, dialogue in dialogues.items():
                if dialogue != "":
                    char_objects[character].play_dialogue(dialogue)
                    print("dialogue played")
                    dialogues[character] = ""
