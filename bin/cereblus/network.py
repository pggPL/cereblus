import time
from .neuron import Neuron
import threading
import queue
from .event import Event

class NonPositiveInterval(Exception):
    pass

class NeuralNetwork:
    def __init__(self):
        self.neurons = []
        self.new_neurons_subscribers = []

        self.time_delay = 1

        self.time = 0.0
        self.steps = 0

        # Temporarily is a list
        # (time_of_event, function)
        self.__event_queue__ = queue.PriorityQueue()

        self.__run_lock__ = threading.Lock()

    def neuron(self, template=Neuron, pos=(0, 0, 0)):
        # Maybe check if neuron in in a network
        neuron = template(pos, self)
        self.neurons.append(neuron)

        neuron.subscribe_on_activation(self.__neuron_activated__)
        for f in self.new_neurons_subscribers:
            f(neuron)

        return neuron

    def subscribe_new_neurons(self, f):
        self.new_neurons_subscribers.append(f)

    def __neuron_activated__(self, sender):
        connections = sender.connections
        for con in connections:
            n, coeff = con
            self.append_fire(self.time + self.time_delay, sender, n, coeff)

    def append_event(self, event):
        self.__event_queue__.put(event)

    def append_fire(self, time, sender, fired_neuron, energy):
        f = (lambda: fired_neuron.add_energy(sender, energy))
        fire_event = Event(time, f)
        self.append_event(fire_event)


    def __get_event_queue_min__(self):
        if self.__event_queue__.empty():
            return False
        return self.__event_queue__.get()


    def stimulate(self, neuron, time_start, time_end, voltage, interval):
        cur_time = time_start
        if interval <= 0:
            raise NonPositiveInterval
        while cur_time <= time_end:
            self.append_fire(cur_time, None, neuron, voltage)
            cur_time += interval

    def run(self, steps=None, time=None):
        """
            Simulation will stop if number of steps are done AND time bound is achieved.
            On the end __current_time__ is equal __current_time__ + time, unless time is not specified.
        """

        self.__run_lock__.acquire()

        if steps is None and time is None:
            while self.__simulate_step__():
                pass
        elif steps is None:
            # time is set
            finish_time = self.time + time
            while self.time <= finish_time and self.__simulate_step__(time_bound=finish_time):
                pass
            self.time = finish_time
        elif time is None:
            # steps are set
            finish_steps = self.steps + steps
            while self.steps < finish_steps and self.__simulate_step__():
                pass
        else:
            # both time and steps are set
            finish_steps = self.steps + steps
            finish_time = self.time + time
            # until steps are done
            while self.steps < finish_steps and self.__simulate_step__():
                pass
            # until time is finished
            while self.time < finish_time and self.__simulate_step__(time_bound=finish_time):
                pass
            # Program can finish before
            self.time = finish_time
        self.__run_lock__.release()

    def __simulate_step__(self, time_bound=None):
        q : Event = self.__get_event_queue_min__()
        if not q:
            return False
        else:
            if time_bound is not None:
                if q.time > time_bound:
                    # we haven't used it
                    self.append_event(q)
                    return False
            self.time = q.time
            q.happen()
            self.steps += 1
            return True
