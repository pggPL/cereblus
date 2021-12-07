import math


class Pixel:
    def __init__(self, parent_stimulation):
        self.parent_stimulation = parent_stimulation
        self.phases = []
        self.all_phrases_time = 0

    def add_phase(self, duration, state):
        self.phases.append((duration, state))
        self.all_phrases_time += duration

    def get(self, time):
        if self.all_phrases_time == 0:
            return False
        if time < 0:
            assert False
        if self.all_phrases_time < time and not self.parent_stimulation.loop:
            return False
        time = time - math.floor(time / self.all_phrases_time) * self.all_phrases_time
        for duration, state in self.phases:
            if time <= duration:
                return state
            else:
                time -= duration
        assert False
        return False