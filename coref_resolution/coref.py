from distutils import core
import pickle
from pathlib import Path

# Get path of pickle file
p = Path(__file__).with_name('allen_coref')

# load saved model
with open(p , 'rb') as f:
    predictor = pickle.load(f)
    
def resolve_coref(text):
    print("---------------COREF MODULE---------------")
    
    prediction = predictor.predict(document=text)  # get prediction
    corefed_text = predictor.coref_resolved(text)

    for cluster in prediction['clusters']:
        print(cluster)  # list of clusters (the indices of spaCy tokens)

    print('\n\n') #Newline

    print('Coref resolved: ', corefed_text)  # resolved text

    print("---------------END OF COREF MODULE---------------")

    return corefed_text