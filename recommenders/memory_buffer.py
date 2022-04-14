import numpy as np


class TabularMemoryBuffer(object):

    def __init__(self, prod2idx, n_products):
        self.prod2idx = prod2idx
        self.buffer = np.zeros(n_products)
        self.counter = np.zeros(n_products)

    def add(self, tup):
        # TODO: add
        prod = tup[1]
        reward = tup[6]
        self.buffer[self.prod2idx[prod]] += reward
        self.counter[self.prod2idx[prod]] += 1

    def get_value(self):
        if self.counter.sum() > 0:
            val = self.buffer / self.counter
        else:
            val = self.buffer
        val = np.nan_to_num(val, nan=0)
        return val