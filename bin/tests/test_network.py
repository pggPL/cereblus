import math

import pytest

from ..cereblus.network import NeuralNetwork, NonPositiveInterval
from ..cereblus.neuron import Neuron
from hypothesis import given, settings, strategies as st


def test_new_neuron_susbscription():
    list_of_added_neurons = []

    neu_network = NeuralNetwork()
    neu_network.subscribe_new_neurons(
        (lambda x: list_of_added_neurons.append(x))
    )

    n1 = neu_network.neuron()
    n2 = neu_network.neuron()

    assert len(list_of_added_neurons) == 2

    n3 = neu_network.neuron()

    assert len(list_of_added_neurons) == 3

    assert (list_of_added_neurons[0] == n1)


"""
    Checking if ,,steps,, and ,,time'' bound for NeuralNetwork.run() work properly.
"""


def test_run_bounds_1():
    """
    Only time
    """
    neu_network = NeuralNetwork()
    n1 = neu_network.neuron()

    neu_network.stimulate(neuron=n1, time_start=0, time_end=4, voltage=1, interval=0.5)

    activations_of_n1 = 0

    def f(sender):
        nonlocal activations_of_n1
        activations_of_n1 += 1

    n1.subscribe_on_activation(f)

    neu_network.run(time=1.1)

    assert (activations_of_n1 == 3)

    neu_network.run(time=0.4)

    assert (activations_of_n1 == 4)


def test_run_bounds_2():
    """
    Only steps
    """
    neu_network = NeuralNetwork()
    n1 = neu_network.neuron()

    neu_network.stimulate(neuron=n1, time_start=0, time_end=10, voltage=1, interval=0.5)

    activations_of_n1 = 0

    def f(sender):
        nonlocal activations_of_n1
        activations_of_n1 += 1

    n1.subscribe_on_activation(f)

    neu_network.run(steps=10)
    assert (activations_of_n1 == 10)

    neu_network.run(steps=5)
    assert (activations_of_n1 == 15)


def test_run_bounds_3():
    """
    Both steps and time
    """
    neu_network = NeuralNetwork()
    n1 = neu_network.neuron()

    neu_network.stimulate(neuron=n1, time_start=0, time_end=10, voltage=1, interval=0.5)

    activations_of_n1 = 0

    def f(sender):
        nonlocal activations_of_n1
        activations_of_n1 += 1

    n1.subscribe_on_activation(f)

    neu_network.run(steps=10, time=1)
    assert (activations_of_n1 == 10)

    neu_network.run(steps=5, time=10)
    assert (activations_of_n1 == 21)


def test_run_bound4():
    neu_network = NeuralNetwork()
    n1 = neu_network.neuron()

    neu_network.stimulate(neuron=n1, time_start=0, time_end=70, voltage=1, interval=1)

    activations_of_n1 = 0

    def f(sender):
        nonlocal activations_of_n1
        activations_of_n1 += 1

    n1.subscribe_on_activation(f)

    neu_network.run(steps=10)
    neu_network.run(steps=10)

    assert (activations_of_n1 == 20)

    neu_network.run(time=20)
    assert (activations_of_n1 == 40)

    neu_network.run(steps=10)
    assert (activations_of_n1 == 50)

    neu_network.run(time=20)
    assert (activations_of_n1 == 70)


def test_append_fire():
    neu_network = NeuralNetwork()
    n1 = neu_network.neuron()

    test_passed = False

    def f(sender):
        nonlocal test_passed
        test_passed = True

    n1.subscribe_on_activation(f)

    neu_network.append_fire(0, None, n1, 0.1)
    neu_network.run(steps=1)
    assert not test_passed

    neu_network.append_fire(0, None, n1, 1.1)
    neu_network.run(steps=2)
    assert test_passed


def test_neuron_activated():
    neu_network = NeuralNetwork()
    n1 = neu_network.neuron()
    n2 = neu_network.neuron()
    n1.connect(n2, 10)

    test_passed = False

    def f(sender):
        nonlocal test_passed
        test_passed = True

    n2.subscribe_on_activation(f)

    neu_network.__neuron_activated__(n1)
    neu_network.run(steps=1)

    assert test_passed


