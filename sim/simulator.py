import gym
import numpy as np
import datetime
from uuid import uuid4
import os
import shutil

# from sim import cfg
# #from . import cfg
#
# from sim.store import Store
# from sim.prior import Prior, Params, DisplayLocations
# from sim.agent import Agent
# from sim.display import CoolerDisplay, Inventory
# from sim.rewards import Rewards

from sim import cfg
from sim.store import Store
from sim.agent import Agent
from sim.display import CoolerDisplay
from sim.rewards import Rewards
from sim.buffer import Buffer

from state import State
from recommenders import reco_manager

from visualizer import plt_cumulative_rewards, plot_traffic



class Simulator(gym.Env):
    dt_format = "%Y-%m-%d"
    runs_dir = './runs'

    def __init__(self, start_dt, end_dt, store, verbose=False):
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.store = store
        self.timedelta = datetime.timedelta(hours=cfg.get_timedelta())
        self.verbose = verbose
        self.rewards = Rewards(displays=cfg.get_display_names(),
                               products=cfg.get_product_names())

        self.curr_time = self.start_dt
        self.stepsize = cfg.get_step_size()
        self.traffic = []
        self.ts = []
        self.sim_id = str(uuid4())
        self.buffer = Buffer()
        self.output_dir = os.path.join(self.runs_dir, self.sim_id)
        if not os.path.exists(self.runs_dir):
            os.mkdir(self.runs_dir)
        os.mkdir(self.output_dir)
        shutil.copy(cfg.cfg_path, os.path.join(self.output_dir, "cfg.yaml"))

    def _day_of_week_features(self, day):
        x = np.zeros(7)
        x[day] = 1.0
        return x

    def _stringify_list(self, l):
        l = [str(x) for x in l]
        s = ",".join(l)
        return "{" + s + "}"


    def step(self, action=None):

        rewards = []


        for ts in range(self.stepsize):
            self.store.print_state()
            self.traffic.append(self.store.get_n_agents())
            self.ts.append(self.curr_time)

            # existing agents make choices
            rewards.append(self.store.shop_agents(self.verbose))

            # agents move across store
            self.store.move_agents(self.curr_time)

            # calculate rewards
            self.rewards.increment(rewards[-1])

            # additional agents enter
            agents = Agent.gen_agents(self.curr_time)
            self.store.get_enter_agents(agents)

            self.curr_time += self.timedelta

        if self.curr_time > self.end_dt:
            done = True
        else:
            done = False


        self.store.take_actions(actions=action, verbose=self.verbose)

        state = State.fromdict(
            self.store.get_state_dict()
        )

        return state, rewards, done, {}

    def main(self, reco_manager):
        """

        :param reco_manager: (RecommendationManager)
        :return:
        """
        step_cntr = 0
        eps_rewards = {}
        done = False

        state = State.fromdict(
            self.store.get_state_dict()
        )

        while not done:
            print(f"Simulating step: {step_cntr}, {self.curr_time}")
            obs_time = self.curr_time

            action = reco_manager(state)

            state, rewards, done, info = self.step(action)

            if self.verbose:
                print("Sold:", rewards)

            tup_list = self.buffer.get_tuple(obs_time, rewards, state)
            reco_manager.update(tup_list)
            self.buffer.add(tup_list)

            step_cntr += 1

        self.buffer.to_csv(os.path.join(self.output_dir, "output.csv"))
        self.rewards.save(os.path.join(self.output_dir, "rewards.json"))

        plt_cumulative_rewards(
            self.rewards.todict(),
            show=False,
            fname=os.path.join(self.output_dir, "rewards.png")
        )
        plot_traffic(
            self.ts,
            self.traffic,
            show=False,
            fname=os.path.join(self.output_dir, "traffic.png")
        )

    @classmethod
    def build_sim(cls):

        store = Store(adj_mtx=cfg.get_adj_mtx(),
                      trans_mtx=cfg.get_trans_mtx(),
                      region_dict=cfg.get_region_dict())

        displays = CoolerDisplay.build_displays_from_dict(
            cfg.get_region_dict())
        store.add_displays_to_regions(displays)

        ts = cfg.get_start_time()
        agents = Agent.gen_agents(ts)

        store.get_enter_agents(agents)

        sim = Simulator(start_dt=cfg.get_start_time(),
                        end_dt=cfg.get_end_time(),
                        store=store)

        return sim


if __name__ == "__main__":
    sim = Simulator.build_sim()

    from recommenders.rand_reco import RandomRecommender



    sim.main()