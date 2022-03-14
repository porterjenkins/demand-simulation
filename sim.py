import gym
import numpy as np
import datetime
import yaml

from store import Store
from prior import Prior, Params, DisplayLocations
from buffer import Buffer

class Simulator(gym.Env):
    dt_format = "%Y-%m-%d"

    def __init__(self, start_date, end_date):
        self.start_date = datetime.datetime.strptime(start_date, self.dt_format)
        self.end_date = datetime.datetime.strptime(end_date, self.dt_format)
        self.n_days = (self.end_date - self.start_date).days
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
            # gen daily price
            prices = {}
            for p in self.products:
                prices[p] = self.prior.gen_price()


            for d in range(self.n_displays):
                disp_loc = Params.displays[d]["loc"]
                product_disp_set, one_hot = self.prior.gen_product_set(self.products)
                prod_disp_val = self.prior.gen_display_prod_value(one_hot)
                disp_spatial_val = self.prior.spatial_effects[d]
                for p in product_disp_set:
                    x_t = self.featurize(
                        day_of_week=day.weekday(),
                        product=p,
                        price=prices[p],
                        disp_prod_val=prod_disp_val,
                        disp_val=disp_spatial_val,
                        disp_loc_type=disp_loc
                    )
                    q, lmbda = self.prior.gen_quantity(x_t)
                    self.buffer.add(
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
                    )
        self.buffer.to_csv("output.csv")

    @classmethod
    def build_sim(cls, cfg_path):
        with open(cfg_path, "r") as f:
            cfg = yaml.load(f)

        store = Store(
            adj_mtx=cfg["store"]["adj"],
            trans_mtx=cfg["store"]["transition"],
            names=cfg["store"]["names"]
        )


if __name__ == "__main__":
    sim = Simulator("2021-01-01", "2021-12-31")
    sim.main()