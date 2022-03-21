import numpy as np

from sim import cfg

from prior import Prior
from sim_utils import softmax
from uuid import uuid4
import names

class Agent(object):

    weekday_params = {
        "a": 2.8,
        "b": 2.4,
        "c": 1.0,
        "d": 5.0
    }

    weekend_params = {
        "a": 2.8,
        "b": 2.4,
        "c": 1.0,
        "d": 10.0
    }

    def __init__(self, params):
        self.params = params
        self.id = uuid4()
        self.name = names.get_full_name()
        self.curr_loc = None

    def __str__(self):
        return str(self.name)

    def action_select(self, state_mtx):
        """

        :param state_mtx: n x (n x 1), where n is the number of products
        :return:
        """
        p_names = cfg.get_products()
        logits = state_mtx @ self.params
        probs = softmax(logits)
        choice = np.random.choice(
            np.arange(probs.shape[0]),
            1,
            p=probs
        )

        choice = p_names[choice[0]]
        return choice

    def update_loc(self, loc):
        self.curr_loc = loc

    def action_move(self, trans_probs):
        new_loc = self.gen_new_loc(trans_probs)
        self.update_loc(new_loc)
        return new_loc

    def gen_new_loc(self, trans_probs):
        idx = np.random.choice(
            np.arange(trans_probs.shape[0]),
            p=trans_probs,
            size=1
        )[0]

        return cfg.idx2reg[idx]


    @classmethod
    def build_agents(
            cls,
            n_agents,
            product_params,
            price_params,
            sigma
    ):
        glob_params = Prior.vectorize_params(product_params, price_params)
        ind_params = Prior.gen_ind_params(glob_params, sigma, n_agents)
        agents = {}
        for p in ind_params:
            agent = Agent(p)
            agents[agent.name] = agent

        return agents

    @classmethod
    def exit_rm_agent(cls, agent, curr_region, prev_loc):
        """
        Agent exits (is deleted) if he is in the entrance region, and chooses to "stay" in that region.
        :param agent: Agent object
        :param curr_region: Region object of current region
        :param prev_loc: (str) Name of previous region
        :return:
        """
        if curr_region.name == prev_loc and curr_region.is_entrance:
            print(f"{agent} exits")
            return True
        else:
            return False

    @classmethod
    def get_sinx(cls, x, a, b, c, d):
        """

        :param x: domain
        :param a: x-scaler
        :param b: shift x
        :param c: shift y
        :param d: y-scaler
        :return:
        """
        sin_x = np.sin(x / a + b) * d + c

        return sin_x

    @classmethod
    def get_temporal_lambda(cls, x, sin_x):
        fx = np.zeros_like(sin_x)
        for xi in x:
            if xi < 6:
                fx[xi] = 0
            else:
                fx[xi] = max(0, sin_x[xi])
        return fx


    @classmethod
    def gen_agents(cls, ts):
        """

        :param ts: (Datetime) time stamp
        :return: List[Agent] list of agent objects
        """

        day_of_week = ts.weekday()
        hour = ts.hour
        x = np.arange(24)

        if day_of_week < 5:
            sinx = cls.get_sinx(
                x=x,
                a=cls.weekday_params["a"],
                b=cls.weekday_params["b"],
                c=cls.weekday_params["c"],
                d=cls.weekday_params["d"]
            )
        else:
            sinx = cls.get_sinx(
                x=x,
                a=cls.weekend_params["a"],
                b=cls.weekend_params["b"],
                c=cls.weekend_params["c"],
                d=cls.weekend_params["d"]
            )

        lmbda = cls.get_temporal_lambda(x, sinx)
        n_agents = np.random.poisson(lmbda[hour])

        agents = Agent.build_agents(
            n_agents=n_agents,
            product_params=cfg.get_prod_weight(),
            price_params=cfg.get_price_param(),
            sigma=cfg.get_var_param()
        )

        return agents





if __name__ == "__main__":
    import datetime
    ts = datetime.datetime.now()


    agents = Agent.gen_agents(ts)