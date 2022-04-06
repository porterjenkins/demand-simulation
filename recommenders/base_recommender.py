
class BaseRecommender(object):

    def __init__(self, disp):
        self.disp = disp


    def __call__(self, state, *args, **kwargs):
        pass