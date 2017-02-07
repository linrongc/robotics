#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 1/23/17 11:44 PM
@author = Rongcheng
"""
import numpy as np
from util import unit_vector, get_vector


def rotation_matrix(axis, theta):
    k = unit_vector(axis)
    theta = np.deg2rad(theta)  # convert degree to radians
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    v_theta = 1 - cos_theta

    return np.array([
        [k[0]*k[0]*v_theta+cos_theta,      k[0]*k[1]*v_theta-k[2]*sin_theta, k[0]*k[2]*v_theta+k[1]*sin_theta],
        [k[0]*k[1]*v_theta+k[2]*sin_theta, k[1]*k[1]*v_theta+cos_theta,      k[1]*k[2]*v_theta-k[0]*sin_theta],
        [k[0]*k[2]*v_theta-k[1]*sin_theta, k[1]*k[2]*v_theta+k[0]*sin_theta, k[2]*k[2]*v_theta+cos_theta]
        ])


def rot(axis, theta):
    """
    :param axis: any 1*3 numpy array or ["x", "y", "z"]
    :param theta: rotation degree
    :return: 4*4 with rotation matrix calculated
    """
    axis = unit_vector(axis)
    mat = np.identity(4)
    mat[:3, :3] = rotation_matrix(axis, theta)
    return mat


def trans(axis, length):
    axis = unit_vector(axis)
    mat = np.identity(4)
    mat[:3, 3] = np.transpose(axis*length)
    return mat


def chain(*opts):
    mat = opts[0]
    for n in range(1, len(opts)):
        mat = np.matmul(mat, opts[n])
    return mat


def points(p):
    vec = np.array([0, 0, 0, 1])[:, np.newaxis]  # clarified as column vector
    vec[:3, 0] = get_vector(p)
    return vec


def to_frame(rot_mat=None, p=None):
    """
    :param rot_mat: 3*3 rotation matrix
    :param p: 3 element vector
    :return: 4*4 frame matrix
    """
    mat = np.identity(4)
    if rot_mat is not None:
        mat[:3, :3] = rot_mat
    if p is not None:
        mat[:, 3] = p.flatten()
    return mat


if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    print rot('x', -90)
    print trans('y', 3)
    print points([0, 0, 1])
    T = chain(rot('z', 90), trans('x', 2), trans('y', 3), rot('x', -90))
    print T
    print chain(T, to_frame(p=points([1, 1, 1])))
    '''
    T_inv = np.linalg.inv(T)
    print T_inv

    print chain(rot('x', 90), trans('y', -3), trans('x', -2), rot('z', -90))

    print chain(rot('x', 45), rot('y', 30))
    print np.degrees(np.arccos(0.866))
    '''