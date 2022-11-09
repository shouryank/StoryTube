from nltk.corpus import stopwords
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

stop_words = set(stopwords.words('english'))

def assign_char_to_action(SVOs):
    print("---------------CHAR TO ACTION MODULE---------------")
    # Create empty dict
    svos = defaultdict(list)

    # Iterate over each svo
    for svo in SVOs:
        # SVO is in the format (subject, verb, object)
        # Get subject and tokenize it
        subject = svo[0]
        word_tokens = word_tokenize(subject)

        # Convert subject to lower
        filtered_sentence = [w.lower() for w in word_tokens if not w.lower() in stop_words]

        # If dialogue
        if svo[1] == "said":
            verb = []
            verb.append(svo[1])
            verb.append(svo[2])
        # If not dialogue
        else:
            verb = WordNetLemmatizer().lemmatize(svo[1])

        # Assign action to the character in the dict
        svos["".join(filtered_sentence)].append(verb)
    
    svos = dict(svos)
    print(svos)

    characters = list(i.lower() for i in svos.keys())
    print(characters)

    print("---------------END OF CHAR TO ACTION MODULE---------------")

    return svos

def get_characters(svos):
    return list(i.lower() for i in svos.keys())