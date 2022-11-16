from distutils import core
import pickle
from pathlib import Path
import re

# Get path of pickle file
p = Path(__file__).with_name('allen_coref')

# load saved model
with open(p , 'rb') as f:
    predictor = pickle.load(f)
    
def resolve_coref(text):
    print("---------------COREF MODULE---------------")
    # Remove dialogues
    text = re.sub(r"([\"\'])(?:(?=(\\?))\2.)*?\1", " ", text)

    corefed_text = predictor.coref_resolved(text)

    print('Coref resolved: ', corefed_text)  # resolved text

    print("---------------END OF COREF MODULE---------------")

    return corefed_text

