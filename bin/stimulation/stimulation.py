from .pixel import Pixel


class Stimulation:
    def __init__(self, num_of_pixels, name=""):
        self.name = name
        self.pixels = []
        self.loop = False

        for i in range(num_of_pixels):
            self.pixels.append(Pixel(parent_stimulation=self))

    def add_phase(self, img, duration=0.1):
        # wrong length

        if len(img) > len(self.pixels):
            raise WrongImageLength

        i = 0
        for pixel in self.pixels:
            pixel.add_phase(duration=duration, state=(img[i] == 'O'))
            i += 1

    def get_pixel(self, number):
        return self.pixels[number]

    def connect(self, neuron, num_of_pixel):
        try:
            neuron.connect_to_stimulus(self.pixels[num_of_pixel])
        except:
            raise NeuronNotReceptive


class WrongImageLength(Exception):
    def __init__(self):
        self.message = "The image in stimulus is bigger than number of the pixels."


class NeuronNotReceptive(Exception):
    def __init__(self):
        self.message = "Neuron is not a receptor – it does not have 'connect_to_stimulus' methos."