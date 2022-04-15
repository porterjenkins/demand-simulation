
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


    def _get_action(self, dist, prods, num_slots):
        action = {}
        for p in prods:
            action[p] = 0

        budget = num_slots
        for i, prob in enumerate(dist):
            q = int(np.round(num_slots * prob))
            if budget - q < 0:
                continue
            action[self.idx2prod[i]] += q
            budget -= q


        if budget > 0:
            idx = np.random.randint(0, len(prods))
            action[self.idx2prod[idx]] += budget
        return action





    def __call__(self, state, *args, **kwargs):
        values = self.mem.get_value()
        print(values)
        prods = list(self.prod2idx.keys())
        if values.sum() == 0.0:
            action = self.get_random(state, prods)
        else:
            dist = values / values.sum()
            action = self._get_action(dist, prods, num_slots=state.n_slots)

            n_allocated = int(np.sum(list(action.values())))
            # TODO: sometimes there's a bug here
            if n_allocated != state.n_slots:
                ax = self._get_action(dist, prods, num_slots=state.n_slots)
            assert n_allocated == state.n_slots, f"allocation: {n_allocated}, max: {state.n_slots}"
        return action

    def update(self, tup):
        self.mem.add(tup)
