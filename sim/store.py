import numpy as np

class Region(object):
    def __init__(self, name, trans_probs, displays=[]):
        self.name = name
        self.trans_probs = trans_probs
        self.displays = []
        self.agents = []

    def __str__(self):
        return self.name

    def add_display(self, disp):
        self.displays.append(disp)

class Store(object):

    def __init__(self, adj_mtx, trans_mtx, names):
        self.adj_mtx = np.array(adj_mtx)
        self.trans_mtx = np.array(trans_mtx)
        self.names = names
        self.trans_mtx = self.norm_trans_mtx(self.adj_mtx, self.trans_mtx)

        self.regions = self.build_regions()


    def build_regions(self):
        """

        :return: (dict) regions dict with name as key
        """

        regions = {}
        for i, name in enumerate(self.names):
            reg = Region(
                name=name,
                trans_probs=self.trans_mtx[i, :]
            )
            regions[name] = reg

        return regions

    def add_displays_to_regions(self, disp_list):
        for disp in disp_list:
            self.regions[disp.region].add_display(disp)




    @staticmethod
    def norm_trans_mtx(adj_mtx, trans_mtx):

        trans_mtx = trans_mtx * adj_mtx
        normed_mtx = trans_mtx / trans_mtx.sum(axis=1).reshape(-1, 1)

        return normed_mtx