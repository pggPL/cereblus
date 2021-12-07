class Event:
    def __init__(self, time, activation_function):
        self.time = time
        self.on_activation = activation_function

    def __eq__(self, other):
        return self.time == other.time

    def __le__(self, other):
        return self.time <= other.time

    def __ge__(self, other):
        return self.time >= other.time

    def __gt__(self, other):
        return self.time > other.time

    def __lt__(self, other):
        return self.time < other.time

    def happen(self):
        self.on_activation()