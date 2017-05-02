#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 1/23/17 11:48 PM
@author = Rongcheng
"""
import numpy as np

note_dict = {"x": 0, "y": 1, "z": 2}


def normalize(x):
    norm = np.linalg.norm(x)
    if norm == 0:
        return x
    return x/norm


def get_vector(x):
    if isinstance(x, str):
        ind = note_dict[x.lower()]
        x = np.zeros(3)
        x[ind] = 1
    return x


def unit_vector(axis):
    axis = get_vector(axis)
    axis = normalize(axis)
    return axis