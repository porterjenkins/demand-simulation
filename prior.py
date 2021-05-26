import numpy as np

class Params(object):
    # [M, T, W, TH, F, Sa, Su]
    day_effect = [0, 1.0, 1.0, .5, 3.0, 4.5, 5.5]
    products = {
        "Coca_Cola_Classic_12_12oz_Cans_2525":
            {
                "price": -1.0,
                "effect": 5.0,
            },
        "Dr_Pepper_12_12oz_Cans_a480":
            {
                "price": -1.1,
                "effect": 4.0
            },
        "Diet_Coke_12_12oz_Cans_43fe":
            {
                "price": -1.2,
                "effect": 3.0
            },
        "Sprite_Lemon_Lime_12_12oz_Cans_12c1":
            {
                "price": -1.3,
                "effect": 3.0
            },
        "Coca_Cola_Classic_2l_Bottle_035c":
            {
                "price": -1.4,
                "effect": 2.0
            }
    }
    product_cov = np.array(
        [
            [1, 0, 1.5, -0.5, -1],
            [0, 1, 0, 3, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [-1, 0, 0, 0, 1],
        ]
    )



    def __init__(self):
        x_day = np.array(Params.day_effect)
        x_price = []
        x_product = []
        for product, prod_dta in self.products.items():
            x_price.append(prod_dta["price"])
            x_product.append(prod_dta["effect"])
        x_price = np.array(x_price)
        x_prod_cov = [1.0]

        self.vals = np.concatenate([x_day, x_product, x_price, x_prod_cov])

    def get_vals(self):
        return self.vals






class Prior(object):

    price_shape = 10
    price_scale = 0.5
    product_display_prob = 0.6

    def __init__(self):
        self.params = Params().get_vals()

    def gen_price(self):
        return np.random.gamma(self.price_shape, self.price_scale)

    def gen_quantity(self, features):
        lmbda = np.dot(self.params, features)
        q = np.random.poisson(np.exp(lmbda))
        return q

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


