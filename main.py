import py_compile
from coref_resolution import coref
from clausIE import char_to_action, svo, weather_extraction
from nltk.stem.snowball import SnowballStemmer
import nltk
from animation import animate
import gui

text = gui.txt1.get(1.0, "end-1c")
print(text)

# text = """A cat is walking on a snowy day. It jumped over a stone. It died. It ran. Dog is walking in the opposite direction. It ran. The dog said "Hello world, the cat is going to die hahaha".""" #  Dog is walking in the opposite direction. It ran. The dog said "Hello world"."""

# Coref resolution
corefed_text = coref.resolve_coref(text)

# Weather extraction
weather = weather_extraction.get_weather(text)

# Get svos
svos = svo.extract_svo(text, corefed_text)

# Assign char to action
svos = char_to_action.assign_char_to_action(svos)

# Create new stemmer for the words
stemmer = SnowballStemmer("english")

# Get actions_movement
actions_movement = {'die' : 0, 'fall' : 0, 'hurt' : 0, 'idle' : 0, 'jump' : 1, 'run' : 1, 'slide' : 1, 'walk' : 1, 'say': 0}
#word2vec similarity between the incoming action vs the ones we have in list of actions and then set a threshold and execute the action based on it

# nltk.download('omw-1.4')
# nltk.download('wordnet')

characters = char_to_action.get_characters(svos)
print(characters)

animate.animate(characters, svos, actions_movement, weather)