

class Buffer(object):

    def __init__(self):
        self.data = []
        self.headers = [
            "Quantity_Sold",
            "Display_Name",
            "Region_Name",
            "Before_Restock",
            "After_Restock"
        ]

    def get_tuple(self, ts, rewards, state, action):
        """
            Translate the reward, state, and action dicts into a tuple to add to the buffer

        :param ts: (Datetime) timestamp
        :param rewards: List[Dict]: list of reward dictionaries
        :param state: (Dict) state dict of store
        :param action: (Dict) Action dict
        :return:
        """
        # TODO: Implement this function to transform into a tuple
        return None

    def add(self, tup):
        self.data.append(tup)

    def add(self, q_sold, display_name, region_name, before_restock, after_restock):
        self.data.append((q_sold, display_name, region_name, before_restock, after_restock))

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