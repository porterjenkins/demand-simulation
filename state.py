from sim import cfg

class State(object):


    def __init__(self, disp, slot_cnts):
        self.disp = disp
        self.slot_cnts = slot_cnts

    def get_slot_dict(self):
        return self.slot_cnts

    def __str__(self):
        return f"{self.disp}"

    @staticmethod
    def get_sum_slots(state):
        """

        :param state: (Dic)
        :return:
        """
        output = {}

        for disp, cnts in state.items():
            output[disp] = {}
            for idx, tup in cnts.items():
                if tup[0] not in output[disp]:
                    output[disp][tup[0]] = 0
                output[disp][tup[0]] += 1
        return output

    @classmethod
    def fromdict(cls, state_dict):

        """

        :param state_dict: (Dict) state dictionary
        :return: (Dict) keys: display names, values: State objects
        """
        output = {}
        slot_cnts = cls.get_sum_slots(state_dict)
        for disp, cnts in slot_cnts.items():
            state = State(disp, slot_cnts=cnts)
            output[disp] = state

        return output

