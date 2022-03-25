import gym
import numpy as np
import datetime
import yaml

from sim import cfg

from sim.store import Store
from sim.prior import Prior, Params, DisplayLocations
from sim.agent import Agent
from sim.display import CoolerDisplay
from sim.rewards import Rewards

from buffer import Buffer


from visualizer import plt_cumulative_rewards, plot_traffic

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
        self.rewards = Rewards(
            displays=cfg.get_display_names(),
            products=cfg.get_product_names()
        )

        self.curr_time = self.start_dt
        self.stepsize = cfg.get_step_size()
        self.traffic = []
        self.ts = []



        self.buffer = Buffer()

    def _day_of_week_features(self, day):
        x = np.zeros(7)
        x[day] = 1.0
        return x


    def _stringify_list(self, l):
        l = [str(x) for x in l]
        s = ",".join(l)
        return "{" + s + "}"



    def step(self, action=None):

        state = None
        rewards = None

        for ts in range(self.stepsize):
            self.store.print_state()
            self.traffic.append(self.store.get_n_agents())
            self.ts.append(self.curr_time)


            # existing agents make choices
            rewards = self.store.shop_agents(self.verbose)

            # agents move across store
            self.store.move_agents(self.curr_time)

            # get state
            state = self.store.get_state_dict()
            # calculate rewards
            self.rewards.increment(rewards)

            # additional agents enter
            agents = Agent.gen_agents(self.curr_time)
            self.store.get_enter_agents(agents)

            self.curr_time += self.timedelta

        if self.curr_time > self.end_dt:
            done = True
        else:
            done = False

        return state, rewards, done, {}


    def main(self, recommender=None):

        step_cntr = 0
        eps_rewards = {}
        done = False

        while not done:

            print(f"Simulating step: {step_cntr}, {self.curr_time}")
            # TODO: Insert action logic here


            obs, rewards, done, info = self.step()
            if self.verbose:
                print("Sold:", rewards)


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
            step_cntr += 1

            CoolerDisplay._restock_coolers()

        #self.buffer.to_csv("output.csv")
        plt_cumulative_rewards(self.rewards.todict(), show=True)
        plot_traffic(self.ts, self.traffic, show=True)




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