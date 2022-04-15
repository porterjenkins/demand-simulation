import numpy as np

class BaseRecommender(object):

    def __init__(self, disp):
        self.disp = disp

    def __str__(self):
        return self.disp

    def __call__(self, state, *args, **kwargs):
        pass

    def update(self, tup):
        """ transition tuple """
        pass

    def get_random(self, state, prods):
        action = {}
        for p in prods:
            action[p] = 0

        budget = state.n_slots

        while budget > 0:
            candidates = np.random.permutation(prods)
            for p in candidates:
                step = np.random.randint(0, budget + 1)  # high is exclusive. need to ensure loop terminates
                action[p] += step
                budget -= step
                if budget == 0:
                    break
        return action
