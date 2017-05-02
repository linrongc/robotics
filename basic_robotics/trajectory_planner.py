#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 3/21/2017 12:23 PM
@author = Rongcheng
"""
import numpy as np
from inverse_kinematics import Planar3D


def cubic_coefficients(org_pos, dest_pos, org_velocity, dest_velocity, time):
    """
    :param org_pos: the original position
    :param dest_pos: the destination position
    :param org_velocity: the original velocity
    :param dest_velocity: the destination velocity
    :param time: duration
    :return: [a_0, a_1, a_2, a_3]
    """
    return [org_pos,  # a_0
            org_velocity,  # a_1
            3.0 / np.square(time) * (dest_pos - org_pos) - 1.0 / time * (2 * org_velocity + dest_velocity),  # a_2
            -2.0 / np.power(time, 3) * (dest_pos - org_pos) + 1.0 / np.square(time) * (org_velocity + dest_velocity)  # a_3
            ]


def cubic_path(via_pos, seg_duration, org_velocity=0., dest_velocity=0.):
    """
    :param via_pos: 1 dimensional position
    :param seg_duration: segment duration
    :param org_velocity: original velocity
    :param dest_velocity: destination velocity
    :return: cubic coefficient for each segmentation
    """
    ave_velocity = []
    for i in range(len(seg_duration)):
        ave_velocity.append((via_pos[i+1] - via_pos[i])/seg_duration[i])

    velocity = [org_velocity]
    for i in range(len(seg_duration) - 1):
        if ave_velocity[i]*ave_velocity[i+1] < 0:
            velocity.append(0.)
        else:
            velocity.append((ave_velocity[i] + ave_velocity[i+1])/2.)
    velocity.append(dest_velocity)
    coefficients = []
    for i in range(len(seg_duration)):
        coefficients.append(cubic_coefficients(via_pos[i], via_pos[i+1], velocity[i], velocity[i+1], seg_duration[i]))
    return coefficients


def cubic_trajectory_generator(time, cubic_par):
    """
    :param time: t
    :param cubic_par: cubic coefficients [a_0, a_1, a_2, a_3]
    :return: [q, qdot, qddot]
    """
    q = cubic_par[0] + cubic_par[1] * time + cubic_par[2]*np.square(time) + cubic_par[3] * np.power(time, 3)
    qdot = cubic_par[1] + 2*cubic_par[2]*time + 3*cubic_par[3]*np.square(time)
    qddot = 2*cubic_par[2] + 6*cubic_par[3]*time
    return [q, qdot, qddot]


class TrajectoryPlanner:

    def __init__(self, manipulator):
        self.manipulator = manipulator

    def get_config_pos(self, via_pos):
        """
        :param via_pos: end effect position&angle
        :return: joint angle array
        """
        config_pos = []
        for pos in via_pos:
            frame = self.manipulator.what_frame(pos)
            if len(config_pos) == 0:
                current = None
            else:
                current = config_pos[-1]
            config = self.manipulator.inverse_kinematics(frame, current_theta=current)
            if config is None:
                raise Exception("can't reach the position: "+str(pos))
            config_pos.append(config[0])  # choose the closest solution
        return config_pos

    def plan_cubic_trajectory(self, via_pos, seg_duration):
        """
        :param via_pos: end_effect position & angle
        :param seg_duration: segment duration
        :return: cubic coefficients for each joint
        """
        config_pos = self.get_config_pos(via_pos)
        joint_coefficients = []
        for joint_pos in zip(*config_pos):
            joint_coefficients.append(cubic_path(joint_pos, seg_duration))
        return np.array(joint_coefficients)

    def cubic_generate_trajectory(self, joint_coefficients, seg_duration, time_slot=0.2):
        """
        :param joint_coefficients: joint coefficients
        :param seg_duration: segmentation duration
        :param time_slot: 1.0/frequency
        :return: trajectory for each joint
        """
        acc_time = [0]
        for duration in seg_duration:
            acc_time.append(acc_time[-1] + duration)
        joint_trajectory = []
        for joint_coef in joint_coefficients:
            seg = 0
            trajectory = []
            for t in np.arange(0, acc_time[-1]+time_slot, time_slot):
                if t > acc_time[seg+1]:
                    seg += 1
                par = cubic_trajectory_generator(t-acc_time[seg], joint_coef[seg])
                trajectory.append(par)
            joint_trajectory.append(trajectory)
        return np.array(joint_trajectory)

    def end_effect_trajectory(self, joint_pos_trajectory):
        """
        :param joint_pos_trajectory: position trajectory for each joint
        :return: end effector trajectory
        """
        pos_list = []
        for joint_pos in zip(*joint_pos_trajectory):
            pos = self.manipulator.where([x[0] for x in joint_pos])
            pos_list.append(pos)
        return np.array(pos_list)

if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    knot_points = np.array([(0.758, 0.173, 0.), (0.6, -0.3, 45.0), (-0.4, 0.3, 120), (0.758, 0.173, 0.0)])
    seg_duration = np.array([3.]*3)
    print "knot points: "
    print knot_points
    print "segment durations: "
    print seg_duration
    robot = Planar3D()
    planner = TrajectoryPlanner(robot)

    joint_coefficients = planner.plan_cubic_trajectory(knot_points, seg_duration)
    print "===================================================================================="
    print "CUBIC COEFFICIENTS"
    print "===================================================================================="
    for name, coefficient in zip(["theta_1", "theta_2", "theta_3"], joint_coefficients):
        print name
        print "[a_0  a_1  a_2  a_3]"
        print coefficient
        print "-------------------------------------------------------------------"
    print "====================================================================================="

    print "\n\n\n\n"

    joint_trajectory = planner.cubic_generate_trajectory(joint_coefficients, seg_duration, time_slot=0.2)
    print "====================================================================================="
    print "JOINT TRAJECTORY"
    print "====================================================================================="
    for name, trajectory in zip(["theta_1", "theta_2", "theta_3"], joint_trajectory):
        print name
        print "45 Rows of [position, velocity, acceleration]"
        print trajectory
        print "-------------------------------------------------------------------"
    print "====================================================================================="
    print "\n\n\n\n"


    end_effect_trajectory = planner.end_effect_trajectory(joint_trajectory)
    print "====================================================================================="
    print "END EFFECTOR TRAJECTORY"
    print "====================================================================================="
    print "time, [x, y, phi]"
    for t, pos in zip(np.arange(0, 9.2, 0.2), end_effect_trajectory):
        print "%.1fs" % t, ",", pos
    print "====================================================================================="