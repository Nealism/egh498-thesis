class Plotter():
    def __init__(self, names):
        self.data = {name:[] for name in names}

    def save_data(self, data):
        for d in data:
            self.data[d].append(data[d])

    def plot(self):
        print("Plotting")