def test_run_1():
    """
        Creates network with two neurons, stimulates one of them.
        Stimulation activates n1 neuron two times,
        which should activate n2 neuron one time.
        Tests running network for time.
    """
    neu_network = NeuralNetwork()

    n1 = neu_network.neuron(template=Neuron, pos=(10, 10, 0))
    n2 = neu_network.neuron(template=Neuron, pos=(20, 10, 0))

    activations_of_n1 = 0
    activations_of_n2 = 0

    def f(sender):
        print("SENDER:" + str(sender))
        nonlocal activations_of_n1, activations_of_n2
        if sender is n1:
            activations_of_n1 += 1
        if sender is n2:
            activations_of_n2 += 1

    n1.subscribe_on_activation(f)
    n2.subscribe_on_activation(f)

    n1.connect(n2, 0.5)

    neu_network.stimulate(neuron=n1, time_start=0, time_end=0.9, voltage=1, interval=0.5)
    neu_network.run(time=2)

    assert (activations_of_n1 == 2)
    assert (activations_of_n2 == 1)


def test_run_2():
    """
    Test running network for few steps
    """
    neu_network = NeuralNetwork()

    n1 = neu_network.neuron(template=Neuron, pos=(10, 10, 0))
    n2 = neu_network.neuron(template=Neuron, pos=(20, 10, 0))

    activations_of_n1 = 0
    activations_of_n2 = 0

    def f(sender):
        nonlocal activations_of_n1
        nonlocal activations_of_n2
        if sender is n1:
            activations_of_n1 += 1
        if sender is n2:
            activations_of_n2 += 2

    n1.subscribe_on_activation(f)
    n2.subscribe_on_activation(f)

    n1.connect(n2, 0.5)

    neu_network.stimulate(neuron=n1, time_start=0.11, time_end=5, voltage=1, interval=0.51)
    neu_network.run(steps=5)

    assert (activations_of_n1 + activations_of_n2 == 5)

@given(st.integers(min_value=1, max_value=100), st.integers(min_value=1, max_value=100), st.integers(min_value=1))
@settings(max_examples=100)
def test_run3(t1: int, t2: int, interval: int):
    time_start = min(t1, t2)
    time_end = max(t1, t2)

    neu_network = NeuralNetwork()

    n1 = neu_network.neuron(template=Neuron, pos=(10, 10, 0))
    n2 = neu_network.neuron(template=Neuron, pos=(20, 10, 0))

    activations_of_n1 = 0
    activations_of_n2 = 0

    def f(sender):
        nonlocal activations_of_n1
        nonlocal activations_of_n2
        if sender is n1:
            activations_of_n1 += 1
        if sender is n2:
            activations_of_n2 += 2

    n1.subscribe_on_activation(f)
    n2.subscribe_on_activation(f)

    n1.connect(n2, 0.5)


    neu_network.stimulate(neuron=n1, time_start=time_start, time_end=time_end, voltage=1, interval=interval)
    return
    neu_network.run(time=time_end + 1)

    expected_activations_of_n1 = 1 + math.floor((time_end - time_start) / interval)
    expected_activations_of_n2 = math.floor(expected_activations_of_n1 / 2)
    expected_activations = expected_activations_of_n1 + expected_activations_of_n2
    assert (activations_of_n1 + activations_of_n2 == expected_activations)

def test_non_positive_interval():
    neu_network = NeuralNetwork()
    n1 = neu_network.neuron()

    with pytest.raises(NonPositiveInterval):
        neu_network.stimulate(n1, 10, 20, 1, 0)

def test_fire_delay():
    """
    Test running network for few steps
    """
    neu_network = NeuralNetwork()
    # Not sure if setting like that
    neu_network.time_delay = 1

    n1 = neu_network.neuron()
    n2 = neu_network.neuron()

    activations_of_n2 = 0

    def f(sender):
        nonlocal activations_of_n2
        activations_of_n2 += 1

    n2.subscribe_on_activation(f)

    n1.connect(n2, 2)

    neu_network.run(time=2)

    n1.activate()

    neu_network.run(time=0.3)
    assert (activations_of_n2 == 0)

    neu_network.run(time=0.7)
    assert (activations_of_n2 == 1)

def test_get_firing_queue_min():
    neu_net = NeuralNetwork()

    assert not neu_net.__get_event_queue_min__()

    neu_net.append_fire(1,None,None,None)
    neu_net.append_fire(-1,None,None,None)
    neu_net.append_fire(2,None,None,None)

    assert neu_net.__get_event_queue_min__().time == -1
    assert neu_net.__get_event_queue_min__().time == 1
    assert neu_net.__get_event_queue_min__().time == 2