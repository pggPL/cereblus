from ..bin.neuron import Neuron, AlreadyConnected
import pytest


def test_activation_subscription():
    n1 = Neuron((0, 0, 0), None)
    test_passed = False

    def f(x):
        nonlocal test_passed
        test_passed = True

    n1.subscribe_on_activation(f)
    n1.activate()
    assert test_passed


def test_duplicated_connection():
    n1 = Neuron((0, 0, 0), None)
    n2 = Neuron((0, 0, 0), None)

    n1.connect(n2, 0.5)
    with pytest.raises(AlreadyConnected):
        n1.connect(n2, 0.6)


def test_connect():
    """
        Checks working of get_connections()
    """
    n1 = Neuron((0,0,0), None)
    n2 = Neuron((0,0,0), None)
    n3 = Neuron((0,0,0), None)
    n4 = Neuron((0,0,0), None)
    n5 = Neuron((0,0,0), None)

    n2.connect(n4, 0.5)
    n1.connect(n5, -2)
    n3.connect(n1, 10)
    n3.connect(n2, -1)

    n1_connections = n1.connections
    n2_connections = n2.connections
    n3_connections = n3.connections
    n4_connections = n4.connections
    n5_connections = n5.connections

    assert (len(n1_connections) == 1)
    assert (len(n2_connections) == 1)
    assert (len(n3_connections) == 2)
    assert (len(n4_connections) == 0)
    assert (len(n5_connections) == 0)

    assert(n1_connections[0][0] is n5)
    assert(n1_connections[0][1] == (-2))

    assert(n2_connections[0][0] is n4)
    assert(n2_connections[0][1] == (0.5))

    assert(n3_connections[0][0] is n1)
    assert(n3_connections[0][1] == (10))
    assert(n3_connections[1][0] is n2)
    assert(n3_connections[1][1] == (-1))


def test_add_energy():
    n1 = Neuron(pos=(0,0,0), network=None)

    test_passed = False

    def f(x):
        nonlocal test_passed
        test_passed = True
    n1.subscribe_on_activation(f)
    n1.add_energy(None, 100)
    assert test_passed