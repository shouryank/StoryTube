import spacy
from spacy.matcher import Matcher
import claucy
import re
from spacy.language import Language
import split_text_to_sentences

'''Add logic to ignore dialogues in NLP'''
nlp = spacy.load("en_core_web_sm")
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

'''
    Main function that actually extracts the SV
    Input is the normal story and the coreference resolved story
'''
def extract_sv(text, coref_text):
    print("---------------SV MODULE---------------")
    SVs = []

    # Split text into sentences
    raw_sentences = split_text_to_sentences.split_into_sentences(text)
    coref_sentences = split_text_to_sentences.split_into_sentences(coref_text)

    print(raw_sentences, end = "\nUNGABUNGA\n")
    print(coref_sentences, end = "\nUNGABUNGA\n")

    # Iterate through each line
    for line, dialogue_line in zip(coref_sentences, raw_sentences):
        # Subsititute dialogue        
        re.sub(r"([\"\'])(?:(?=(\\?))\2.)*?\1", " ", line)

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
                print(line)
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
    extract_sv('A detective was walking on a sunnny day. He saw a ninja boy. The ninja boy was attacking. The detective said "You are caught for attacking. Now die.".', 
    'A detective was walking on a sunnny day. He saw a ninja boy. The ninja boy was attacking. The detective said "You are caught for attcking. Now die.".')