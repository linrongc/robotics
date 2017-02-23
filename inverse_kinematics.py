#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 2/23/17 12:19 PM
@author = Rongcheng
"""
import numpy as np
from forward_kinematics import mult_step_trans


def normalize_angle(vec):
    """
    normalize the angle to [-180, 180]
    :param vec: input angle vector
    :return: normalized angle
    """
    def change_angle(x):
        if x > 180:
            return x - 360
        if x < -180:
            return x + 360
        return x
    tmp = np.array([0]*len(vec))
    while True:
        tmp = np.array([change_angle(x) for x in vec])
        if all(tmp == vec):
            break
        else:
            vec = tmp
    return tmp


def abs_angle_dist(x, y):
    """
    :return: return the sum of minimum angular distance
    """
    return np.sum(np.abs(normalize_angle(x - y)))


class Planar3D:
    def __init__(self, l1=1, l2=1):
        self.l1, self.l2 = l1, l2
        self.theta = np.array([0, 0, 0])

    def inverse_kinematics(self, goal_frame, current_theta, solver=None):
        """
        :param goal_frame: the goal frame
        :param current_theta: current configuration
        :param solver: inverse kinematic solver
        :return: solutions
        """
        if solver is None:
            solver = self.close_form_inverse
        if goal_frame.shape == (3, 3):  # convert 3*3 frame to 4*4 frame
            tmp = np.identity(4)
            tmp[:2, :2] = goal_frame[:2, :2]
            tmp[:2, 3] = goal_frame[:2, 2]
            goal_frame = tmp
        elif goal_frame.shape != (4,4):
            raise Exception("goal frame shape error!")

        solutions = solver(goal_frame)
        if solutions is None:
            return
        dis_sol = [(abs_angle_dist(x, current_theta), x) for x in solutions]
        dis_sol.sort(key=lambda x: x[0])
        return [x[1] for x in dis_sol]

    def close_form_inverse(self, frame):
        """
        :param frame: 4*4 goal_frame
        :return: list of solutions, each solution is a array of configurations
        """
        px, py = frame[0, 3], frame[1, 3]
        m = (np.power(self.l1, 2) + np.power(px, 2) + np.power(py, 2) - np.power(self.l2, 2))/(2*self.l1)
        a = np.power(px, 2) + np.power(py, 2)
        b = -2*m*px
        c = np.power(m, 2) - np.power(py, 2)
        det = np.power(b, 2) - 4*a*c
        if a == 0:
            print "singularity occurs, set theta1 to 0!"
            sol_c1 = [1]
        else:
            if det < 0: return None
            elif det == 0: sol_c1 = [(-b)/(2*a)]
            else:
                sol_c1 = [(-b + np.sqrt(det))/(2*a), (-b - np.sqrt(det))/(2*a)]
        solutions = []
        for c1 in sol_c1:
            if py != 0:
                sol_s1 = [(m-c1*px)/py]
            else:
                tmp = np.sqrt(1 - np.square(c1))
                sol_s1 = [tmp, -tmp]
            for s1 in sol_s1:
                theta1 = np.arctan2(s1, c1)
                c12 = (px - self.l1*c1)/self.l2
                s12 = (py - self.l1*s1)/self.l2
                theta2 = np.arctan2(s12, c12) - theta1
                c123 = frame[0, 0]
                s123 = frame[1, 0]
                theta3 = np.arctan2(s123, c123) - theta1 - theta2
                solutions.append(normalize_angle(np.rad2deg(np.array([theta1, theta2, theta3]))))
        return solutions

    def to_dh_mat(self, theta):
        """
        construct the DH matrix
        :param theta: 3 angles
        :return: DH matrix
        """
        dh = np.zeros((3, 4))
        dh[1, 1] = self.l1
        dh[2, 1] = self.l2
        dh[:3, 3] = theta
        return dh

    def forward_kinematics(self, theta):
        """
        :param theta: 3 angles
        :return: final frame
        """
        dh = self.to_dh_mat(theta)
        return mult_step_trans(dh)

    def where(self, theta):
        """
        :param theta: 3 angles
        :return: (x, y, phi)
        """
        frame = self.forward_kinematics(theta)
        return np.array([frame[0,3], frame[1,3], np.rad2deg(np.arctan2(frame[1, 0], frame[0,0]))])

    def what_frame(self, loc):
        """
        :param loc: (x, y, phi)
        :return: frame(4*4)
        """
        frame = np.identity(4)
        phi = np.deg2rad(loc[2])
        c123 = np.cos(phi)
        s123 = np.sin(phi)
        frame[0, 0] = c123
        frame[1, 1] = c123
        frame[0, 1] = -s123
        frame[1, 0] = s123

        frame[:2, 3] = loc[:2]
        return frame


if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    current = np.array([0, 0, 0])
    robot = Planar3D()
    configures = [(0, 0, -90), (0.6, -0.3, 45), (-0.4, 0.3, 120), (0.8, 1.4, 30)]
    for loc in configures:
        print "==============================================================================================="
        print "Gripper location:"
        print loc
        frame = robot.what_frame(loc)

        print "WHATFRAME: "
        print frame
        sols = robot.inverse_kinematics(frame, current)
        print ""
        print "Inverse kinematics: "
        if sols is None:
            print "No solutions!"
        else:
            print "The found solutions are:"
            if len(sols) > 1:
                print "[Near, Far]:",
            print sols
            print ""
            print "WHERE:"
            for theta in sols:
                print robot.where(theta)
        print "==============================================================================================="



