from gtts import gTTS
import random
from pathlib import Path
import os, shutil
from constants import dialogues_path

language = 'en'

def create_dialogue(char, line_no, dialogue):
    print("---------------DIALOGUE MODULE---------------")
    print("Character: ", char, "line_no: ", line_no)
    print("Dialogue: ", dialogue)

    # Create directory to store the dialogues
    dialogues_dir = dialogues_path / char
    dialogues_dir.mkdir(parents=True, exist_ok=True)

    print("Dialogue_dir is ", dialogues_dir)

    tlds = ["com.au", "co.uk", "com", "ca", "co.in", "ie", "co.za"]
    myobj = gTTS(text = char + " said " + dialogue, lang = language, slow=False, tld=random.choice(tlds))

    dialogue_file_name = str(dialogues_dir) + "/dialogue" + str(line_no) + ".mp3"

    print("Saving dialogue ", dialogue_file_name, "at path ", dialogues_dir)

    myobj.save(dialogue_file_name)

    print("---------------END OF DIALOGUE MODULE---------------")


