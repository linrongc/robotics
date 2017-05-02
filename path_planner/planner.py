#! /usr/bin/env python
# -*- coding: utf-8 -*- 
"""
@time = 4/27/2017 9:31 PM
@author = Rongcheng
"""
from calculator import *


class PotentialPlanner:

    def __init__(self):
        self.circle_obstacles = []
        self.rectangle_obstacles = []
        self.sources = []
        self.goals = []
        self.par_dic = {}
        self.accept_zone = 0.
        self.goal_calculator = LinearCalculator()
        self.circle_calculator = CircleCalculator()
        self.rect_calculator = RectangleCalculator()

        self.calculator_dic = {}

    def reload_calculator_dic(self):
        self.calculator_dic = {"circle_obstacle":[self.circle_obstacles, self.circle_calculator],
                           "rectangle_obstacle":[self.rectangle_obstacles, self.rect_calculator],
                           "goal":[self.goals, self.goal_calculator],
                           "source":[[pos[:2] + [self.par_dic["ball_size"]] for pos in self.sources], self.circle_calculator]
                           }

    def calculate_force(self, pos):
        force = np.array((0., 0.))
        r = self.par_dic["resolution"]
        for name, (objects, calculator) in self.calculator_dic.iteritems():
            if name == "source":
                continue
            for obj_par in objects:
                force += calculator.get_force(np.array(obj_par)/r, np.array(pos + [self.par_dic["ball_size"]])/r)
        return force

    def calculate_potential(self, pos):
        potential = 0.
        r = self.par_dic["resolution"]
        for objects, calculator in self.calculator_dic.values():
            for obj_par in objects:
                potential += calculator.get_potential(np.array(obj_par)/r, np.array(pos + [self.par_dic["ball_size"]])/r)
        return potential

    def load_configuration(self, config):
        self.circle_obstacles = config["circle_obstacles"]
        self.rectangle_obstacles = config["rectangle_obstacles"]
        self.sources =config["sources"]
        self.goals = config["goals"]
        self.par_dic = {key:value for (key, value) in config["parameter"]}
        self.circle_calculator.alpha = self.par_dic["alpha"]
        self.rect_calculator.alpha = self.par_dic["alpha"]
        self.accept_zone = self.par_dic["resolution"]
        if len(self.goals) > 0:
            self.goal_calculator.slope = self.par_dic["attract"] / len(self.goals)
        self.reload_calculator_dic()

    def update_source_dic(self, pos):
        self.calculator_dic["source"][0] = [p[:2] + [self.par_dic["ball_size"]] for p in pos]

    def get_nearest_dis(self, pos):
        if len(self.goals) > 0:
            nearest = euclidean(np.array(self.goals[0][:2]), np.array(pos[:2]))
            for n in range(1, len(self.goals)):
                dis = euclidean(np.array(self.goals[n][:2]), np.array(pos[:2]))
                if dis < nearest:
                    nearest = dis
            return nearest
        else:
            return None

    def generate_path(self):
        path = [[sour[:2] for sour in self.sources]]
        move = 10
        delta = self.par_dic["stride"] * self.par_dic["resolution"]
        count = 0
        while move > 1e-3 and count < 1000:
            move = 0
            sour_pos = path[-1]
            forces = [self.calculate_force(pos) for pos in sour_pos]
            dest_pos = []
            for s_pos, s_f in zip(sour_pos, forces):
                nearest = self.get_nearest_dis(s_pos)
                if nearest < self.accept_zone:
                    new_pos = s_pos
                else:
                    new_pos =[p + delta*f for p, f in zip(s_pos, s_f)]
                    move += euclidean(np.array(new_pos), np.array(s_pos))
                dest_pos.append(new_pos)
            # print forces
            count += 1
            self.update_source_dic(dest_pos)
            path.append(dest_pos)
        return path

    def get_potential_field(self):
        ticks = np.linspace(0, 800, 800/self.par_dic["resolution"])
        num_ticks = len(ticks)
        potential = np.zeros((num_ticks, num_ticks), dtype=np.float64)
        for i in range(num_ticks):
            for j in range(num_ticks):
                potential[i][j] = self.calculate_potential([ticks[i], ticks[j]])
        return potential


if __name__ == "__main__":
    import json
    planner = PotentialPlanner()
    with open("ai.json", "r") as f:
        planner.load_configuration(json.load(f))
    # planner.generate_path()
    potential = planner.get_potential_field()
    print potential
