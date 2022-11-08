import nltk
from nltk.corpus import wordnet

def weather_exraction(weather):
    synonyms = []
    for syn in wordnet.synsets(weather):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return synonyms

print(weather_exraction('sunny'))
