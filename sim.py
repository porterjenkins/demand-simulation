import numpy as np
import datetime

from prior import Prior

class Simulator(object):
    dt_format = "%Y-%m-%d"

    def __init__(self, n_displays, start_date, end_date):
        self.n_displays = n_displays
        self.start_date = datetime.datetime.strptime(start_date, self.dt_format)
        self.end_date = datetime.datetime.strptime(end_date, self.dt_format)
        self.n_days = (self.end_date - self.start_date).days

        self.prior = Prior()

    def _day_of_week_features(self, day):
        x = np.zeros(7)
        x[day] = 1.0
        return x


    def featurize(self, day_of_week):
        x = self._day_of_week_features(day_of_week)
        return x


    def main(self):

        for t in range(self.n_days):
            day = self.start_date + datetime.timedelta(days=t)
            x_t = self.featurize(day.weekday())
            q = self.prior.get_quantity(x_t)
            print(day, day.weekday())

if __name__ == "__main__":
    sim = Simulator(3, "2021-01-01", "2021-01-31")
    sim.main()