from ..neuron import Neuron
from ..event import Event

class Receptor(Neuron):
    def __init__(self, pos, network, resolution=0.01):
        super(Receptor, self).__init__(pos, network)
        self.resolution = resolution
        self.stimuli = []

        start_event = Event(0, self.affect_by_stimulus)
        self.network.append_event(start_event)

    def connect_to_stimulus(self, pixel):
        self.stimuli.append(pixel)

    def affect_by_stimulus(self):
        event = Event(self.network.time + self.resolution, self.affect_by_stimulus)
        self.network.append_event(event)
        for s in self.stimuli:
            if s.get(self.network.time):
                self.activate()
                return