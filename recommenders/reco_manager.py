

class RecommendationManager(object):

    def __init__(self, agents):
        """

        :param agents: (List) list of reco agents
        """
        self.agents = {}
        for a in agents:
            self.agents[a.disp] = a


    def __call__(self, states, *args, **kwargs):
        actions = []
        for disp, state in states.items():
            agent = self.agents[disp]
            a = agent(state)
            reg = disp.split("-")[0]
            act_dict = {
                "region": reg,
                "display": disp,
                "action": a
            }
            actions.append(act_dict)
        return actions
