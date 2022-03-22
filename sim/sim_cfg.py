import os
import sys

# path = os.path.join(os.path.dirname(__file__), os.pardir)
# sys.path.append(path)
os.chdir(os.path.join(os.path.dirname(__file__)))

import yaml
import numpy as np
class SimCfg(object):

    def __init__(self, cfg_path):
        # print(os.listdir())
        # print(os.path.join(os.path.dirname(__file__)))
        with open(cfg_path, "r") as f:
            self.cfg_dict = yaml.safe_load(f)

        self.prod2idx = {}
        self.idx2prod = {}
        self.reg2idx = {}
        self.idx2reg = {}

        i = 0
        for p, prod_dict in self.cfg_dict["params"]["products"].items():
            self.prod2idx[p] = i
            self.idx2prod[i] = p
            i += 1

        i = 0
        for r, reg_dict in self.cfg_dict["store"]["regions"].items():
            self.reg2idx[r] = i
            self.idx2reg[i] = r
            i += 1

    def get_products(self):
        products = []
        for p, idx in self.prod2idx.items():
            products.append(p)

        return products

    def get_prod_weight(self):
        weights = []
        for p, idx in self.prod2idx.items():
            weights.append(self.cfg_dict["params"]["products"][p]["weight"])

        return weights

    def get_price_by_product(self, p):
        p = self.cfg_dict["params"]["products"][p]["price"]
        return p

    def get_prod_prices(self):
        prices = []
        for p, idx in self.prod2idx.items():
            prices.append(self.cfg_dict["params"]["products"][p]["price"])
        return prices

    def get_price_param(self):
        return self.cfg_dict["params"]["price"]

    def get_adj_mtx(self):
        return np.array(self.cfg_dict["store"]["adj"])

    def get_trans_mtx(self):
        return np.array(self.cfg_dict["store"]["transition"])

    def get_region_dict(self):
        return self.cfg_dict["store"]["regions"]

    def get_region_names(self):
        return list(self.cfg_dict["store"]["regions"].keys())

    def get_var_param(self):
        return self.cfg_dict["params"]["sigma"]

    def get_time(self):
        return self.cfg_dict["time"]

    def get_start_time(self):
        return self.cfg_dict["time"]["start"]

    def get_end_time(self):
        return self.cfg_dict["time"]["end"]

    def get_timedelta(self):
        td_dict = self.cfg_dict["time"]["timedelta"]
        return td_dict["resolution"]