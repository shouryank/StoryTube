import spacy
import claucy
import re
from coref_resolution import coref

nlp = spacy.load("en_core_web_sm")
claucy.add_to_pipe(nlp)

def get_sv_from_line(text):
    doc = nlp(text)
    SVs = doc._.clauses
    return SVs

# Input is the normal story and the coreference resolved story
def extract_sv(text, coref_text):
    print("---------------SV MODULE---------------")
    SVs = []
    for line, dialogue_line in zip(coref_text.split('.'), text.split('.')):
        SV = get_sv_from_line(line)
        if not line or not SV:
            continue
        print(SV)
        result = re.search(r"([\"\'])(?:(?=(\\?))\2.)*?\1", dialogue_line)
        print(line)
        if result:
            print("in if")
            SV = [(str(SV[0].subject), str(SV[0].verb), result.group().strip("\""))]
        else:
            print("else")
            SV = [(str(SV[0].subject), str(SV[0].verb))]
        print(line)
        print(SV)
        SVs += (SV)

    print("---------------END OF SV MODULE---------------")

    return SVs