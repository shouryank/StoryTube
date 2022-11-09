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
 
class MySprite(pygame.sprite.Sprite):

    def __init__(self, char, x, y, dir, svos, actions_movement):
        super(MySprite, self).__init__()
        
        self.images = {}
        self.actions = []
        # self.images = [pygame.image.load(img) for img in glob.glob("pygame\\cat\\*.png")]
        for action in svos[char]:
            if type(action) == list:
                dialogues.append(action[1])

            # self.actions.append(action[0] if type(action) == list else action)
                        
            action = WordNetLemmatizer().lemmatize(action[0] if type(action) == list else action,'v')   
            self.actions.append(action)
            print(self.actions)

            if action not in self.images:
                self.images[action] = [pygame.transform.scale(pygame.image.load(img) , (200,200)) for img in glob.glob(character_path + char + "\\" + action + "\\*")]
            
        print(self.images)
        self.char = char
        self.index = 0
        self.action_count = 0
        self.dir = dir
        self.x = x
        self.y = y
        self.svos = svos
        self.actions_movement = actions_movement
        self.image = None

    def play_dialogue(self, index):
        myobj = gTTS(text=dialogues[index], lang=language, slow=False)
        myobj.save("dialogue.mp3")
        with audioread.audio_open('dialogue.mp3') as f:
            totalsec = f.duration
        pygame.mixer.init()
        pygame.mixer.music.load("dialogue.mp3")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()
        sleep(totalsec)
        
    def movement_update(self):
        # if self.x == 880:
        #     self.dir = 'l'
        # elif self.x == 0:
        #     self.dir = 'r'

        if self.dir == 'r':                        
            self.x += FPS
        else:
            self.image = pygame.transform.flip(self.image, True, False)
            self.x -= FPS
        screen.blit(self.image, (self.x, self.y))
 
    def update(self):
        # print(self.index, self.action_count, len(self.actions), len(self.images[self.actions[self.action_count]]))
        print(self.actions[self.action_count])
        if self.actions[self.action_count] == "say":
            global dialogue_count
            self.play_dialogue(dialogue_count)
            dialogue_count += 1
            print("dialogue played")
        if self.index >= len(self.images[self.actions[self.action_count]]):
            if self.action_count >= len(self.actions) - 1:
                return 1
            self.index = 0
            self.action_count += 1
        self.image = self.images[self.actions[self.action_count]][self.index]
        self.index += 1

        if self.actions_movement[self.actions[self.action_count]]:
            self.movement_update()
        else:
            screen.blit(self.image, (self.x, self.y))
        
        return 0

    def update_idle(self):
        self.image = pygame.transform.scale(pygame.image.load(character_path + self.char + "/idle/idle1.png") , (200,200))
        flip_var = True if self.dir == "l" else False
        print(flip_var)
        self.image = pygame.transform.flip(self.image, flip_var, False)
        screen.blit(self.image, (self.x, self.y))
        
 
def animate(characters, svos, actions_movement, extracted_weather):
    bg = pygame.transform.scale(pygame.image.load(weather_path + extracted_weather + '.jpg') , SIZE)

    pygame.init()
    pygame.display.set_caption("Trace")
    char_objects = []
    for i in range(len(characters)):
        dir = list(dir_list.keys())[i % 2]
        char_objects.append(MySprite(characters[i], dir_list[dir] * ((i % 2) + 1), 480, dir, svos, actions_movement))
    # my_group = pygame.sprite.Group(my_sprite)

    idle_char = []
    clock = pygame.time.Clock()
    
    loop = 1
    count = 0 # number of characters whos actions have been completed


    return_val = 0
    while count < len(characters): 

        pygame.event.get() 
        
        screen.fill((0,0,0))        
        screen.blit(bg, (0, 0))

        for char in char_objects:
            return_val = char.update()   
            print(return_val) 
            if return_val == 1:
                char_objects.remove(char)
                idle_char.append(char)
                count += return_val
        
        for char in idle_char:
            print(char.x)
            char.update_idle()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()