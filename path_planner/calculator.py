#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 4/28/2017 5:03 PM
@author = Rongcheng
"""
import numpy as np
from utility import *


class Calculator(object):

    def __init__(self):
        pass

    def get_force(self, par, pos):
        pass

    def get_potential(self, par, pos):
        pass


class LinearCalculator(Calculator):

    def __init__(self, slope=1.0, accept_zone=0.0):
        self.accept_zone = accept_zone
        self.slope = slope
        super(LinearCalculator, self).__init__()

    def get_force(self, par, pos):
        """
        :param par: goal position
        :param pos: [x, y]
        :return: force [fx, fy]
        """
        vec = par[:2] - pos[:2]
        dis = l2_dis(vec)
        if dis > self.accept_zone:
            return self.slope*vec/dis
        else:
            return np.array((0., 0.))

    def get_potential(self, par, pos):
        """
        :param par: goal position
        :param pos: [x, y]
        :return: potential
        """
        vec = par[:2] - pos[:2]
        dis = l2_dis(vec)
        if dis > self.accept_zone:
            return (dis - self.accept_zone)*self.slope
        else:
            return 0.


class CircleCalculator(Calculator):

    def __init__(self, alpha=1.0):
        self.alpha = alpha
        super(CircleCalculator, self).__init__()

    def get_force(self, par, pos):
        """
        :param par:  the parameter of rectangle [x_c, y_c, r]
        :param pos: [x, y, r]
        :return: force [fx, fy]
        """
        center = par[:2]
        radius = par[2]
        vec = pos[:2] - center
        dis = l2_dis(vec) - radius - pos[2]
        if dis <= 0:
            return np.array((0., 0.))
        force = self.alpha * np.exp(-dis)
        return force*vec/(dis + radius)

    def get_potential(self, par, pos):
        """
        :param par: par: the parameter of rectangle [x, y, r]
        :param pos: [x, y]
        :return: potential
        """
        center = par[:2]
        radius = par[2]
        dis = euclidean(center, pos[:2]) - radius - pos[2]
        if dis <= 0:
            return self.alpha
        else:
            return self.alpha*np.exp(-dis)


class RectangleCalculator(Calculator):
    """
        Calculator for Rectangles
    """

    def __init__(self, alpha=1.0):
        self.alpha = alpha
        super(RectangleCalculator, self).__init__()

    def get_closest_vector(self, par, pos):
        """
        :param par:  the parameter of rectangle [x0, y0, x1, y1]
        :param pos: [x, y]
        :return: shortest vector from rectangle to the position
        """
        def get_pos(x, low, high):
           if x < low:
               return x - low
           if x > high:
               return x - high
           return 0
        return np.array((get_pos(pos[0], par[0], par[2]), get_pos(pos[1], par[1], par[3])))

    def get_force(self, par, pos):
        """
        :param par: the parameter of rectangle [x0, y0, x1, y1]
        :param pos: [x, y, size]
        :return: force [fx, fy]
        """
        vec = self.get_closest_vector(par, pos)
        dis = l2_dis(vec) - pos[2]
        if dis <= 0:
            return np.array((0., 0.))
        else:
            force = self.alpha * np.exp(-dis)
            force = force*vec/dis
            return force + 0.1*np.array((force[1], -force[0]))

    def get_potential(self, par, pos):
        """
        :param par: par: the parameter of rectangle [x0, y0, x1, y1]
        :param pos: [x, y]
        :return: potential
        """
        vec = self.get_closest_vector(par, pos)
        dis = l2_dis(vec) - pos[2]
        if dis <= 0:
            return self.alpha
        else:
            return self.alpha*np.exp(-dis)




if __name__ == "__main__":
    cal = CircleCalculator(1)
    par = np.array((1, 1., 0.5))
    pos = np.array((0, 1))
    print cal.get_force(par, pos)
    print cal.get_potential(par, pos)

    cal = RectangleCalculator(1)
    par = np.array((0, 0, 2, 1))
    pos = np.array((4, 0.5))
    print cal.get_force(par, pos)
    print cal.get_potential(par, pos)
