import pyvisgraph as vg
import math
from multiprocessing import cpu_count


class vis_graph:

    def __init__(self, index, points, obstacles):
        self.index = index
        self.points = points
        obstacle_points = []
        for o in obstacles:
            ob = []
            for p in o:
                ob.append(vg.Point(p[0], p[1]))
            obstacle_points.append(ob)
        _g = vg.VisGraph()
        _g.build(obstacle_points, workers=cpu_count())
        self._g = _g

    def get_shortest_path(self, start, destination):
        return self._g.shortest_path(start, destination)

    def __lt__(self, point):
        return self.x + self.y < point.x + point.y

    def get_shortest_path_length(self, start, destination):
        shortest_path = self.get_shortest_path(start, destination)

        path_length = 0.0

        for i in range(0, len(shortest_path) - 1):
            path_length += math.sqrt(
                math.pow(shortest_path[i+1].x-shortest_path[i].x, 2) +
                math.pow(shortest_path[i+1].y - shortest_path[i].y, 2))

        return path_length
