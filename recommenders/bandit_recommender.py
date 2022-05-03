import random
import numpy as np

from recommenders.base_recommender import BaseRecommender
from recommenders.memory_buffer import TabularQFunction

class BanditRecommender(BaseRecommender):

    def __init__(self, disp, prod2idx, eps=.1):
        super(BanditRecommender, self).__init__(disp)
        self.prod2idx = prod2idx
        self.idx2prod = {}
        self.eps = eps
        self.a_space = self.get_action_space(list(prod2idx.keys()))
        for k, v in prod2idx.items():
            self.idx2prod[v] = k

        self.mem = TabularQFunction(self.a_space)

    @staticmethod
    def get_action_space(prods):
        a_space = {}
        cntr = 0

        for p_i in prods:
            for p_j in prods:
                if p_i == p_j:
                    continue
                a_space[cntr] = (p_i, p_j)
                cntr += 1

        a_space[cntr] = (None, None)

        return a_space


    def _get_action(self, a_idx, state):
        action = state
        inc_prod, dec_prod = self.a_space[a_idx]
        if inc_prod is None:
            return state
        action[inc_prod] += 1
        action[dec_prod] -= 1

        return action


    def __call__(self, state, *args, **kwargs):
        prods = list(self.prod2idx.keys())
        p = random.random()

        if p < self.eps:
            action = self.get_random(state, prods)
        else:
            values = self.mem.get_value()
            a_idx = np.argmax(values)
            action = self._get_action(a_idx, state.slot_cnts)

        return action



    def update(self, tup):
        self.mem.add(tup)
