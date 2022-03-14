import numpy as np

class Store(object):

    def __init__(self, adj_mtx, trans_mtx, names):
        self.adj_mtx = np.array(adj_mtx)
        self.trans_mtx = np.array(trans_mtx)
        self.names = np.array(names)


    def _norm_trans_mtx(self, tra):