

class Buffer(object):

    def __init__(self):
        self.data = []


    def add(self, tup):
        self.data.append(tup)

    def to_csv(self, fname):
        with open(fname, "w") as stream:
            for row in self.data:
                row = [str(x) for x in row]
                line = '","'.join(row)
                line = f'"{line}"\n'
                stream.write(line)