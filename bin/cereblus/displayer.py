from .graphics import Graphics
from .neuron_graphics import NeuronGraphics
import threading
import time


class Displayer:
    def __init__(self, neural_network, graphics=Graphics):
        self.graphics = graphics(self)
        self.canvas = self.graphics.getCanvas()
        self.neural_network = neural_network
        self.neurons = []

        self.__collect_neurons_from_network__()
        self.neural_network.subscribe_new_neurons(self.__new_neuron__)

        self.animation_thread = None
        self.__animation_running__ = False
        self.__animation_rate__ = 1

        self.__time_elapse_update__ = 100

    def show(self):
        self.graphics.start()

    def __collect_neurons_from_network__(self):
        for n in self.neural_network.neurons:
            neuron_graphics_layer = NeuronGraphics(n, self.canvas)
            self.neurons.append(neuron_graphics_layer)

    def __new_neuron__(self, neuron):
        self.neurons.append(NeuronGraphics(neuron, self.canvas))

    def next_steps(self, steps):
        if self.__animation_running__:
            return
        self.neural_network.run(steps=steps)
        self.update_graphics()
        self.update_steps_and_time()

    def next_time(self, time):
        if self.__animation_running__:
            return
        milisec = 0.001
        self.neural_network.run(time=milisec * time)
        self.update_graphics()
        self.update_steps_and_time()

    def start_animation(self):

        self.graphics.animation_lock_buttons()

        self.__animation_running__ = True
        self.animation_thread = threading.Thread(target=self.animate, daemon=True)
        self.animation_thread.start()

    def animate(self):
        while self.__animation_running__:
            self.update_steps_and_time()
            time_window = 100
            time_start = time.time()

            # We do as much as we can in a time window
            done_steps = 0
            neuron_time_start = self.neural_network.time
            time_elapsed = time.time() - time_start
            while (self.neural_network.time - neuron_time_start) < 0.001 * self.__animation_rate__ and \
                    (time_elapsed < time_window):
                self.neural_network.run(steps=1)
                done_steps += 1
                # time.time() is costly, so we update it sometimes
                if done_steps % self.__time_elapse_update__ == 0:
                    self.update_steps_and_time()
                    time_elapsed = time.time() - time_start
            self.update_graphics()

            time_elapsed = time.time() - time_start
            self.update_steps_and_time()
            if time_elapsed < time_window:
                time.sleep(0.001 * (time_window - time_elapsed))

    def stop_animation(self):
        self.__animation_running__ = False
        self.graphics.enable_buttons()

    def change_animation_rate(self, x):
        self.__animation_rate__ = int(x)

    def update_steps_and_time(self):
        self.graphics.update_steps_and_time(steps=self.neural_network.steps, time=self.neural_network.time)

    def update_graphics(self):
        m = 0
        for neuron in self.neurons:
            m = max(neuron.activations, m)

        for neuron in self.neurons:
            neuron.update_graphics(m)