from ..neuron import Neuron
from ..network import NeuralNetwork
from ..neurons.receptor import Receptor

class Network1(NeuralNetwork):
    def __init__(self):
        super(Network1, self).__init__()

        # five columns of 20 neurons
        self.time_delay = 0.03

        cols = 5
        in_row = 20

        prev_col = []
        cur_col = []

        for c in range(cols):
            for r in range(in_row):
                neuron = self.neuron(template=Neuron, pos=(30 * c + 20, 20 * r + 20, 0))
                cur_col.append(neuron)
                for x in prev_col[(max(r - 3, 0)):(min(r + 3, in_row))]:
                    neuron.connect(x, 0.3)
            prev_col = cur_col
            cur_col = []


        # receptors

        self.receptors = []
        self.__last_time_stimulated__ = -1

        for r in range(10):
            rec = self.neuron(template=Receptor, pos=(30 * cols + 20, 40 * r + 30, 0))
            self.stimulate(neuron=rec, time_start=0, time_end=5, voltage=2, interval=2)
            self.receptors.append(rec)
            for x in prev_col[(max(2 * r - 4, 0)):(min(2 * r, 19))]:
                pass
                rec.connect(x, -0.05)
            for x in prev_col[(max(2 * r + 1, 0)):(min(2 * r + 4, 19))]:
                pass
                rec.connect(x, -0.05)
            rec.connect(prev_col[2 * r], 0.2)
