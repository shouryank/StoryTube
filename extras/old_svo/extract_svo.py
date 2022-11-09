from subject_verb_object_extract import findSVOs, nlp

def extract_svos(text):
    print("---------------SVO MODULE---------------")   

    tokens = nlp(text)
    SVOs = findSVOs(tokens)
    
    print(SVOs)
    print("---------------END OF SVO MODULE---------------")   

    return SVOs