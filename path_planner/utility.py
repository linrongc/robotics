#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 4/28/2017 5:58 PM
@author = Rongcheng
"""
import numpy as np


def l2_dis(x):
    """
    l2 norm of a vector
    """
    return np.sqrt(np.sum(np.square(x)))


def euclidean(x, y):
    """
    get euclidean distance from x to y
    :param x: any array
    :param y: any array with same size with x
    :return: euclidean distance
    """
    return l2_dis(x-y)