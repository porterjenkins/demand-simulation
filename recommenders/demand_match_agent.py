
import numpy as np

from recommenders.base_recommender import BaseRecommender
from recommenders.memory_buffer import MemoryBuffer

class DemandMatchRecommender(BaseRecommender):

    def __init__(self, disp):
        super(DemandMatchRecommender, self).__init__(disp)
        self.mem = MemoryBuffer()

    def __call__(self, state, *args, **kwargs):
        pass


    def