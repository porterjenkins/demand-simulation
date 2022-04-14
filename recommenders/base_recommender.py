
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