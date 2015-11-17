import logging
from constants import Objective



class Pipeline(object):


    def __init__(self, transformer, model_klass, model_params, objective, log_level=logging.DEBUG):
        """
        The transformer should be a Preprocess class.
        The model_klass should be the class of the model.
        The model_params are a dict of the params to initialize the model.
        """
        # populate the model params with the Pipeline params
        # unless they're otherwise defined
        if 'objective' not in model_params:
            model_params['objective'] = objective
        if 'log_level' not in model_params:
            model_params['log_level'] = log_level

        self.transformer = transformer
        self.model_klass = model_klass
        self.model_params = model_params
        self.objective = objective
        self.log_level = log_level


    def fit(self, data, targets, unsupervised_data=None):
        """
        Should accept a dataset and targets.
        Should set self.hyper_params
        """

        # test without transforming data to get a baseline score
        model = self.model_klass(**self.model_params)
        model.optimize(data, targets)
        best = model.best_score
        self.hyper_params = None
        print 'score without transformation', model.best_score  # TODO logging

        # the transformer class should return a generator of modified datasets
        # test each one with the model, and if the performance is better, then
        # set the new best score to that performance
        for transformed, hyper_params in self.transformer().each_transformation(data, unsupervised_data):
            model = self.model_klass(**self.model_params)
            model.optimize(transformed, targets)
            print model.best_score, hyper_params  # TODO logging

            if self.objective == Objective.MINIMIZE:
                if model.best_score < best:
                    best = model.best_score
                    self.hyper_params = hyper_params
            elif self.objective == Objective.MAXIMIZE:
                if model.best_score > best:
                    best = model.best_score
                    self.hyper_params = hyper_params



    def transform(self, data):
        if self.hyper_params:
            return self.transformer().transform(data, **self.hyper_params)
        else:
            # TODO logger.warn('hyper_params set to None. Either you forgot to run .fit(), or .fit() found no improvement')
            return data
