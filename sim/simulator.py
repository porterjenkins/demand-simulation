import os
import sys

path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

import gym
import numpy as np
import datetime
import yaml
from sim import cfg

from store import Store
from prior import Prior, Params, DisplayLocations
from buffer import Buffer
from agent import Agent
from display import CoolerDisplay

from visualizer import plt_cumulative_rewards

# Original:
# from sim.store import Store
# from sim.prior import Prior, Params, DisplayLocations
# from buffer import Buffer
# from sim.agent import Agent
# from sim.display import CoolerDisplay

# from visualizer import plt_cumulative_rewards

class Simulator(gym.Env):
    dt_format = "%Y-%m-%d"

    def __init__(self, start_dt, end_dt, store, verbose=False):

        self.start_dt = start_dt
        self.end_dt = end_dt
        self.store = store
        self.timedelta = datetime.timedelta(
            hours=cfg.get_timedelta()
        )
        self.verbose = verbose



        self.buffer = Buffer()

    def _day_of_week_features(self, day):
        x = np.zeros(7)
        x[day] = 1.0
        return x


    def _stringify_list(self, l):
        l = [str(x) for x in l]
        s = ",".join(l)
        return "{" + s + "}"



    def step(self, ts, action=None):
        # existing agents make choices
        rewards = self.store.shop_agents(self.verbose)
        # agents move across store
        self.store.move_agents()
        obs = self.store

        # additional agents enter
        agents = Agent.gen_agents(ts)
        self.store.get_enter_agents(agents)

        return obs, rewards, False, {}


    def main(self, recommender=None):
        curr_time = self.start_dt
        step_cntr = 0
        eps_rewards = {}

        while curr_time < self.end_dt:

            print(f"Simulating step: {step_cntr}, {curr_time}")
            # TODO: Insert action logic here

            self.store.print_state()
            obs, rewards, _, _ = self.step(curr_time)
            if self.verbose:
                print("Sold:", rewards)

            eps_rewards = self.increment_rewards(eps_rewards, rewards)

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

            curr_time += self.timedelta
            step_cntr += 1
        #self.buffer.to_csv("output.csv")
        plt_cumulative_rewards(eps_rewards, show=True)



    @staticmethod
    def increment_rewards(agg, new):
        if not agg:
            agg = {}

        for k, v in new.items():
            if k not in agg:
                agg[k] = []
            else:
                agg[k].append(v)

        return agg


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

        ts = cfg.get_start_time()
        agents = Agent.gen_agents(ts)

        store.get_enter_agents(agents)

        sim = Simulator(
            start_dt=cfg.get_start_time(),
            end_dt=cfg.get_end_time(),
            store=store
        )

        return sim



if __name__ == "__main__":
    sim = Simulator.build_sim()

    sim.main()