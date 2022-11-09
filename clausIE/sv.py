import spacy
from spacy.matcher import Matcher
import claucy
import re
from spacy.language import Language

nlp = spacy.load("en_core_web_sm")

'''Add logic to ignore dialogues in NLP'''
matcher = Matcher(nlp.vocab)
pattern = [{'ORTH': '"'},
           {'OP': '+', 'IS_ASCII': True},
           {'ORTH': '"'}]
matcher.add('QUOTED', [pattern])

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
            # print("@@@@@@ Spanned: ", [token for token in span], "######")
            
    return doc

nlp.add_pipe('quote_merger', first=True)  # add it right after the tokenizer
'''End of logic'''

# Claucy
claucy.add_to_pipe(nlp)

def get_sv_from_line(text):
    doc = nlp(text)
    SVs = doc._.clauses

    return SVs

# Input is the normal story and the coreference resolved story
def extract_sv(text, coref_text):
    print("---------------SV MODULE---------------")
    SVs = []
    # Iterate through each line
    for line, dialogue_line in zip(coref_text.split('.'), text.split('.')):
        # Append the list of SVs for that line
        SV = []
        SV += get_sv_from_line(line)

        # If empty line or no SV returned, skip
        if not line or not SV:
            continue

        # Extract the dialogues from the current line
        result = re.search(r"([\"\'])(?:(?=(\\?))\2.)*?\1", dialogue_line)

        SVs.append([])

        for sv in SV:
            # If dialogues are there in line
            if result:
                sv = [(str(sv.subject), str(sv.verb), result.group().strip("\""))]
            # If no dialogues
            else:
                sv = [(str(sv.subject), str(sv.verb))]
                
            SVs[-1] += sv

    print("SVs list returned: ", SVs)
    print("---------------END OF SV MODULE---------------")

    return SVs

if __name__ == "__main__":
    # Test for the module
    extract_sv('A cat is walking on a snowy day. It jumped over a stone. It died. Dog is walking in the opposite direction. It ran. The dog said "Hello world, the cat is going to die hahaha".', 
    'A cat is walking on a snowy day. It jumped over a stone. It died. Dog is walking in the opposite direction. It ran. The dog said "Hello world, the cat is going to die hahaha".')