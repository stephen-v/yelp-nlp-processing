from allennlp.predictors.predictor import Predictor

predictor = Predictor.from_path('../models/openie-model.2018-08-20.tar.gz')
r =predictor.predict(
    sentence="I love this place! My fiance And I go here atleast once a week"
)
print(r)
