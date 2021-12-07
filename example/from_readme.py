from cereblus import *

neural_network = NeuralNetwork()
n1 = neural_network.neuron(template=Receptor, pos=(300, 300, 0))
n2 = neural_network.neuron(template=Receptor, pos=(300, 400, 0))
n3 = neural_network.neuron(template=Receptor, pos=(550, 350, 0))

n1.connect(n3, coeff=0.5)
n2.connect(n3, coeff=0.7)

stimulus = StimulationLoader.load_from_file("stimulation.json")
stimulus.connect(n1, num_of_pixel=0)
stimulus.connect(n2, num_of_pixel=1)


displayer = Displayer(neural_network)
displayer.show()
