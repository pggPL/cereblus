# Info

Project which allow to simulate simple biological neural networks.

Below I attach the screen of a sample simulation. That simulation explains how lateral inhibition works.

![There should be photo of an app.](https://github.com/pggPL/cereblus/blob/master/img/celebrus.gif)


# Installation

1. Download [tar.gz file](https://github.com/pggPL/cereblus/raw/master/to_download/cereblus-0.1.0.tar.gz).
2. Run ```pip install ./path_to_file/cereblus-0.1.0.tar.gz```

# Usage

We have got four basic objects

1. ```Neuron``` represents one neuron.
2. ```Neural Network``` represents network.
3. ```Displayer``` represents graphical interface.
4. ```Stimulus``` represents stimulus, which activates neurons.

### Creating first network

Let's write
``` python
from cereblus import *

neural_network = NeuralNetwork()
n1 = neural_network.neuron(template=Receptor, pos=(300, 300, 0))
n2 = neural_network.neuron(template=Receptor, pos=(300, 400, 0))
n3 = neural_network.neuron(template=Receptor, pos=(550, 350, 0))
```

We've just created a network with three neurons – n1, n2 and n3. First two neurons are receptors -- they can react to the stimuli, which we will use later. n3 is standard Neuron. It is worth mentioning that all Receptor in child class of Neuron. Let's join them
```python
n1.connect(n3, coeff=0.5)
n2.connect(n3, coeff=0.7)
```
Now n1 is connected to n3 with coefficient 0.5 and n2 is connected to n3 with coefficient 0.7.

We connect our network to the ```Displayer```
```python
displayer = Displayer(neu_net)
displayer.show()
```

![](https://github.com/pggPL/cereblus/raw/master/img/from_readme_2.gif)

### Stimulating neurons

Our network is doing exactly nothing. Why? We haven't stimulated it. 
Let's create file ```stimulation.json``` 
```json
  {
  "num_of_pixels": 2,
  "loop": true,
  "phases": [
    [0.5, "O-"],
    [0.5, "-O"],
    [1, "OO"]
  ]
}

```

And connect it to the neurons n1 and n2
```python
stimulus = StimulationLoader.load_from_file("stimulation.json")
stimulus.connect(n1, num_of_pixel=0)
stimulus.connect(n2, num_of_pixel=1)
```

We can imagine it as two receptors connected to the two pixels. Pixel is active when there is 'O' in current phase, and it in inactive when it is '-'.

Now let's look on our network.

![](https://github.com/pggPL/cereblus/raw/master/img/from_readme_1.gif)

# Steps further

You can write your own Neurons – which for example learn and change connections. The easiest way is to inherit from the Neuron class. Look into the code to undersand how Neuron works – it is simple.
