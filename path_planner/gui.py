#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 4/27/2017 9:31 PM
@author = Rongcheng
"""
from Tkinter import *
import math
from motion_canvas import MotionCanvas
import tkFileDialog, tkMessageBox
import json
from planner import PotentialPlanner
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.minsize(900, 720)
        self.root.title("Potential Field Path Planner")
        self._center(self.root)
        self.var_dic = {}
        self.planner = PotentialPlanner()
        self.init_widgets()


    def init_var(self):
        """
        Initialize the parameters
        """
        self.alpha = DoubleVar()
        self.alpha.set(1.0)
        self.var_dic["alpha"] = self.alpha

        self.status = StringVar()
        self.status.set("status: empty")
        self.var_dic["status"] = self.status

        self.attract = DoubleVar()
        self.attract.set(0.1)
        self.var_dic["attract"] = self.attract

        self.block_type = IntVar()
        self.block_type.set(1)
        self.var_dic["block_type"] = self.block_type

        self.ball_size = IntVar()
        self.ball_size.set(5)
        self.var_dic["ball_size"] = self.ball_size

        self.clock = DoubleVar()
        self.clock.set(0.01)
        self.var_dic["clock"] = self.clock

        self.stride = DoubleVar()
        self.stride.set(1.0)
        self.var_dic["stride"] = self.stride

        self.resolution = DoubleVar()
        self.resolution.set(10)
        self.var_dic["resolution"] = self.resolution

        self.momentum = DoubleVar()
        self.momentum.set(0.5)
        self.var_dic["momentum"] = self.momentum

    def init_widgets(self):
        """
        initialize the frames
        """
        self.init_var()

        # frame initialization
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=YES)

        self.label_status = Label(self.main_frame, textvariable=self.status, font=("Courier", 10))
        self.label_status.pack(side=BOTTOM, fill=X)

        self.canvas = MotionCanvas(self.main_frame, 700, 700, gui=self)
        self.canvas.pack(side=RIGHT, expand=YES)

        self.config_frame = Frame(self.main_frame, width=200, height=700)
        self.config_frame.pack(side=LEFT, fill=Y)

        self.par_frame = Frame(self.config_frame, width=200, height=500)
        self.par_frame.pack(side=TOP, fill=Y)

        self.control_frame = Frame(self.config_frame, width=200, height=200)
        self.control_frame.pack(side=BOTTOM, fill=NONE)

        self.init_control_frame()
        # parameter widgets
        self.init_par_frame()

    def init_control_frame(self):
        """
        Initialize the widgets in control frame
        :return: None
        """
        # control widgets
        self.label_control = Label(self.control_frame, text="Control:", font=("Courier", 13))
        self.label_control.grid(row=0, column=0, sticky=W, pady=2)

        self.btn_start = Button(self.control_frame, text="Start", bg="green", width=15, bd=2, font=("Courier", 13))
        self.btn_start.grid(row=1, column=0, pady=2, sticky=E)
        self.btn_start.bind('<Button-1>', self.button_event)

        # self.btn_end = Button(self.control_frame, text="End", bg="red", width=15, bd=2, font=("Courier", 13))
        # self.btn_end.grid(row=2, pady=2, sticky=E)

        self.btn_clear = Button(self.control_frame, text="Clear Traj", bg="red", width=15, bd=2, font=("Courier", 13))
        self.btn_clear.grid(row=2, pady=2, sticky=E)
        self.btn_clear.bind('<Button-1>', self.button_event)

        self.btn_draw_potential = Button(self.control_frame, bg='gray', text="Potential Field", width=15, bd=2, font=("Courier", 13))
        self.btn_draw_potential.grid(row=3, pady=2, sticky=E)
        self.btn_draw_potential.bind("<Button-1>", self.button_event)



    def init_par_frame(self):
        """
        Initialize the widgets in parameter frame
        :return: None
        """
        ind = 0
        self.label_config = Label(self.par_frame, text="Configuration:", font=("Courier", 13))
        self.label_config.grid(row=ind/2, column=ind%2, pady=2, columnspan=2, sticky=W)
        ind += 2

        self.label_size = Label(self.par_frame, text="Size:", font=("Courier", 13))
        self.label_size.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        ind += 1
        self.entry_size = Entry(self.par_frame, width=8, bd=2, text=self.ball_size, font=("Courier", 13))
        self.entry_size.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        ind += 1

        # self.label_clock = Label(self.par_frame, text="Clock:", font=("Courier", 13))
        # self.label_clock.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        # ind += 1
        # self.entry_clock = Entry(self.par_frame, width=8, bd=2, text=self.clock, font=("Courier", 13))
        # self.entry_clock.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        # ind += 1

        self.label_stride = Label(self.par_frame, text="Stride:", font=("Courier", 13))
        self.label_stride.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        ind += 1
        self.entry_stride = Entry(self.par_frame, width=8, bd=2, text=self.stride, font=("Courier", 13))
        self.entry_stride.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        ind += 1

        '''
        self.label_momentum = Label(self.par_frame, text="momentum:", font=("Courier", 13))
        self.label_momentum.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        ind += 1
        self.entry_momentum = Entry(self.par_frame, width=8, bd=2, text=self.momentum, font=("Courier", 13))
        self.entry_momentum.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        ind += 1
        '''

        self.label_resolution = Label(self.par_frame, text="Resolution:", font=("Courier", 11))
        self.label_resolution.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        ind += 1
        self.entry_resolution = Entry(self.par_frame, width=8, bd=2, text=self.resolution, font=("Courier", 13))
        self.entry_resolution.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        ind += 1

        self.split_1 = Label(self.par_frame, text="-------------------------------------")
        self.split_1.grid(row=ind/2, column=ind%2, pady=2, columnspan=2)
        ind += 2

        self.label_force = Label(self.par_frame, text="Force:", font=("Courier", 13))
        self.label_force.grid(row=ind/2, column=ind%2, pady=2, columnspan=2, sticky=W)
        ind += 2

        self.label_alpha = Label(self.par_frame, text="Repulse:", font=('Courier', 13))
        self.label_alpha.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        ind += 1

        self.entry_alpha = Entry(self.par_frame, width=8, bd=2, text=self.alpha, font=('Courier', 13))
        self.entry_alpha.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        ind += 1

        self.label_attract = Label(self.par_frame, text="Attract: ", font=("Courier", 13))
        self.label_attract.grid(row=ind/2, column=ind%2, pady=2, sticky=W)
        ind += 1

        self.entry_attract = Entry(self.par_frame, width=8, bd=2, text=self.attract, font=("Courier", 13))
        self.entry_attract.grid(row=ind/2, column=ind%2, pady=2)
        ind += 1

        self.split_2 = Label(self.par_frame, text="-------------------------------------")
        self.split_2.grid(row=ind/2, column=ind%2, pady=2, columnspan=2)
        ind += 2

        self.label_block = Label(self.par_frame, text="Obstacle Type: ", font=("Courier", 13))
        self.label_block.grid(row=ind/2, column=ind%2, columnspan=2, pady=2, sticky=W)
        ind += 2

        self.blocks = [
            ("Circle", 1),
            ("Rectangle", 2)
        ]
        self.radio_block =[]
        for txt, val in self.blocks:
            btn = Radiobutton(self.par_frame, indicatoron=0, width=10, text=txt, variable=self.block_type, value=val)
            btn.grid(row=ind/2, column=ind%2, pady=2)
            ind += 1

        self.btn_create_block = Button(self.par_frame, text="Add Obstacle", bg="gray", font=("Courier", 13), width=15)
        self.btn_create_block.grid(row=ind/2, column=ind%2, columnspan=2, pady=2)
        self.btn_create_block.bind("<Button-1>", self.button_event)
        ind += 2

        self.btn_create_start = Button(self.par_frame, text="Add Source", bg="pale green", font=("Courier", 13), width=15)
        self.btn_create_start.grid(row=ind/2, column=ind%2, columnspan=2, pady=2)
        self.btn_create_start.bind("<Button-1>", self.button_event)
        ind += 2

        self.btn_create_goal = Button(self.par_frame, text="Add Goal", bg="tomato", font=("Courier", 13), width=15)
        self.btn_create_goal.grid(row=ind/2, column=ind%2, columnspan=2, pady=2)
        self.btn_create_goal.bind("<Button-1>", self.button_event)
        ind += 2

        self.split_3 = Label(self.par_frame, text="-------------------------------------")
        self.split_3.grid(row=ind/2, column=ind%2, pady=2, columnspan=2)
        ind += 2

        self.btn_save = Button(self.par_frame, text="Save", bg="slate blue", fg="white",
                               font=("Courier", 13), width=15, command=self.save_config)
        self.btn_save.grid(row=ind/2, column=ind%2, columnspan=2, pady=2)
        ind += 2

        self.btn_load = Button(self.par_frame, text="Load", bg="slate blue", fg="white",
                               font=("Courier", 13), width=15, command=self.load_config)
        self.btn_load.grid(row=ind/2, column=ind%2, columnspan=2, pady=2)
        ind += 2

    def _center(self, toplevel):
        """
        Put the widget in the window center
        :param toplevel: container
        :return: None
        """
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def run(self):
        self.root.mainloop()

    def button_event(self, event):
        """
        function to deal with button events
        :param event: tkinter event
        :return: None
        """
        if event.widget == self.btn_create_block:
            print "click create obstacle button..."
            if self.block_type.get() == 1:
                self.set_status("creating circle obstacles..")
                self.canvas.task = "obstacle_circle"
                self.canvas.record_pos = None
            elif self.block_type.get() == 2:
                self.set_status("creating rectangle obstacles..")
                self.canvas.task = "obstacle_rectangle"
                self.canvas.record_pos = None
        elif event.widget == self.btn_create_start:
            print "create source..."
            self.set_status("creating source...")
            self.canvas.task = "source"
        elif event.widget == self.btn_create_goal:
            print "create goal..."
            self.set_status("creating goal...")
            self.canvas.task = "goal"
        elif event.widget == self.btn_start:
            print "start planning path..."
            self.planner.load_configuration(self.export_config())
            path = self.planner.generate_path()
            for p in zip(*path):
                p = np.array(p).flatten()
                self.canvas.draw_trajectory(p)
        elif event.widget == self.btn_clear:
            print "clear trajectories..."
            self.canvas.clear_trajectory()

        elif event.widget == self.btn_draw_potential:
            print "plot potential fields..."
            import plotly.plotly as py
            self.planner.load_configuration(self.export_config())
            potential = self.planner.get_potential_field()
            py.plot([dict(z=potential, type="surface")])

    def _export_par(self):
        """
        export the parameters as [(par_name, par_value), ....]
        """
        data = []
        for name, var in self.var_dic.iteritems():
            data.append((name, var.get()))
        return data

    def import_par(self, par_list):
        """
        import the parameters from [(par_name, par_value), ....]
        """
        for name, val in par_list:
            if name in self.var_dic:
                self.var_dic[name].set(val)

    def export_config(self):
        """
        export the configuration as a dictionary
        """
        data = self.canvas.export_data()
        data["parameter"] = self._export_par()
        return data

    def save_config(self):
        """
        save the configuration as a json file
        """
        print "Saving Configuration..."
        data = self.export_config()
        path = tkFileDialog.asksaveasfilename(title="Save Configuration File", defaultextension=".json")
        if len(path) > 0:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)

    def load_config(self):
        """
        load the configuration from file
        """
        print "Loading Configuration..."
        path = tkFileDialog.askopenfilename(title="Open Configuration File", defaultextension=".json")
        if len(path) > 0:
            with open(path, "r") as f:
                data = json.load(f)
            self.canvas.import_data(data)
            self.import_par(data["parameter"])

    def set_status(self, s="empty"):
        self.status.set("status: " + s)

if __name__ == "__main__":
    gui = GUI()
    gui.run()
