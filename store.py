import numpy as np

### TODO: Implement Store class ###

class Store(object):

    def __init__(self, adj_mtx, trans_mtx, names):
        self.adj_mtx = np.array(adj_mtx)
        self.trans_mtx = np.array(trans_mtx)
        self.names = np.array(names)

        self.trans_mtx = self._norm_trans_mtx(self.adj_mtx, self.trans_mtx)


    @staticmethod
    def _norm_trans_mtx(adj_mtx, trans_mtx):

        trans_mtx = trans_mtx * adj_mtx
        normed_mtx = trans_mtx / trans_mtx.sum(axis=1).reshape(-1, 1)

        return normed_mtx