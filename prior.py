import numpy as np
from enum import Enum

class DisplayLocations(Enum):
    DELI = "deli"
    ENTRANCE = "entrance"
    DAIRY = "dairy"

    idx_map = {
        DELI: 0,
        ENTRANCE: 1,
        DAIRY: 2
    }

class Params(object):
    # [M, T, W, TH, F, Sa, Su]
    day_effect = [0, .5, .5, .6, 1.0, 1.25, 1.25]
    products = {
        "Coca_Cola_Classic_12_12oz_Cans_2525":
            {
                "price": -1.0,
                "effect": 1.5,
            },
        "Dr_Pepper_12_12oz_Cans_a480":
            {
                "price": -1.1,
                "effect": 1.25
            },
        "Diet_Coke_12_12oz_Cans_43fe":
            {
                "price": -1.2,
                "effect": 1.0
            },
        "Sprite_Lemon_Lime_12_12oz_Cans_12c1":
            {
                "price": -1.3,
                "effect": .5
            },
        "Coca_Cola_Classic_2l_Bottle_035c":
            {
                "price": -1.4,
                "effect": .5
            }
    }
    displays = {
        0: {"loc": DisplayLocations.DELI},
        1: {"loc": DisplayLocations.ENTRANCE},
        2: {"loc": DisplayLocations.DAIRY}
    }
    product_cov = np.array(
        [
            [1, 0, 1.5, -0.5, -1],
            [0, 1, 0, 1.5, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [-1, 0, 0, 0, 1],
        ]
    )

    disp_agg_demand = [.5, 1.0, -1.0]

    adj_mtx = np.array([
        [1, 1, 1],
        [0, 1, 1],
        [1, 1, 1]
    ])

    display_loc_effects = {
        "deli": 0.25,
        "dairy": -.5,
        "entrance": 0.5
    }




    def __init__(self):
        self.vals = self._get_vals()
        self.deg_mtx = self._get_deg_mtx(self.adj_mtx)
        self.disp_nbr_map = self._get_nbr_displays(self.adj_mtx)

    def _get_deg_mtx(self, A):
        # get D^-1/2
        D = np.diag(A.sum(axis=1))
        D = np.linalg.inv(D)
        D = np.power(D, .5)

        return D

    def _get_nbr_displays(self, A):
        disp_nbr_map = {}
        for i, row in enumerate(A):
            disp_nbr_map[i] = []
            for j, col in enumerate(row):
                if i != j and col == 1:
                    disp_nbr_map[i].append(j)

        return disp_nbr_map


    def _get_vals(self):
        x_day = np.array(Params.day_effect)
        x_price = []
        x_product = []
        x_disp_loc = []
        for product, prod_dta in self.products.items():
            x_price.append(prod_dta["price"])
            x_product.append(prod_dta["effect"])
        x_price = np.array(x_price)
        for disp, disp_cfg in self.displays.items():
            x_disp_loc.append(self.display_loc_effects[disp_cfg["loc"].value])
        x_disp_loc = np.array(x_disp_loc)
        x_prod_cov = [1.0]
        x_disp_val = [1.0]

        return np.concatenate([x_day, x_product, x_price, x_prod_cov, x_disp_val, x_disp_loc])







class Prior(object):

    price_shape = 10
    price_scale = 0.5
    product_display_prob = 0.6

    def __init__(self):
        self.params = Params()
        self.spatial_effects = self.get_display_spatial_effects()

    def gen_price(self):
        return np.random.gamma(self.price_shape, self.price_scale)

    def gen_quantity(self, features):
        lmbda = np.dot(self.params.vals, features)
        q = np.random.poisson(np.exp(lmbda))
        return q, lmbda

    def gen_product_set(self, products):
        idx = np.random.binomial(1, self.product_display_prob, len(products))
        return products[idx.astype(bool)], idx.reshape(-1, 1)

    def gen_display_prod_value(self, prod_vec):
        cov = Params.product_cov
        prod_cov_val = np.dot(
            prod_vec.transpose(),
            np.dot(cov, prod_vec)
        )
        return prod_cov_val.flatten()


    def get_display_spatial_effects(self):
        D = self.params.deg_mtx
        A = self.params.adj_mtx
        X = self.params.disp_agg_demand
        Z = np.dot(np.dot(np.dot(D, A),D), X)
        return Z

