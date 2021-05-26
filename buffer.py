

class Buffer(object):

    def __init__(self):
        self.data = []
        self.headers = [
            "quantity",
            "day",
            "product",
            "display_id",
            "price",
            "products_on_display"
        ]


    def add(self, tup):
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