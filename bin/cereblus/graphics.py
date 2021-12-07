from tkinter import *


class Graphics:
    def __init__(self, displayer):
        self.size = (1000, 500)
        self.master = Tk()
        self.master.title("Neural network simulation")
        self.canvas = Canvas(self.master,
                             width=self.size[0],
                             height=self.size[1])
        self.canvas.pack(expand=YES, fill=BOTH)
        self.displayer = displayer

        self.time_step_labels()

        self.buttons_box = self.steps_buttons_box = Label(
            self.master
        )

        self.buttons_to_lock_when_animation_starts = []

        self.buttons_box.pack()

        self.steps_buttons_box = None
        self.animation_buttons_box = None
        self.time_buttons_box = None
        self.init_button_boxes()

        self.init_buttons("steps",
                          "Steps",
                          self.steps_buttons_box,
                          (lambda mult: self.displayer.next_steps(mult * self.steps_mult)),
                          self.steps_mult_modify
                          )
        self.steps_mult = 0

        self.init_buttons("miliseconds",
                          "Time",
                          self.time_buttons_box,
                          (lambda mult: self.displayer.next_time(mult * self.time_mult)),
                          self.time_mult_modify
                          )
        self.time_mult = 0


        self.init_animations(self.animation_buttons_box)

    def init_button_boxes(self):
        self.steps_buttons_box = Label(
            self.buttons_box,
            text="Steps",
            borderwidth=1,
            relief="solid"
        )
        self.steps_buttons_box.pack(side=LEFT, expand=True)

        self.time_buttons_box = Label(
            self.buttons_box,
            text="Time",
            borderwidth=1,
            relief="solid"
        )
        self.time_buttons_box.pack(
            padx=5,
            side=RIGHT
        )

        self.animation_frame = Frame(self.buttons_box,
                                     width=200,
                                     height=1400,
                                     borderwidth=1,
                                     relief="solid"
                                     )
        self.animation_frame.pack_propagate()
        self.animation_frame.pack()

        self.animation_buttons_box = Frame(
            self.animation_frame,
            width=200
        )
        self.animation_buttons_box.pack(
            padx=50,
            side=RIGHT,
        )

    def steps_mult_modify(self, x):
        self.steps_mult = int(x)

    def init_buttons(self, unit, category, box, function, mult_modify_function):
        l = Label(box, text=category, bg="yellow")
        l.pack()
        self.steps_silder = Scale(box,
                                  from_=0,
                                  to=100,
                                  orient=HORIZONTAL,
                                  label="Choose x",
                                  command=mult_modify_function)
        self.steps_silder.pack()

        def step_button(mult):
            nonlocal self
            button = Button(box,
                            text='Next {0}x '.format(mult) + unit,
                            command=(lambda: function(mult)))
            button.pack(side=BOTTOM)
            self.buttons_to_lock_when_animation_starts.append(button)

        step_button(100)
        step_button(10)
        step_button(1)

    def init_animations(self, box):
        l = Label(box, text="Animation", bg="yellow")
        l.pack()
        self.steps_silder = Scale(box,
                                  from_=0,
                                  to=100,
                                  orient=HORIZONTAL,
                                  label="Ms per second",
                                  command=self.displayer.change_animation_rate)
        self.steps_silder.pack()

        start_button = Button(box,
                              text='Start',
                              command=self.displayer.start_animation)
        stop_button = Button(box,
                              text='Stop',
                              command=self.displayer.stop_animation)

        stop_button.pack(side=BOTTOM)
        start_button.pack(side=BOTTOM)

        self.buttons_to_lock_when_animation_starts.append(start_button)

    def animation_lock_buttons(self):
        for b in self.buttons_to_lock_when_animation_starts:
            b['state'] = 'disabled'

    def enable_buttons(self):
        for b in self.buttons_to_lock_when_animation_starts:
            b['state'] = 'normal'

    def time_step_labels(self):
        self.time_label = Label(
            self.master,
            text="Neuronal time = 0.000 s"
        )
        self.time_label.pack(
            padx=5,
            side=TOP
        )
        self.steps_label = Label(
            self.master,
            text="Steps = 0"
        )
        self.steps_label.pack(
            padx=5,
            side=TOP
        )

    def time_mult_modify(self, x):
        self.time_mult = int(x)

    def start(self):
        mainloop()

    def getCanvas(self):
        return self.canvas

    def update_steps_and_time(self, steps, time):
        self.time_label['text'] =  "Time = {} s".format(round(time,3))
        self.steps_label['text'] =  "Steps = {} ".format(steps)
