import os
from pathlib import Path
import re
import shutil

def order(folder_name):
    # Current path
    p = Path(folder_name)

    # # Iterate through each file
    for file in os.listdir(p):
        print(file)
        # Read non-numerical part of name
        # regex to get all elements before numerics
        res = re.findall('([a-zA-Z ]+[a-zA-Z])[^1-9]*([1-9]+[0-9*])[^0-9]*', file)
        print(res)
        if len(res) > 0 and len(res[0]) == 2:
            action = res[0][0]
            number = res[0][1]
        else: return

        new_path = p / action

        # # If no dir, make new dir
        # if not os.path.exists(new_path):
        #     print("Made new directory ", new_path)
        #     os.makedirs(new_path)

        # # put file in that dir
        # shutil.move(p / file, new_path / (action + number + '.png'))

if __name__ == '__main__':
    # Give animal name here
    for file in os.listdir(os.getcwd()):
        order(file)