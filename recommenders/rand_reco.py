import numpy as np

from recommenders.base_recommender import BaseRecommender
from sim import cfg




class RandomRecommender(BaseRecommender):

    def __init__(self, disp):
        super(RandomRecommender, self).__init__(disp)

    def __call__(self, state, *args, **kwargs):

        prods = cfg.get_product_names()
        action = {}
        for p in prods:
            action[p] = 0

        budget = state.n_slots

        while budget > 0:
            candidates = np.random.permutation(prods)
            for p in candidates:
                step = np.random.randint(0, budget+1) # high is exclusive. need to ensure loop terminates
                action[p] += step
                budget -= step
                if budget == 0:
                    break

        return action


    def add_reward(self, reward):
        """

        :param reward: (tuple)
        :return:
        """
        pass
