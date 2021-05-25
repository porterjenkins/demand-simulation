import numpy as np

class Prior(object):

    # [M, T, W, TH, F, Sa, Su]
    day_effect = [-1, 0, 0, .5, 1, 2.5, 2.5]

    def __init__(self):
        self.params = self._get_params()

    def _get_params(self):
        return np.array(self.day_effect)


    def get_quantity(self, features):
        lmbda = np.dot(self.params, features)
        q = np.random.poisson(lmbda)
        return q

