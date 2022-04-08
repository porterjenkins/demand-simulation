from recommenders.base_recommender import BaseRecommender


DEFAULT_ACTION = [{
    "region": "deli",
    "display": "deli-cooler",
    "action": {
        "coca_cola_20oz_bottle": 4,
        "dr_pepper_20oz_bottle": 0,
        "diet_coke_20oz_bottle": 0,
        "sprite_20oz_bottle": 0,
        "Monster_16oz_can": 4
    }
}, {
    "region": "entrance",
    "display": "entrance-cooler",
    "action": {
        "coca_cola_20oz_bottle": 4,
        "dr_pepper_20oz_bottle": 0,
        "diet_coke_20oz_bottle": 0,
        "sprite_20oz_bottle": 0,
        "Monster_16oz_can": 4
    }
}, {
    "region": "dairy",
    "display": "dairy-cooler",
    "action": {
        "coca_cola_20oz_bottle": 4,
        "dr_pepper_20oz_bottle": 0,
        "diet_coke_20oz_bottle": 0,
        "sprite_20oz_bottle": 0,
        "Monster_16oz_can": 4
    }
}]




class StaticRecommender(BaseRecommender):

    action = {
        "coca_cola_20oz_bottle": 4,
        "dr_pepper_20oz_bottle": 0,
        "diet_coke_20oz_bottle": 0,
        "sprite_20oz_bottle": 0,
        "Monster_16oz_can": 4
    }

    def __init__(self, disp):
        super(StaticRecommender).__init__(disp)

    def __call__(self, state, *args, **kwargs):
        return self.action