from nltk.corpus import stopwords
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

stop_words = set(stopwords.words('english'))

def filter_sent(text):
    word_tokens = word_tokenize(text)
    filtered_subject = [w.lower() for w in word_tokens if not w.lower() in stop_words]
    return "".join(filtered_subject)

def refactor_svo(SVOs):
    print("---------------REFACTOR SVO MODEL MODULE---------------")
    svos = list()
    characters = set()

    for svo in SVOs:
        # Remove stop words from subject
        subject = filter_sent(svo[0])
        characters.add(subject)

        final_svo = ()

        if svo[1] == "said":
            # If dialogue exists, append both the verb 'said' and dialogue
            action = WordNetLemmatizer().lemmatize(filter_sent(svo[1]), 'v')
            dialogue = svo[2]
            final_svo = (subject, action, dialogue)
        else:
            # If no dialogue, just append the verb
            action = WordNetLemmatizer().lemmatize(filter_sent(svo[1]), 'v')
            final_svo = (subject, action)

        svos.append(final_svo)

    print("---------------END OF REFACTOR SVO MODEL MODULE---------------")

    return svos, characters