import gym
import numpy as np
import datetime
import yaml

from sim import cfg

from sim.store import Store
from sim.prior import Prior, Params, DisplayLocations
from buffer import Buffer
from sim.agent import Agent
from sim.display import CoolerDisplay

class Simulator(gym.Env):
    dt_format = "%Y-%m-%d"

    def __init__(self, start_date, end_date, store):
        #self.start_date = datetime.datetime.strptime(start_date, self.dt_format)
        #self.end_date = datetime.datetime.strptime(end_date, self.dt_format)
        self.start_date = start_date
        self.end_date = end_date

        self.n_days = (self.end_date - self.start_date).days
        self.store = store

        self.products = np.array(list(Params.products.keys()))
        self.n_displays = len(Params.displays)

        self.product_idx = {}
        for i, p in enumerate(self.products):
            self.product_idx[p] = i


        self.prior = Prior()
        self.buffer = Buffer()

    def _day_of_week_features(self, day):
        x = np.zeros(7)
        x[day] = 1.0
        return x

    def _product_features(self, product):
        x = np.zeros(len(self.products))
        x[self.product_idx[product]] = 1.0
        return x
    def _disp_loc_features(self, disp_loc_type):
        x = np.zeros(len(DisplayLocations.idx_map.value))
        x[DisplayLocations.idx_map.value[disp_loc_type.value]] = 1.0
        return x

    def featurize(self, day_of_week, product, price, disp_prod_val, disp_val, disp_loc_type):
        x_day = self._day_of_week_features(day_of_week)
        x_product = self._product_features(product)
        x_price = x_product*price
        x_disp_loc = self._disp_loc_features(disp_loc_type)

        return np.concatenate([x_day, x_product, x_price, disp_prod_val, [disp_val], x_disp_loc])

    def _stringify_list(self, l):
        l = [str(x) for x in l]
        s = ",".join(l)
        return "{" + s + "}"

    def main(self):

        for t in range(self.n_days):
            day = self.start_date + datetime.timedelta(days=t)

            # TODO: Insert simulation logic here

            """self.buffer.add(
                (
                    q,
                    day,
                    p,
                    d,
                    prices[p],
                    disp_loc.value,
                    self._stringify_list(product_disp_set),
                    self._stringify_list(self.prior.params.disp_nbr_map[d])

                )
            )"""
        self.buffer.to_csv("output.csv")

    @classmethod
    def build_sim(cls):

        store = Store(
            adj_mtx=cfg.get_adj_mtx(),
            trans_mtx=cfg.get_trans_mtx(),
            region_dict=cfg.get_region_dict()
        )

        displays = CoolerDisplay.build_displays_from_dict(
            cfg.get_region_dict()
        )
        store.add_displays_to_regions(displays)


        agents = Agent.build_agents(
            n_agents=10,
            product_params=cfg.get_prod_weight(),
            price_params=cfg.get_price_param(),
            sigma=cfg.get_var_param()
        )

        sim = Simulator(
            start_date=cfg.get_start_time(),
            end_date=cfg.get_end_time(),
            store=store
        )

        return sim



if __name__ == "__main__":
    sim = Simulator.build_sim()

    #sim.main()