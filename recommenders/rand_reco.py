import numpy as np

from recommenders.base_recommender import BaseRecommender
from sim import cfg




class RandomRecommender(BaseRecommender):

    def __init__(self, disp):
        super(RandomRecommender, self).__init__(disp)

    def __call__(self, state, *args, **kwargs):

        prods = cfg.get_product_names()
        action = self.get_random(state, prods)

        return action


    def add_reward(self, reward):
        """

        :param reward: (tuple)
        :return:
        """
        pass
