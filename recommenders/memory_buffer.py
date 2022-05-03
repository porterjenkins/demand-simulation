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


class TabularQFunction(object):

    def __init__(self, a_space):
        self.a_space = a_space
        self.num_actions = len(a_space)
        self.q_a = np.zeros(self.num_actions)
        self.n_a = np.zeros(self.num_actions)

        self.action2idx = {}
        for k, v in a_space.items():
            self.action2idx[v] = k


    def add(self, tup):
        # TODO: add
        prod = tup[1]
        reward = tup[6]

        self.n_a[self.action2idx[a]] += 1
        current_val = self.q_a[self.action2idx[a]]

        cnt = self.q_a[self.action2idx[a]]

        self.q_a[self.action2idx[a]] = current_val + 1/cnt * (reward - current_val)


    def get_value(self):
        return self.q_a