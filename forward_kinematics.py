#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 2/6/17 5:11 PM
@author = Rongcheng
"""
from frame import rot, trans, chain
import numpy as np


def step_trans(par):
    """
    :param par:[alpha_{i-1}(link twist), a_{i-1}(link length), d_i(link offset), theta_i(joint angle)]
    :return: Transition Matrix
    """
    if len(par) != 4:
        print "par:[alpha_{i-1}(link twist), a_{i-1}(link length), d_i(link offset), theta_i(joint angle)]"
        exit()

    opts = []
    if par[0] != 0:
        opts.append(rot("x", par[0]))
    if par[1] != 0:
        opts.append(trans("x", par[1]))
    if par[3] != 0:
        opts.append(rot("z", par[3]))
    if par[2] != 0:
        opts.append(trans("z", par[2]))
    if len(opts) > 0:
        return chain(*opts)
    else:
        return np.identity(4)


def mult_step_trans(par):
    """
    :param par: DH matrix with shape (None, 4)
    :return: Transition Matrix
    """
    steps = map(step_trans, par)
    return chain(*steps)


if __name__ == "__main__":
    np.set_printoptions(suppress=True)  # for concise print

    dh = np.array([
        [0, 0, 0, 0],
        [-90, 0, 0, 0],
        [0, 17, 4.9, 0],
        [-90, 0.8, 17.0, 0],
        [90, 0, 0, 0],
        [-90, 0, 0, 0]
    ])

    theta = np.array([60, 45, 25, 15, -10, -30])

    dh[:, 3] = theta


    print "the input DH matrix:"
    print dh
    print "======================================================================"
    for n in range(len(dh)):
        print "step ", n+1
        print step_trans(dh[n])
        print "---------------------------------------"
    print "======================================================================"
    print "full transformation matrix: "
    end = mult_step_trans(dh)
    print end


    print "======================================================================"
    from coordinate import rot_to_xyz_fix
    print "alpha, beta, gamma"
    print rot_to_xyz_fix(end)
    print "position:"
    print end[:3, 3].flatten()


