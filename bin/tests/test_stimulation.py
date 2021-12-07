from bin.cereblus.network import NeuralNetwork
from ..cereblus.neuron import Neuron
from ..cereblus.stimulation import Stimulation, StimulationLoader, WrongImageLength, NeuronNotReceptive
from ..cereblus.neurons.receptor import Receptor

import pytest

def vision():
    neu_net = NeuralNetwork()
    n1 = neu_net.neuron()
    n2 = neu_net.neuron()
    n3 = neu_net.neuron()

    # list with Stimulation objects
    all_stimulations = StimulationLoader.load_all_from_folder("folder_with_stimulations")
    s1 = all_stimulations[0]

    # no synchronization with network, cause the neuron which asks know the time

    # neuron reacts to stimuli, not reverse

    n1.connect_to_stimulus(s1.get_pixel(0))

    neu_net.run(steps=100)

def test_load_from_file():
    neu_net = NeuralNetwork()
    neurons = []
    for i in range(5):
        neurons.append(neu_net.neuron(template=Receptor))

    stimulation = StimulationLoader.load_from_file("./bin/tests/test_stimulations/test_stimulation1.json")

    for i in range(5):
        stimulation.connect(num_of_pixel=i, neuron=neurons[i])

    assert stimulation.loop

def test_create_manual():
    s1 = Stimulation(num_of_pixels=5)
    s1.add_phase("––OO–", duration=0.1)
    s1.add_phase( "–OOO–", duration=0.1)
    s1.add_phase("OOOO–", duration=0.1)
    s1.loop = True


def test_one_neuron_connection():
    s1 = Stimulation(num_of_pixels=5)
    s1.add_phase("––OO–", duration=0.1)
    s1.add_phase( "–OOO–", duration=0.1)
    s1.add_phase("OOOO–", duration=0.1)
    s1.loop = True

    neu_net = NeuralNetwork()
    n1 = neu_net.neuron(template=Receptor)

    activations_of_n1 = 0

    def f(sender):
        nonlocal activations_of_n1
        activations_of_n1 += 1

    n1.subscribe_on_activation(f)

    s1.connect(num_of_pixel=0, neuron=n1)

    neu_net.run(time=0.1)
    assert activations_of_n1 == 0
    neu_net.run(time=0.1)
    assert activations_of_n1 == 0
    neu_net.run(time=0.1)

    # flaws of floating point
    assert (activations_of_n1 == 11 or activations_of_n1 == 10)


def test_too_long_phase():
    with pytest.raises(WrongImageLength):
        stimulation = StimulationLoader.load_from_file("./bin/tests/test_stimulations/test_stimulation2.json")


def test_connecting_non_receptive_neuron():
    s1 = Stimulation(num_of_pixels=5)
    neu_net = NeuralNetwork()
    n1 = neu_net.neuron(template=Neuron)

    with pytest.raises(NeuronNotReceptive):
        s1.connect(s1, 0)
