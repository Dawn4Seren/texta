
# Uses scikit-learn 0.18.1

from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import GridSearchCV


class ModelNull(BaseEstimator):

    def fit(self, x, y):
        # Do nothing
        return self

    def transform(self, x):
        # Do nothing
        return x


class ModelStep:

    def __init__(self, name, model, label, params):
        self.name = name
        self.model = model
        self.label = label
        self.params = params

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_step(self):
        return (self.name, self.model())

    def get_param(self):
        param_dict = {}
        for k in self.params:
            p_name = '{0}__{1}'.format(self.name, k)
            p_value = self.params[k]
            param_dict[p_name] = p_value
        return param_dict


class PipelineBuilder:
    def __init__(self):
        self.extractor_list = []
        self.reductor_list = []
        self.normalizer_list = []
        self.classifier_list = []
        self.extractor_op = 0
        self.reductor_op = 0
        self.normalizer_op = 0
        self.classifier_op = 0

    def add_extractor(self, name, model, label, params):
        self.extractor_list.append(ModelStep(name, model, label, params))

    def add_reductor(self, name, model, label, params):
        self.reductor_list.append(ModelStep(name, model, label, params))

    def add_normalizer(self, name, model, label, params):
        self.normalizer_list.append(ModelStep(name, model, label, params))

    def add_classifier(self, name, model, label, params):
        self.classifier_list.append(ModelStep(name, model, label, params))

    def get_extractor_options(self):
        options = []
        for i, x in enumerate(self.extractor_list):
            options.append({'index': i, 'label': x.label})
        return options

    def get_reductor_options(self):
        options = []
        for i, x in enumerate(self.reductor_list):
            options.append({'index': i, 'label': x.label})
        return options

    def get_normalizer_options(self):
        options = []
        for i, x in enumerate(self.normalizer_list):
            options.append({'index': i, 'label': x.label})
        return options

    def get_classifier_options(self):
        options = []
        for i, x in enumerate(self.classifier_list):
            options.append({'index': i, 'label': x.label})
        return options

    def set_pipeline_options(self, extractor_op, reductor_op, normalizer_op, classifier_op):
        self.extractor_op = extractor_op
        self.reductor_op = reductor_op
        self.normalizer_op = normalizer_op
        self.classifier_op = classifier_op

    def pipeline_representation(self):
        e = self.extractor_list[self.extractor_op].name
        r = self.reductor_list[self.reductor_op].name
        n = self.normalizer_list[self.normalizer_op].name
        c = self.classifier_list[self.classifier_op].name
        rep = "{0} | {1} | {2} | {3}".format(e, r, n, c)
        return rep

    def build(self):
        # Build model Pipeline
        steps = []
        steps.append(self.extractor_list[self.extractor_op].get_step())
        steps.append(self.reductor_list[self.reductor_op].get_step())
        steps.append(self.normalizer_list[self.normalizer_op].get_step())
        steps.append(self.classifier_list[self.classifier_op].get_step())
        pipe = Pipeline(steps)
        # Build model params for Grid Search
        params = {}
        params.update(self.extractor_list[self.extractor_op].get_param())
        params.update(self.reductor_list[self.reductor_op].get_param())
        params.update(self.normalizer_list[self.normalizer_op].get_param())
        params.update(self.classifier_list[self.classifier_op].get_param())
        return pipe, params


def get_pipeline_builder():

    pipe_builder = PipelineBuilder()

    # Feature Extraction
    # params = {'ngram_range': [(1, 1), (1, 2), (1, 3)]}
    params = {'ngram_range': [(1, 1)]}
    pipe_builder.add_extractor('CountVectorizer', CountVectorizer, 'Count Vectorizer', params)

    params = {}
    pipe_builder.add_extractor('HashingVectorizer', HashingVectorizer, 'Hashing Vectorizer', params)

    params = {}
    pipe_builder.add_extractor('TfidfVectorizer', TfidfVectorizer, 'TfIdf Vectorizer', params)

    # Dimension Reduction
    params = {}
    pipe_builder.add_reductor('No_Reduction', ModelNull, 'None', params)

    params = {}
    pipe_builder.add_reductor('TruncatedSVD', TruncatedSVD, 'Truncated SVD', params)

    # Normalization
    params = {}
    pipe_builder.add_normalizer('No_Normalization', ModelNull, 'None', params)

    params = {}
    pipe_builder.add_normalizer('Normalizer', Normalizer, 'Normalizer', params)

    # Classification Models
    params = {}
    pipe_builder.add_classifier('MultinomialNB', MultinomialNB, 'Multinomial Naive Bayes', params)

    params = {}
    pipe_builder.add_classifier('BernoulliNB', BernoulliNB, 'Bernoulli Naive Bayes', params)

    params = {}
    pipe_builder.add_classifier('KNeighborsClassifier', KNeighborsClassifier, 'K-Neighbors', params)

    params = {}
    pipe_builder.add_classifier('RadiusNeighborsClassifier', RadiusNeighborsClassifier, 'Radius Neighbors', params)

    return pipe_builder


def train_model_with_cv(model, params, X, y):

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    # Use Train data to parameter selection in a Grid Search
    gs_clf = GridSearchCV(model, params, n_jobs=1, cv=5)
    gs_clf = gs_clf.fit(X_train, y_train)
    model = gs_clf.best_estimator_

    # Use best model and test data for final evaluation
    y_pred = model.predict(X_test)

    _f1 = f1_score(y_test, y_pred, average='micro')
    _confusion = confusion_matrix(y_test, y_pred)
    __precision = precision_score(y_test, y_pred)
    _recall = recall_score(y_test, y_pred)
    _statistics = {'f1_score': _f1,
                   'confusion_matrix': _confusion,
                   'precision': __precision,
                   'recall': _recall
                   }

    return model, _statistics


def save_model(model, file_name):
    joblib.dump(model, file_name)


def load_model(file_name):
    model = joblib.load(file_name)
    return model

