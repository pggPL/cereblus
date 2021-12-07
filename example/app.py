from cereblus import Displayer, StimulationLoader
from cereblus.neural_networks import LateralInhibitionNetwork
import math


neu_net = LateralInhibitionNetwork()

s = StimulationLoader.load_from_file("./stimulations/lateral_inhibition_example.json")
i = 0
for receptor in neu_net.neurons_receptors:
    s.connect(receptor, math.floor(i/ 2))
    i += 1


displayer = Displayer(neu_net)
displayer.show()