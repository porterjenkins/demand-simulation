

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




    def get_tuple(self, ts, rewards, state):
        """
            Translate the reward, state, and action dicts into a tuple to add to the buffer

        :param ts: (Datetime) timestamp
        :param rewards: List[Dict]: list of reward dictionaries
        :param state: (Dict) state dict of store
        :return:
        """
        # TODO: Implement this function to transform into a tuple

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

        self.get_sum_rewards(rewards)

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