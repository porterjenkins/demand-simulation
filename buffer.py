

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