# from numpy import character
import pygame
import glob
from time import sleep
import audioread
from constants import actions_movement
from utils import char_action_set_getter
from pathlib import Path
import os
from constants import dialogues_path, main_path

language = 'en'

SIZE = WIDTH, HEIGHT = 1280, 720 #the width and height of our screen
FPS = 7 #Frames per second

screen = pygame.display.set_mode(SIZE)
character_path = str(main_path / 'assets/characters')
weather_path = str(main_path / 'assets/weather')

dir_list = {'r' : 200, 'l' : 400} #moving towards which direction

dialogues = []
dialogue_count = 0

# Get character action mapping that is supported
char_action_set = char_action_set_getter.get_char_action_set()

class MySprite(pygame.sprite.Sprite):

    def __init__(self, char, x, y, dir):
        super(MySprite, self).__init__()
        
        self.images = {}
        self.image = pygame.Surface((0,0))
        self.char = char
        self.index = 0
        self.dir = dir
        self.x = x
        self.y = y
        self.prev_action = None
        self.dialogues_dir = str(dialogues_path / self.char)

    def play_dialogue(self, line_no):
        dialogue_path = self.dialogues_dir + "/dialogue" + str(line_no) + ".mp3"

        try:
            # Try playing the audio
            with audioread.audio_open(dialogue_path) as f:
                totalsec = f.duration
        except Exception as e:
            print("Error: audioread failed for dialogue path", dialogue_path)
            print(e)
            exit(1)

        try:
            pygame.mixer.init()
            pygame.mixer.music.load(dialogue_path)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()
            sleep(totalsec)
            
            pygame.mixer.music.unload()
        except Exception as e:
            print("ERROR: dialogue file with path", dialogue_path)

            if not os.path.exists(dialogue_path):
                print("Looks like the dialogues path does not exist. Check if dialogues are being generated properly and input path is correct")

            print("Here is the exception that occured: ")
            print(e)

        
    def movement_update(self, x_speed, y_speed, fps = FPS):
        if self.dir == 'r':                        
            self.x += x_speed
            self.y += y_speed
        else:
            self.image = pygame.transform.flip(self.image, True, False)
            self.x -= fps
            self.y += y_speed

        screen.blit(self.image, (self.x, self.y))
 
    def update(self, action):
        # Get images that are used to animate the given action
        flag = 0
        self.prev_action = action

        # Loading action images
        if action not in self.images or len(self.images[action]) == 0:
            print("Adding images for char ", self.char, " for action ", action)
            self.images[action] = [pygame.transform.scale(pygame.image.load(img) , (200,200)) for img in glob.glob(str(main_path) + "/assets/characters/" + self.char + "/" + action + "/*.png")]

        if self.index >= len(self.images[action]):
            flag = 1
            self.index = 0
            self.prev_action = action

        if not flag:
            self.image = self.images[action][self.index]
            self.index += 1
            if action in actions_movement:
                fps = FPS if actions_movement[action] else 0
                x, y = 0, 0
                if actions_movement[action] == 1:
                    x = fps
                elif actions_movement[action] == 2:
                    if self.index >= len(self.images[action]) // 2:
                        y = fps
                    else:
                        y = -fps

                self.movement_update(x, y, fps)
            else:
                self.movement_update(0, 0, 0)
        
        # Display prev action of the character until other character's action is completed
        else:
            self.prev_action = action
            self.play_prev_frame()
        

        print("self.index: ", max(self.index - 1, 0), "for char and action: ", self.char, action)

        return flag


    def play_prev_frame(self, char_in_scene=False):
        print("Playing previous action", self.prev_action, "of", self.char)

        # Play previous animation's last frame
        try:
            if self.prev_action is not None:
                self.image = self.images[self.prev_action][-1]

                self.movement_update(0, 0, 0)
            elif char_in_scene:
                print("Loading idle action for character: ", self.char)
                self.update('idle')
        except Exception as e:
            print("previous action failed to load for character: ", self.char)
            print(e)
        

def animate(characters, SVs, extracted_weather):
    bg = pygame.transform.scale(pygame.image.load(weather_path + '/' + extracted_weather + '.jpg') , SIZE)

    pygame.init()
    pygame.display.set_caption("StoryTube")
    
    char_objects = dict()

    dir_keys = list(dir_list.keys())

    for line_no, character in enumerate(characters):
        dir = dir_keys[line_no % 2]
        char_objects[character] = MySprite(character, dir_list[dir] * ((line_no % 2) + 1), 480, dir)

    clock = pygame.time.Clock()
    
    # svs is a list of lists. Each list refers to a line. Each line has a list of tuples if svos
    for line_no, line in enumerate(SVs):
        print("\n-----LINE ", line_no, "-----\n")
        flag = 0
        dialogues = {}
        characters_in_line = [sv[0] for sv in line]
        n = len(characters_in_line)

        done = {}
        for sv in line:
            done[sv] = 0

        while not flag:
            pygame.event.get()

            screen.fill((0,0,0))        
            screen.blit(bg, (0, 0))

            for sv in line:
                print("Animation sv: ", sv)
                character = sv[0]
                action = sv[1]
                dialogue = ""

                if(len(sv) == 3):
                    dialogue = sv[2]

                dialogues[character] = dialogue

                for char in char_objects:
                    if char not in characters_in_line:
                        char_objects[char].play_prev_frame(char_in_scene=False)

                if done[sv]:
                    char_objects[character].play_prev_frame(char_in_scene=True)
                    continue

                if action not in char_action_set[character]:
                    done[sv] = 1

                    char_objects[character].play_prev_frame(char_in_scene=True)

                    continue

                done[sv] = char_objects[character].update(action)

            pygame.image.save(screen,"screenshots\screenshot"+ str(line_no) +".jpg")
            pygame.display.update()
            clock.tick(FPS)

           

            print("Dialogues: ", dialogues)

            flag = 1

            for sv, x in done.items():
                if x == 0:
                    flag = 0
                    break

            if flag:
                for character, dialogue in dialogues.items():
                    if dialogue != "":
                        char_objects[character].play_dialogue(line_no)
                        print("dialogue played")
                        dialogues[character] = ""
