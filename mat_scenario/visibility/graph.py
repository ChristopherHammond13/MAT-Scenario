import pyvisgraph as vg
from multiprocessing import cpu_count
from os.path import exists as path_exists

class Map:

    def __init__(self, index, points, obstacles):
        self.index = index
        self.points = points
        obstacle_points = []
        for o in obstacles:
            ob = []
            for p in o:
                ob.append(vg.Point(p[0], p[1]))
            obstacle_points.append(ob)
        g = vg.VisGraph()
        g.build(obstacle_points, workers=cpu_count())
