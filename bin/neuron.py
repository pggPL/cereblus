# Base Neuron class

class AlreadyConnected(Exception):
    def __init__(self):
        super().__init__("Connected neuron to another neuron despite the connection already exist.")


class Neuron:
    def __init__(self, pos, network):
        self.position = pos
        self.network = network

        self.connections = []
        self.energy = 0
        self.activation_potential = 1

        self.__subscribers__ = []

    def is_connected_to(self, neuron):
        for pair in self.connections:
            n, _ = pair
            if n is neuron:
                return True
        return False

    def connect(self, neuron, coeff):
        # check if this neuron is already connected
        if self.is_connected_to(neuron):
            raise AlreadyConnected

        # if not, connect
        self.connections.append((neuron, coeff))

    def activate(self):
        self.energy = 0
        self.send_to_subscribers(self)

    def add_energy(self, sender, energy):

        self.energy += energy
        if self.energy < -0.1:
            self.energy = -0.1
        if self.energy >= self.activation_potential:
            #print("Neuron {} got {} energy and have now {}".format(self, energy, self.energy))
            self.activate()

    def subscribe_on_activation(self, f):
        self.__subscribers__.append(f)

    def send_to_subscribers(self, message):
        for f in self.__subscribers__:
            f(message)
