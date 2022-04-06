from sim import cfg

class Buffer(object):

    def __init__(self):
        self.data = []
        self.headers = [
            "datetime",
            "product",
            "display",
            "num_slots",
            "quantity_sold",
            "price",
            "revenue"
        ]

    @staticmethod
    def get_sum_rewards(rewards):
        """

        :param rewards: (Dict)
        :return:
        """
        output = {}
        for r in rewards:
            for disp, vals in r.items():
                if disp not in output:
                    output[disp] = {}
                for prod, obs in vals.items():
                    if prod not in output[disp]:
                        output[disp][prod] = {}
                    for k, v in obs.items():
                        if isinstance(v, str):
                            output[disp][prod][k] = v
                        else:
                            if k not in output[disp][prod]:
                                output[disp][prod][k] = 0.0
                            output[disp][prod][k] += v

        return output


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


    def get_tuple(self, ts, rewards, state):
        """
            Translate the reward, state, and action dicts into a tuple to add to the buffer

        :param ts: (Datetime) timestamp
        :param rewards: List[Dict]: list of reward dictionaries
        :param state: (Dict) state dict of store
        :return:
        """

        rewards = self.get_sum_rewards(rewards)
        slots = self.get_sum_slots(state)

        tup_list = []

        for disp, rew_dict in rewards.items():
            dis_slots = slots[disp]
            for prod, cnt in dis_slots.items():
                r = rew_dict.get(
                    prod,
                    {
                        "q_sold": 0,
                        "total_sales": 0
                    }
                )
                price = cfg.get_price_by_product(prod)
                t = [
                    str(ts),
                    prod,
                    disp,
                    cnt,
                    r['q_sold'],
                    price,
                    r['total_sales']
                ]
                tup_list.append(t)

        return tup_list

    def add(self, tup):
        if isinstance(tup, list):
            for t in tup:
                self.data.append(t)
        else:
            self.data.append(tup)

    def to_csv(self, fname, headers=True):
        with open(fname, "w") as stream:
            if headers:
                line = '","'.join(self.headers)
                line = f'"{line}"\n'
                stream.write(line)
            for row in self.data:
                row = [str(x) for x in row]
                line = '","'.join(row)
                line = f'"{line}"\n'
                stream.write(line)