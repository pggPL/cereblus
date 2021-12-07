from ..neuron import Neuron
from ..neurons.receptor import Receptor
from ..network import NeuralNetwork


class LateralInhibitionNetwork(NeuralNetwork):
    def __init__(self):
        super(LateralInhibitionNetwork, self).__init__()

        self.time_delay = 0.01

        self.number_of_neurons = 32

        self.neurons_receptors = []
        self.neurons_bipolar = []
        self.neurons_ganglion = []

        self.center_power = 0.4
        self.inhibition_power = -0.07
        self.inhibition_width = 4

        self.neurons_receptors = list(map(
            (lambda i: self.neuron(template=Receptor, pos=(0, 15 * i, 0))),
            list(range(self.number_of_neurons))
        ))
        self.neurons_bipolar = list(map(
            (lambda i: self.neuron(pos=(50, 15 * i, 0))),
            list(range(self.number_of_neurons))
        ))
        self.neurons_ganglion = list(map(
            (lambda i: self.neuron(pos=(100, 15 * i, 0))),
            list(range(self.number_of_neurons))
        ))
        self.next_rows = list(map(
            (lambda j:
             list(map(
                 (lambda i: self.neuron(pos=(100 + 50 * (j + 1), 15 * i, 0))),
                 list(range(self.number_of_neurons))
             ))
             ),
            list(range(17))
        ))

        for i in range(self.number_of_neurons):
            self.neurons_receptors[i].connect(self.neurons_bipolar[i], 1)
            self.neurons_bipolar[i].connect(self.neurons_ganglion[i], self.center_power)

            if i > 1:
                for x in self.neurons_ganglion[max(0, i - self.inhibition_width):i]:
                    self.neurons_bipolar[i].connect(x, self.inhibition_power)

            if i < self.number_of_neurons:
                for x in self.neurons_ganglion[(i + 1):min(self.number_of_neurons, i + self.inhibition_width + 1)]:
                    self.neurons_bipolar[i].connect(x, self.inhibition_power)

        for neu_ind in range(len(self.next_rows[0])):
            self.neurons_ganglion[neu_ind].connect(self.next_rows[0][neu_ind], coeff=10)

        for row_ind in range(len(self.next_rows) - 1):
            for neu_ind in range(len(self.next_rows[row_ind])):
                self.next_rows[row_ind][neu_ind].connect(self.next_rows[row_ind + 1][neu_ind], 1.6)
