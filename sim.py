import numpy as np
import datetime

from prior import Prior, Params
from buffer import Buffer

class Simulator(object):
    dt_format = "%Y-%m-%d"

    def __init__(self, n_displays, start_date, end_date):
        self.n_displays = n_displays
        self.start_date = datetime.datetime.strptime(start_date, self.dt_format)
        self.end_date = datetime.datetime.strptime(end_date, self.dt_format)
        self.n_days = (self.end_date - self.start_date).days
        self.products = np.array(list(Params.products.keys()))
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

    def featurize(self, day_of_week, product, price, disp_prod_val, disp_val):
        x_day = self._day_of_week_features(day_of_week)
        x_product = self._product_features(product)
        x_price = x_product*price

        return np.concatenate([x_day, x_product, x_price, disp_prod_val, [disp_val]])

    def _stringify_list(self, l):
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
                product_disp_set, one_hot = self.prior.gen_product_set(self.products)
                prod_disp_val = self.prior.gen_display_prod_value(one_hot)
                disp_spatial_val = self.prior.spatial_effects[d]
                for p in product_disp_set:
                    x_t = self.featurize(
                        day_of_week=day.weekday(),
                        product=p,
                        price=prices[p],
                        disp_prod_val=prod_disp_val,
                        disp_val=disp_spatial_val
                    )
                    q, lmbda = self.prior.gen_quantity(x_t)
                    self.buffer.add(
                        (
                            q,
                            day,
                            p,
                            d,
                            prices[p],
                            self._stringify_list(product_disp_set)
                        )
                    )
        self.buffer.to_csv("output.csv")

if __name__ == "__main__":
    sim = Simulator(3, "2021-01-01", "2021-01-31")
    sim.main()