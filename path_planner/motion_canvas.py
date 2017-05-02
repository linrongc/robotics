#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 4/28/2017 2:15 PM
@author = Rongcheng
"""
from Tkinter import *
import math


class MotionCanvas(Canvas):
    def __init__(self, master, width, height, gui=None):
        Canvas.__init__(self, master, width=width, height=height, bg="black")
        self.master = master
        self.gui = gui
        self.pos_dic = {}
        self.name_dic = {}
        self.goals = []
        self.sources = []
        self.trajectory = []

        self.task = ""
        self.mouse_status = ""
        self.record_pos = None

        self.circle_obstacles = []
        self.rect_obstacles = []
        self.focus_set()
        self.bind("<Key>", self.canvas_keyboard)

        self.bind("<Button-1>", self.canvas_click)
        self.bind("<ButtonRelease-1>", self.canvas_click_release)
        self.bind("<B1-Motion>", self.canvas_motion)

        self.create_source(600, 100)
        print self.coords(self.sources[-1])
        self.create_goal(100, 600)
        self.create_circle_obstacle(300, 450, 50)
        self.create_rect_obstacle(400, 200, 200, 150)

    def clear(self):
        self.pos_dic.clear()
        self.name_dic.clear()
        widget_list = [self.sources, self.goals, self.rect_obstacles, self.circle_obstacles, self.trajectory]
        for item_list in widget_list:
            print item_list
            for item in item_list[:]:
                self.delete_widget(item)

    def import_data(self, data):
        self.clear()
        for coord in data["rectangle_obstacles"]:
            self.create_rect_obstacle((coord[2] + coord[0])/2, (coord[3] + coord[1])/2, width=(coord[2] - coord[0]),
                                      height=(coord[3] - coord[1]))
        for par in data["circle_obstacles"]:
            self.create_circle_obstacle(*par)
        for par in data["sources"]:
            self.create_source(*par)
        for par in data["goals"]:
            self.create_goal(*par)

    def export_data(self):
        data = {
            "sources": self._export_triangle(self.sources),
            "goals": self._export_triangle(self.goals),
            "rectangle_obstacles": self._export_rectangle(self.rect_obstacles),
            "circle_obstacles": self._export_circle(self.circle_obstacles)
                }
        return data

    def _export_rectangle(self, items):
        data = []
        for rect in items:
            data.append(self.coords(rect))
        return data

    def _export_triangle(self, items):
        data = []
        for tri in items:
            coord = self.coords(tri)
            data.append([coord[0], (coord[1] + 2*coord[3])/3, (coord[3] - coord[1])*2/3])
        return data

    def _export_circle(self, items):
        data = []
        for circle in items:
            coord = self.coords(circle)
            data.append([(coord[0] + coord[2])/2, (coord[1] + coord[3])/2, (coord[2] - coord[0])/2])
        return data

    def create_source(self, x, y, size=20):
        print "creating source..."
        source = self.create_triangle(x, y, size=size, fill="green")
        self.sources.append(source)
        self.name_dic[source] = "Source_" + str(source)
        self.task = ""

    def create_goal(self, x, y, size=20):
        print "crating goal..."
        goal = self.create_triangle(x, y, size=size, fill="red")
        self.goals.append(goal)
        self.name_dic[goal] = "Goal_" + str(goal)
        self.task = ""

    def create_circle_obstacle(self, x, y, r=10):
        print "creating circle..."
        self.record_pos = (x, y)
        circle = self.create_circle(x, y, r=r, fill="gray")
        self.name_dic[circle] = "circle_obstacle_"+str(circle)
        self.circle_obstacles.append(circle)

    def create_rect_obstacle(self, x, y, width=10, height=10):
        print "creating rectangle..."
        self.record_pos = (x, y)
        rect = self.create_rectangle(x - width/2, y - height/2, x + width/2, y + height/2, fill="gray")
        self.enable_moving(rect)
        self.name_dic[rect] = "rectangle_obstacle_"+str(rect)
        self.rect_obstacles.append(rect)

    def canvas_click(self, event):
        if self.task == "obstacle_circle":
            self.create_circle_obstacle(event.x, event.y)
        elif self.task == "obstacle_rectangle":
            self.create_rect_obstacle(event.x, event.y)
        elif self.task == "source":
            self.create_source(event.x, event.y)
        elif self.task == "goal":
            self.create_goal(event.x, event.y)

    def canvas_keyboard(self, event):
        if event.keysym =="Delete" or event.keysym == "BackSpace":
            try:
                widget = event.widget.find_closest(event.x, event.y)[0]
                self.delete_widget(widget)
            except IndexError:
                pass

    def delete_widget(self, widget):
        print "delete widget: ", str(widget)
        self.delete(widget)
        if widget in self.sources:
            self.sources.remove(widget)
        elif widget in self.goals:
            self.goals.remove(widget)
        elif widget in self.circle_obstacles:
            self.circle_obstacles.remove(widget)
        elif widget in self.rect_obstacles:
            self.rect_obstacles.remove(widget)
        elif widget in self.trajectory:
            self.trajectory.remove(widget)

    def canvas_click_release(self, event):
        if self.task.startswith("obstacle") and self.record_pos is not None:
            '''
            target = self.obstacles[-1]
            (x, y) = self.record_pos
            r = math.sqrt((event.x - x)**2 + (event.y - y)**2)
            self.itemconfig(target, x0=x-r, y0=y-r, x1=x+r, y1=y+r)
            '''
            self.record_pos = None
            self.task = ""

    def canvas_motion(self, event):
        if self.task == "obstacle_circle" and self.record_pos is not None:
            target = self.circle_obstacles[-1]
            (x, y) = self.record_pos
            r = math.sqrt((event.x - x)**2 + (event.y - y)**2)
            # print r
            self.coords(target, x-r, y-r, x+r, y+r)
        elif self.task == "obstacle_rectangle" and self.record_pos is not None:
            target = self.rect_obstacles[-1]
            (x, y) = self.record_pos
            w_2, h_2 = math.fabs(event.x - x), math.fabs(event.y - y)
            self.coords(target, x-w_2, y-h_2, x+w_2, y+h_2)
        else:
            self.gui.set_status("x: %d, y:%d" % (event.x, event.y))
        self.focus_set()

    def create_triangle(self, x, y, size=10, fill="red"):
        triangle= self.create_polygon([
            x , y - size,
            x + int(1.73*size/2), y + size/2 ,
            x - int(1.73*size/2), y + size/2
        ], fill=fill, outline="blue")
        self.enable_moving(triangle)
        return triangle

    def create_circle(self, x, y, r=10, **kwargs):
        circle = self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
        self.enable_moving(circle)
        return circle

    def on_click(self, event):
        widget = event.widget.find_closest(event.x, event.y)[0]
        self.itemconfig(widget, outline="green")
        self.pos_dic[widget] = (event.x, event.y)
        self.gui.set_status("click on " + self.name_dic[widget])

    def on_click_release(self, event):
        try:
            widget = event.widget.find_closest(event.x, event.y)[0]
            self.itemconfig(widget, outline="blue")
            if widget in self.pos_dic:
                del self.pos_dic[widget]
        except TclError:
            pass

    def on_motion(self, event):
        widget = event.widget.find_closest(event.x, event.y)[0]
        if widget in self.pos_dic:
            pre = self.pos_dic[widget]
            current = (event.x, event.y)
            self.move(widget, current[0]-pre[0], current[1]-pre[1])
            self.pos_dic[widget] = current

    def enable_moving(self, widget):
        self.tag_bind(widget, '<Button-1>', self.on_click)
        self.tag_bind(widget, '<ButtonRelease-1>', self.on_click_release)
        self.tag_bind(widget, '<B1-Motion>', self.on_motion)

    def draw_trajectory(self, path):
        line = self.create_line(*path, fill="green")
        self.trajectory.append(line)

    def clear_trajectory(self):
        for traj in self.trajectory[:]:
            self.delete_widget(traj)
