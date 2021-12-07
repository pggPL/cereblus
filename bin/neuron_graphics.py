# it hold graphical representation of a neuron
import tkinter
import math


class NeuronGraphics:
    def __init__(self, neuron, canvas):
        self.neuron = neuron
        self.x, self.y, self.z = neuron.position
        self.neuron.subscribe_on_activation(self.change_state)
        self.canvas = canvas

        self.size = 4

        # draw initial
        self.state = "passive"
        self.drawn_state = "passive"

        self.activations = 0

        self.draw_passive()

    def create_circle(self, x, y, r, rgb_fill):  # center coordinates, radius
        if rgb_fill is not None:
            fill = self._from_rgb(rgb_fill)
        else:
            fill = None
        x += 30
        y += 30
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        c = self.canvas.create_oval(x0, y0, x1, y1, fill=fill)
        return c

    def change_state(self, sender):
        self.activations += 1
        self.state = "active"

    def update_graphics(self, max_activations):
        if self.state != self.drawn_state:
            self.canvas.delete(self.graphical_representation)
        else:
            self.state = "passive"
            self.activations = 0
            return
        if self.state == "active":
            self.draw_active((self.activations / max_activations))
        else:
            self.draw_passive()
        self.state = "passive"
        self.activations = 0

    def _from_rgb(self, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb

    def draw_active(self, activation_ratio):
        print(activation_ratio)
        self.graphical_representation = self.create_circle(self.x,
                                                           self.y,
                                                           self.size,
                                                           (math.floor(200 * activation_ratio),
                                                            math.floor(255 * (1 - math.sqrt(activation_ratio))),
                                                            math.floor(255 * (1 - math.sqrt(activation_ratio)))))
        self.drawn_state = "active"

    def draw_passive(self):
        self.graphical_representation = self.create_circle(self.x, self.y, self.size, None)
        self.drawn_state = "passive"
