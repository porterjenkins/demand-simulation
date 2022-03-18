from sim import cfg
import numpy as np

class Region(object):
    def __init__(self, name, trans_probs, idx, displays=[], is_entrance=False):
        self.name = name
        self.trans_probs = trans_probs
        self.displays = displays
        self.idx = idx
        self.is_entrance = is_entrance

    def __str__(self):
        return self.name

    def add_display(self, disp):
        self.displays.append(disp)


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
                idx=r_idx
            )
            regions[name] = reg
            i += 1

        return regions

    def add_displays_to_regions(self, disp_list):
        for disp in disp_list:
            self.regions[disp.region].add_display(disp)

    def add_agent(self, agent):
        self.agents[agent.name] = agent

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




    @staticmethod
    def norm_trans_mtx(adj_mtx, trans_mtx):

        trans_mtx = trans_mtx * adj_mtx
        normed_mtx = trans_mtx / trans_mtx.sum(axis=1).reshape(-1, 1)

        return normed_mtx