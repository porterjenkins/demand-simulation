
import numpy as np

from recommenders.base_recommender import BaseRecommender
from recommenders.memory_buffer import TabularMemoryBuffer

class DemandMatchRecommender(BaseRecommender):

    def __init__(self, disp, prod2idx):
        super(DemandMatchRecommender, self).__init__(disp)
        self.prod2idx = prod2idx
        self.idx2prod = {}
        for k, v in prod2idx.items():
            self.idx2prod[v] = k

        self.mem = TabularMemoryBuffer(
            prod2idx=prod2idx,
            n_products=len(prod2idx)
        )

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

    def _get_action(self, dist, prods, num_slots):
        action = {}
        for p in prods:
            action[p] = 0

        budget = num_slots
        while budget > 0:
            for i, prob in enumerate(dist):
                q = int(np.round(num_slots * prob))
                action[self.idx2prod[i]] += q
                budget -= q
                if budget == 0:
                    break
        return action





    def __call__(self, state, *args, **kwargs):
        values = self.mem.get_value()
        prods = list(self.prod2idx.keys())
        if values.sum() == 0.0:
            action = self.get_random(state, prods)
        else:
            dist = values / values.sum()
            action = self._get_action(dist,prods,num_slots=state.n_slots)

            n_allocated = int(np.sum(list(action.values())))

            assert n_allocated == state.n_slots, f"allocation: {n_allocated}, max: {state.n_slots}"
        return action

    def update(self, tup):
        self.mem.add(tup)
