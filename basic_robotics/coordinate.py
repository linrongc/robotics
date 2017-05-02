#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 2/7/17 11:00 AM
@author = Rongcheng
"""
from frame import rot, chain
import numpy as np


def rot_to_xyz_fix(rot_mat):
    """
    :param rot_mat: rotation matrix or frame matrix
    :return: [alpha, beta, gamma]
    """
    beta = np.arctan2(-rot_mat[2, 0], np.sqrt(np.square(rot_mat[0, 0]) + np.square(rot_mat[1, 0])))
    cos_beta = np.cos(beta)
    if cos_beta != 0:  # beta is not -pi/2 or pi/2
        alpha = np.arctan2(rot_mat[1, 0]/cos_beta, rot_mat[0,0]/cos_beta)
        gamma = np.arctan2(rot_mat[2, 1]/cos_beta, rot_mat[2, 2]/cos_beta)
    else:
        alpha = 0
        gamma = np.sin(beta)*np.arctan2(rot_mat[0, 1], rot_mat[1, 1])
    return np.rad2deg([alpha, beta, gamma])


def xyz_fix_to_rot(par, to_frame=False):
    """
    :param par: [alpha, beta, gamma]
    :param to_frame: return 4*4 frame matrix (True) or only 3*3 rotation matrix (False)
    :return: frame matrix
    """
    mat = chain(rot("z", par[0]), rot("y", par[1]), rot("x", par[2]))
    if not to_frame:
        return mat[:3, :3]
    return mat


if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    mat = xyz_fix_to_rot([0, 90, 75], to_frame=False)
    print mat
    xyz = rot_to_xyz_fix(mat)
    print xyz