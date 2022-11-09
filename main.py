import py_compile
from coref_resolution import coref
from clausIE import refactor_svo, svo, weather_extraction
from nltk.stem.snowball import SnowballStemmer
import nltk
from animation import animate
import gui

text = gui.text
print(text)

# text = """A cat is walking on a snowy day. It jumped over a stone. It died. It ran. Dog is walking in the opposite direction. It ran. The dog said "Hello world, the cat is going to die hahaha".""" #  Dog is walking in the opposite direction. It ran. The dog said "Hello world"."""

# Coref resolution
corefed_text = coref.resolve_coref(text)

# Weather extraction
weather = weather_extraction.get_weather(text)

# Get svos
svos = svo.extract_svo(text, corefed_text)

# Assign char to action
svos, characters = refactor_svo.refactor_svo(svos)

# Create new stemmer for the words
stemmer = SnowballStemmer("english")

#word2vec similarity between the incoming action vs the ones we have in list of actions and then set a threshold and execute the action based on it

# nltk.download('omw-1.4')
# nltk.download('wordnet')

animate.animate(characters, svos, weather)