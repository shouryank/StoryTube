import os

'''Function to get the actions supported by each character'''
def get_char_action_set():
    char_action_set = dict()
    
    rootdir = os.getcwd() + '/assets/characters'

    for char in os.listdir(rootdir):
        char_action_set[char] = [x for x in os.listdir(rootdir + '/' + char)]

    return char_action_set

'''Function to print all the characters followed by the actions supported. Used in GUI'''
def print_char_action_set():
    char_action_set = get_char_action_set()
    res = ""

    for character, actions in char_action_set.items():
        res += character.title() + ": "

        for action in actions[:-1]:
            res += action.title() + ", "

        if len(actions) > 0:
            res += actions[-1].title()

        res += "\n"
    
    res = res[:-1]

    return res


print(print_char_action_set())