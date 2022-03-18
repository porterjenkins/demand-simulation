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

    def __init__(self, start_dt, end_dt, store):

        self.start_dt = start_dt
        self.end_dt = end_dt
        self.store = store
        self.timedelta = datetime.timedelta(
            hours=cfg.get_timedelta()
        )


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
        # TODO
        for a_name, agent in self.store.agents.items():
            probs = self.store.regions[agent.curr_loc].trans_probs
            agent.action_move(probs)


    def main(self, recommender=None):
        curr_time = self.start_dt
        step_cntr = 0
        while curr_time < self.end_dt:

            print(f"Simulating step: {step_cntr}, {curr_time}")
            self.store.print_state()
            self.step()


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

            curr_time += self.timedelta
            step_cntr += 1
        #self.buffer.to_csv("output.csv")

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