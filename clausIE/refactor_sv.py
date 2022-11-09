from nltk.corpus import stopwords
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

stop_words = set(stopwords.words('english'))

def filter_sent(text):
    word_tokens = word_tokenize(text)
    filtered_subject = [w.lower() for w in word_tokens if not w.lower() in stop_words]
    return "".join(filtered_subject)

def refactor_sv(SVs):
    print("---------------REFACTOR SV MODEL MODULE---------------")
    svs = list()
    characters = set()

    for sv in SVs:
        # Remove stop words from subject
        subject = filter_sent(sv[0])
        characters.add(subject)

        final_sv = ()

        if sv[1] == "said":
            # If dialogue exists, append both the verb 'said' and dialogue
            action = WordNetLemmatizer().lemmatize(filter_sent(sv[1]), 'v')
            dialogue = sv[2]
            final_sv = (subject, action, dialogue)
        else:
            # If no dialogue, just append the verb
            action = WordNetLemmatizer().lemmatize(filter_sent(sv[1]), 'v')
            final_sv = (subject, action)

        svs.append(final_sv)

    print("---------------END OF REFACTOR SV MODEL MODULE---------------")

    return svs, characters