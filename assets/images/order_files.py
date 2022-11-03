import os
from pathlib import Path
import re
import shutil

def order(folder_name):
    # Current path
    p = Path(folder_name)

    # # Iterate through each file
    for file in os.listdir(p):
        # Read non-numerical part of name
        # regex to get all elements before numerics
        res = re.findall('([a-zA-Z ]*)\d*.*', file)
        name = res[0]

        new_path = p / name

        # If no dir, make new dir
        if not os.path.exists(new_path):
            print("Made new directory ", new_path)
            os.makedirs(new_path)

        # put file in that dir
        shutil.move(p / file, new_path / file)

if __name__ == '__main__':
    # Give animal name here
    order('cat')