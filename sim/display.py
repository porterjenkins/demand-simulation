import numpy as np
from sim import cfg


class InventoryProduct(object):

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.quantity}"

    def increment(self):
        self.quantity += 1
    def decrement(self):
        if self.quantity >= 1:
            self.quantity -= 1
        else:
            raise ValueError(f"Current quantity = {self.}")

    def restock(self, q):
        self.quantity = q


class Inventory(object):

    def __init__(self, n_slots, max_per_slot, products):

        self.n_prods = len(products)
        self.n_slots = n_slots
        self.inv = {}
        for slot_id in range(n_slots):

            idx = slot_id % self.n_prods
            p = products[idx]

            inv_prod = InventoryProduct(name=p, quantity=max_per_slot)
            self.inv[slot_id] = inv_prod

    def get_state_mtx(self):
        """
            create a state matrix with dims (n_products x n_products+1)
            the matrix is essentiall an identity matrix concatenated with a column vector of ones
            each row "turns on" the product indicator and the price
                [
                    [1. 0. 0. 0. 0. 1.],
                    [0. 1. 0. 0. 0. 1.],
                    [0. 0. 1. 0. 0. 1.],
                    [0. 0. 0. 1. 0. 1.],
                    [0. 0. 0. 0. 1. 1.]
            ]
        :return:
        """
        state = np.zeros((self.n_prods, self.n_prods+1))

        for _, inv_prod in self.inv.items():
            idx = cfg.prod2idx[inv_prod.name]
            state[idx, idx] = 1.0 # turn on product
            state[idx, -1] = 1.0 # turn on price

        return state

    def restock(self, action_dict):
        """

        :param action_dict: slots per product
        :return:
        """
        pass

    def decrement(self, product):

        shopped = False
        slot_id = 0
        while not shopped:
            prod_inv = self.inv[slot_id]
            if prod_inv.name == product:
                prod_inv.decrement()
                shopped = True
            slot_id += 1



class CoolerDisplay(object):


    def __init__(self, n_slots, max_per_slot, products):
        self.n_slots = n_slots
        self.max_per_slot = max_per_slot
        self.products = products
        self.inventory = self._get_init_inventory(n_slots, max_per_slot, products)

    @staticmethod
    def _get_init_inventory(n_slots, max_per_slot, products):
        inv = Inventory(n_slots, max_per_slot, products)
        return inv

    def get_state_mtx(self):
        return self.inventory.get_state_mtx()

    def decrement(self, product):
        self.inventory.decrement(product)



if __name__ == "__main__":


    inv = Inventory(
        n_slots=11,
        max_per_slot=5,
        products=cfg.get_products()
    )
    inv.get_state_mtx()