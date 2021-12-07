import math


def app_init():
    from .graphics import Graphics
    from .neural_networks.network1 import Network1
    from .neural_networks.lateral_inhibiton_example import LateralInhibitionNetwork
    from .displayer import Displayer
    from .stimulation import Stimulation, StimulationLoader

    neu_net = LateralInhibitionNetwork()

    s = StimulationLoader.load_from_file("./stimulations/lateral_inhibition_example.json")
    i = 0
    for receptor in neu_net.neurons_receptors:
        s.connect(receptor, math.floor(i/ 2))
        i += 1

    print(neu_net.neurons_bipolar[7].connections)

    displayer = Displayer(neu_net)
    displayer.show()