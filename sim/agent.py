import numpy as np

from sim import cfg

from prior import Prior
from sim_utils import softmax
from uuid import uuid4

class Agent(object):
    def __init__(self, params):
        self.params = params
        self.id = uuid4()

    def __str__(self):
        return str(self.id)

    def action_select(self, state_mtx):
        """

        :param state_mtx: n x (n x 1), where n is the number of products
        :return:
        """
        names = cfg.get_products()
        logits = state_mtx @ self.params
        probs = softmax(logits)
        choice = np.random.choice(
            np.arange(probs.shape[0]),
            1,
            p=probs
        )

        choice = names[choice[0]]
        return choice

    def action_move(self):
        pass


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

        agents = []
        for p in ind_params:
            agent = Agent(p)
            agents.append(agent)

        return agents