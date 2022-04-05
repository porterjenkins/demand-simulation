

class Buffer(object):

    def __init__(self):
        self.data = []
        self.headers = [
            "datetime",
            "quantity_sold",
            "num_slots",
            "product",
            "price",
            "revenue",
            "region",
            "display"
        ]

    def get_tuple(self, ts, rewards, state):
        """
            Translate the reward, state, and action dicts into a tuple to add to the buffer

        :param ts: (Datetime) timestamp
        :param rewards: List[Dict]: list of reward dictionaries
        :param state: (Dict) state dict of store
        :return:
        """
        # TODO: Implement this function to transform into a tuple
        return None

    def add(self, tup):
        self.data.append(tup)

    def add(self, datetime, quantity_sold, num_slots, product, price, revenue, region, display):
        self.data.append((datetime, quantity_sold, num_slots, product, price, revenue, region, display))

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