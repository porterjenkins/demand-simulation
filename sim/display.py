import numpy as np
from sim import cfg
from uuid import uuid4
import pprint


class InventoryProduct(object):

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}: {self.quantity}"

    def increment(self):
        self.quantity += 1
    def decrement(self):
        if self.quantity >= 1:
            self.quantity -= 1
        else:
            raise ValueError(f"Current quantity of {self.name} = {self.quantity}")

    def restock(self, q):
        self.quantity = q


class Inventory(object):

    def __init__(self, n_slots, max_per_slot, products):

        self.n_prods = len(products)
        self.n_slots = n_slots
        self.inv = {}
        self.max_per_slot

        for slot_id in range(n_slots):

            idx = slot_id % self.n_prods
            p = products[idx]

            inv_prod = InventoryProduct(name=p, quantity=max_per_slot)
            self.inv[slot_id] = inv_prod

    def get_total_quantity(self):
        q = {}
        for idx, item in self.inv.items():
            if item.name not in q:
                q[item.name] = 0
            q[item.name] += item.quantity

        return q


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
        #state = np.zeros((self.n_prods, self.n_prods+1))
        state = []
        names = []

        prod_quant = self.get_total_quantity()


        for name, q in prod_quant.items():
            idx = cfg.prod2idx[name]
            state_vec = np.zeros(self.n_prods+1)
            state_vec[idx] = 1.0 # turn on product
            state_vec[-1] = 1.0 # turn on price

            if q > 0:
                state.append(state_vec)
                names.append(name)

        return np.array(state), names

    def restock(self):
        """
        Max Capcity is all available slots x max_per_slot

        :param action_dict: slots per product
        :return:
        """
        for _, v in self.inv.items():
            v.restock(self.max_per_slot)

    def decrement(self, product):

        shopped = False
        slot_id = 0
        while not shopped:
            prod_inv = self.inv[slot_id]
            if prod_inv.name == product and prod_inv.quantity > 0:
                prod_inv.decrement()
                shopped = True
            slot_id += 1
            if slot_id == self.n_slots and not shopped:
                # checked all slots and couldn't decrement. Exit loop
                shopped = True



class CoolerDisplay(object):


    def __init__(self, n_slots, max_per_slot, products, region, name=None):
        self.id = uuid4()
        self.n_slots = n_slots
        self.max_per_slot = max_per_slot
        self.products = products
        self.region = region
        self.inventory = self._get_init_inventory(n_slots, max_per_slot, products)
        self.name = name if name else str(self.id)

    def __str__(self):
        return self.name

    @staticmethod
    def _get_init_inventory(n_slots, max_per_slot, products):
        inv = Inventory(n_slots, max_per_slot, products)
        return inv

    def get_state_mtx(self):
        return self.inventory.get_state_mtx()

    def decrement(self, product):
        self.inventory.decrement(product)

    def print_state(self, n_cols=4):
        state_dict = self.inventory.inv
        n_slots = self.inventory.n_slots

        n_rows = n_slots // n_cols
        if n_slots % n_cols > 0:
            n_rows += 1

        state = np.array(["N/A"]*(n_rows*n_cols), dtype=object)

        for idx, inv in state_dict.items():
            state[idx] = inv.__str__()

        print("-"*20)
        print(self.__str__())
        print(state.reshape(n_rows, n_cols))

    def get_slot_counts(self):
        cnts = {}
        for id, inv in self.inventory.inv.items():
            cnts[id] = (inv.name, inv.quantity)

        return cnts





    @classmethod
    def build_displays_from_dict(cls, reg_dict):
        disp_list = []
        for reg, reg_data in reg_dict.items():
            for disp_type, dta in reg_data["displays"].items():
                display = CoolerDisplay(
                    n_slots=dta["n_slots"],
                    max_per_slot=dta["max_per_slot"],
                    products=cfg.get_product_names(),
                    name=cfg.get_disp_name(reg, disp_type),
                    region=reg
                )
                disp_list.append(display)

        return disp_list


if __name__ == "__main__":


    inv = Inventory(
        n_slots=11,
        max_per_slot=5,
        products=cfg.get_product_names()
    )
    inv.get_state_mtx()