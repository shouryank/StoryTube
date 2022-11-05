import spacy
import claucy

nlp = spacy.load("en_core_web_sm")
claucy.add_to_pipe(nlp)

def get_svos(text):
    doc = nlp(text)
    SVOs = doc._.clauses
    return SVOs