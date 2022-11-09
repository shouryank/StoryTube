# from clausIE import sv
# from coref_resolution import coref

import claucy
import spacy
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import token

'''Old merger'''
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
pattern = [{'ORTH': '"'},
           {'OP': '+', 'IS_ALPHA': True},
           {'ORTH': '"'}]
matcher.add('QUOTED', [pattern])
from spacy.tokens import Doc

Doc.set_extension("dialogues", default = [])

@Language.component('quote_merger')
def quote_merger(doc):
    # this will be called on the Doc object in the pipeline
    matched_spans = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        matched_spans.append(span)
    with doc.retokenize() as retokenizer:
        for span in matched_spans:
            retokenizer.merge(span)
            joined_dialogue = " ".join([str(token) for token in span])
            doc._.dialogues.append(joined_dialogue)
            
    return doc

nlp.add_pipe('quote_merger', first=True)  # add it right after the tokenizer


claucy.add_to_pipe(nlp)

def get_sv_from_line(text):
    doc = nlp(text)
    print("Dialogues: ", doc._.dialogues)
    SVs = doc._.clauses
    SVs.append(doc._.dialogue)

    return SVs

print(get_sv_from_line(text))