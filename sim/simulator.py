import gym
import numpy as np
import datetime
import yaml

# from sim import cfg
# #from . import cfg
#
# from sim.store import Store
# from sim.prior import Prior, Params, DisplayLocations
# from sim.agent import Agent
# from sim.display import CoolerDisplay, Inventory
# from sim.rewards import Rewards

from sim_cfg import SimCfg
cfg = SimCfg("./cfg.yaml")

from store import Store
from prior import Prior, Params, DisplayLocations
from agent import Agent
from display import CoolerDisplay, Inventory
from rewards import Rewards

from buffer import Buffer

from visualizer import plt_cumulative_rewards, plot_traffic

DEFAULT_ACTION = [{
    "region": "deli",
    "display": "deli-cooler",
    "action": {
        "coca_cola_20oz_bottle": 4,
        "dr_pepper_20oz_bottle": 0,
        "diet_coke_20oz_bottle": 0,
        "sprite_20oz_bottle": 0,
        "Monster_16oz_can": 4
    }
}, {
    "region": "entrance",
    "display": "entrance-cooler",
    "action": {
        "coca_cola_20oz_bottle": 4,
        "dr_pepper_20oz_bottle": 0,
        "diet_coke_20oz_bottle": 0,
        "sprite_20oz_bottle": 0,
        "Monster_16oz_can": 4
    }
}, {
    "region": "dairy",
    "display": "dairy-cooler",
    "action": {
        "coca_cola_20oz_bottle": 4,
        "dr_pepper_20oz_bottle": 0,
        "diet_coke_20oz_bottle": 0,
        "sprite_20oz_bottle": 0,
        "Monster_16oz_can": 4
    }
}]


class Simulator(gym.Env):
    dt_format = "%Y-%m-%d"

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

        rewards = []

        # get state
        state = self.store.get_state_dict()

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

        return state, rewards, done, {}

    def main(self, recommender=None):
        step_cntr = 0
        eps_rewards = {}
        done = False

        while not done:
            print(f"Simulating step: {step_cntr}, {self.curr_time}")
            obs_time = self.curr_time
            state_before = self.store.get_state_dict()
            state, rewards, done, info = self.step(DEFAULT_ACTION)

            if self.verbose:
                print("Sold:", rewards)

            # datetime, quantity_sold, num_slots, product, price, revenue, region, display
            # Loop over all regions
            totals = {
                "region": {
                    "display": {
                        "product": {
                            "name": "something",
                            "price": 0,
                            "slots": 0,
                            "total_sales": 0,
                            "q_sold": 0,
                        },
                    }
                }
            }
                        
            for reward in rewards:
                # Loop over all displays
                for display, products in reward.items():
                    # Loop over all products
                    for product_name, product in products.items():
                        region = product["region"]
                        # check for region key in map, make if not exists

                        # check for total[region][display], make if not exists

                        # check for product: make if not exists
                        prev_product = totals[region][display][product_name]
                        if prev_product is None:
                            totals[region][display][product_name] = {
                                "name": product_name,
                                "price": cfg.get_price_by_product(product_name), 
                                "slots": next(q for d, q in state_before[display].values() if d == product_name),
                                "total_sales": product["total_sales"],
                                "q_sold": product["q_sold"],
                            }
                        else:
                            q_sold = prev_product["q_sold"]
                            total_sales = prev_product["total_sales"]
                            prev_product["q_sold"] += q_sold
                            prev_product["total_sales"] += total_sales


                        # price = cfg.get_price_by_product(product_name)
                        # q_sold = product["q_sold"]
                        # total_sales = product["total_sales"]
                        # region = product["region"]
                        # slots = next(q for d, q in state_before[display].values() if d == product_name)
                        # # tup = (obs_time, q_sold, slots, product_name, price, total_sales, "region", display)
                        # # self.buffer.add(tup)
            
            # Loop through each product in totals and log
            self.buffer.add(obs_time, q_sold, slots, product_name, price, total_sales, region, display)
            
            # Main GOALS
            # make sure product logs are unique for every timestamp bucket
            # aggregate all product sales per display per region
                    
            step_cntr += 1

        self.buffer.to_csv("output.csv")
        plt_cumulative_rewards(self.rewards.todict(), show=True)
        plot_traffic(self.ts, self.traffic, show=True)

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

    sim.main()