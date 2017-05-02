#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 4/28/2017 5:58 PM
@author = Rongcheng
"""
import numpy as np


def l2_dis(x):
    return np.sqrt(np.sum(np.square(x)))


def euclidean(x, y):
    return l2_dis(x-y)