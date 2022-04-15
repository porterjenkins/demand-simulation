import json

class Rewards(object):

    def __init__(self, displays, products):
        self._rewards = {}
        for d in displays:
            self._rewards[d] = {}
            for p in products:
                self._rewards[d][p] = []

    def add_disp_product_rew(self, d, p, val):
        self._rewards[d][p].append(val)

    def add_rew_list(self, arr):
        if arr:
            for disp, prod, val in arr:
                self.add_disp_product_rew(disp, prod, val)
    def increment(self, r_i):
        for disp, disp_dict in self._rewards.items():
            if disp in r_i:
                for p in disp_dict.keys():
                    if p in r_i[disp]:
                        r_i_dict = r_i[disp][p]
                        self.add_disp_product_rew(disp, p, r_i_dict["total_sales"])
                    else:
                        self.add_disp_product_rew(disp, p, 0)
            else:
                for p in disp_dict.keys():
                    self.add_disp_product_rew(disp, p, 0)

    def todict(self):
        return self._rewards

    def save(self, fname):
        with open(fname, "w") as f:
            json.dump(self._rewards, f)