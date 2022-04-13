from recommenders.base_recommender import BaseRecommender
from sim import cfg

class StaticRecommender(BaseRecommender):

    action = {
        "coca_cola_20oz_bottle": 4,
        "dr_pepper_20oz_bottle": 0,
        "diet_coke_20oz_bottle": 0,
        "sprite_20oz_bottle": 0,
        "Monster_16oz_can": 4
    }

    def __init__(self, disp):
        super(StaticRecommender, self).__init__(disp)

    def __call__(self, state, *args, **kwargs):
        return self.action


class UniformRecommender(BaseRecommender):


    def __init__(self, disp):
        super(UniformRecommender, self).__init__(disp)

    def __call__(self, state, *args, **kwargs):

        prods = cfg.get_product_names()
        step = state.n_slots // len(prods)

        action = {}
        budget = state.n_slots

        while budget > 0:
            for p in prods:
                if p not in action:
                    action[p] = 0
                action[p] += step
                budget -= step
                if budget == 0:
                    break

        return action





