from ..bin.network import NeuralNetwork
from ..bin.displayer import Displayer

class CanvasTest:
    def create_oval(self, *args, **kargs):
        assert kargs["fill"] is None

class GraphicsTest:
    def __init__(self, displayer):
        self.displayer = displayer

    def getCanvas(self):
        return CanvasTest


def test_passing_graphics():
    neu_network = NeuralNetwork()

    n1 = neu_network.neuron()

    displayer = Displayer(neu_network, graphics=GraphicsTest)

    assert displayer.graphics.displayer is displayer

def test_adding_neurons():
    neu_network = NeuralNetwork()

    n1 = neu_network.neuron()

    displayer = Displayer(neu_network, graphics=GraphicsTest)

    assert len(displayer.neurons) == 1

    n2 = neu_network.neuron()
    n3 = neu_network.neuron()

    assert len(displayer.neurons) == 3

def test_start_animation():
    pass

def test_stop_animation():
    pass

def test_change_animation_rate():
    pass