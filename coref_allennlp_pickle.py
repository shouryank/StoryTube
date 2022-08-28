from allennlp.predictors.predictor import Predictor
import pickle
# import allennlp_models.tagging

model_url = "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2020.02.27.tar.gz"
predictor = Predictor.from_path(model_url)

# create an iterator object with write permission - model.pkl
with open('allen_coref', 'wb') as files:
    pickle.dump(predictor, files)