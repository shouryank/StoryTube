import re

def split_into_sentences(text):
    # Regex to ignore full stops in quotes
    pattern = re.compile(r'''((?:[^."]|"[^"]*")+)''')

    # Split text into sentences
    sentences = pattern.split(text)[1::2]

    # Strip white spaces
    sentences = [s.strip() for s in sentences]
    
    return sentences