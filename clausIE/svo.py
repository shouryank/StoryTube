import spacy
import claucy
import re
from coref_resolution import coref

nlp = spacy.load("en_core_web_sm")
claucy.add_to_pipe(nlp)

def get_svo_from_line(text):
    doc = nlp(text)
    SVOs = doc._.clauses
    return SVOs

# Input is the normal story and the coreference resolved story
def extract_svo(text, coref_text):
    print("---------------SVO MODULE---------------")
    SVOs = []
    for line, dialogue_line in zip(coref_text.split('.'), text.split('.')):
        SVO = get_svo_from_line(line)
        if not line or not SVO:
            continue
        print(SVO)
        result = re.search(r"([\"\'])(?:(?=(\\?))\2.)*?\1", dialogue_line)
        print(line)
        if result:
            print("in if")
            SVO = [(str(SVO[0].subject), str(SVO[0].verb), result.group().strip("\""))]
        else:
            print("else")
            SVO = [(str(SVO[0].subject), str(SVO[0].verb))]
        print(line)
        print(SVO)
        SVOs += (SVO)

    print("---------------END OF SVO MODULE---------------")

    return SVOs