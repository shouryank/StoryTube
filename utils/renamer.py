import glob
import os
from pathlib import Path
from constants import main_path

path = str(main_path / 'assets' / 'dog')

# search text files starting with the word "sales"
pattern = path + "dead" + "*.png"

# List of the files that match the pattern
result = glob.glob(pattern)

# Iterating the list with the count
count = 1
for file_name in result:
    old_name = file_name
    new_name = path + 'die' + str(count) + ".png"
    os.rename(old_name, new_name)
    count = count + 1

# printing all revenue txt files
res = glob.glob(path + "die" + "*.png")
for name in res:
    print(name)