import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from sim import cfg
from sim.agent import Agent


class Region(object):
    def __init__(self, name, trans_probs, idx, displays, is_entrance=False):
        self.name = name
        self.trans_probs = trans_probs
        self.displays = displays
        self.idx = idx
        self.is_entrance = is_entrance

    def __str__(self):
        return self.name

    def add_display(self, disp):
        self.displays.append(disp)

    def get_displays(self):
        return self.displays


class Store(object):

    def __init__(self, adj_mtx, trans_mtx, region_dict):
        self.adj_mtx = np.array(adj_mtx)
        self.trans_mtx = np.array(trans_mtx)
        self.names = list(region_dict.keys())
        self.trans_mtx = self.norm_trans_mtx(self.adj_mtx, self.trans_mtx)
        self.ent_reg = None
        self.regions = self.build_regions(region_dict)
        self.agents = {}



    def build_regions(self, region_dict):
        """

        :return: (dict) regions dict with name as key, Region object as value
        """

        regions = {}
        i = 0
        for name, r_data in region_dict.items():
            is_entrance = r_data.get("is_entrance", False)
            if is_entrance:
                self.ent_reg = name

            r_idx = cfg.reg2idx[name]
            reg = Region(
                name=name,
                trans_probs=self.trans_mtx[r_idx, :],
                is_entrance=is_entrance,
                idx=r_idx,
                displays=[]
            )
            regions[name] = reg
            i += 1

        return regions

    def add_displays_to_regions(self, disp_list):
        for disp in disp_list:
            reg = self.regions[disp.region]
            reg.add_display(disp)

    def add_agent(self, agent):
        self.agents[agent.name] = agent

    def get_num_agents(self):
        return len(self.agents)

    def get_enter_agents(self, agents):
        """

        :param agents: List[Agent]
        :return: None"""

        for name, a in agents.items():
            a.update_loc(self.ent_reg)
            self.add_agent(a)



    def print_state(self):
        reg_cntr = dict(zip(list(self.regions.keys()), [0]*len(self.regions)))
        for a_name, a in self.agents.items():
            reg_cntr[a.curr_loc] += 1
        for reg, cnt in reg_cntr.items():
            bar = "".join(["X"]*cnt)
            print(f"\t{reg}: {bar}")


    def move_agents(self):
        d = {}
        for a_name, agent in self.agents.items():
            probs = self.regions[agent.curr_loc].trans_probs
            prev_loc = agent.curr_loc
            new_loc = agent.action_move(probs)

            is_exit = Agent.exit_rm_agent(
                agent=agent,
                curr_region=self.regions[new_loc],
                prev_loc=prev_loc
            )

            if is_exit:
               del agent
            else:
                d[a_name] = agent

        self.agents = d

    def shop_agents(self, verbose=False):
        rewards = {}

        for a_name, agent in self.agents.items():
            reg = self.regions[agent.curr_loc]
            displays = reg.get_displays()
            d_idx = np.random.randint(len(displays))

            disp = displays[d_idx]
            state_mtx, names = disp.get_state_mtx()

            if state_mtx.size > 0:
                action = agent.action_select(state_mtx, names)
                disp.decrement(action)
                price = cfg.get_price_by_product(action)
                #rewards[disp.name][action] += price
                if disp.name not in rewards:
                    rewards[disp.name] = {}
                if action not in rewards[disp.name]:
                    rewards[disp.name][action] = 0

                rewards[disp.name][action] += price




            if verbose:
                disp.print_state()


        return rewards

    def get_state_dict(self):
        state = {}
        for r_name, reg in self.regions.items():
            for d in reg.displays:
                inv = d.get_slot_counts()
                state[d.name] = inv

        return state


    @staticmethod
    def norm_trans_mtx(adj_mtx, trans_mtx):

        trans_mtx = trans_mtx * adj_mtx
        normed_mtx = trans_mtx / trans_mtx.sum(axis=1).reshape(-1, 1)

        return normed_mtx