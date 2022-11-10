import os

def get_char_action_set():
    char_action_set = dict()
    
    rootdir = os.getcwd() + '/assets/characters'

    for char in os.listdir(rootdir):
        char_action_set[char] = [x for x in os.listdir(rootdir + '/' + char)]

    return char_action_set