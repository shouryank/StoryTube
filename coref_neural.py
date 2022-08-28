import spacy
import neuralcoref

nlp = spacy.load('en_core_web_sm')  # load the model
neuralcoref.add_to_pipe(nlp)

text = "Joseph Robinette Biden Jr. is an American politician who is the 46th and\
current president of the United States. A member of the Democratic Party, \
he served as the 47th vice president from 2009 to 2017 under Barack Obama and\
represented Delaware in the United States Senate from 1973 to 2009."

doc = nlp(text)  # get the spaCy Doc (composed of Tokens)

print(doc._.coref_clusters)  # You can see cluster of similar mentions
print(doc._.coref_resolved)