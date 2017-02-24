import json

class parser():

    def __init__(self):
        self._valid = None
        self.index = 0

    def is_valid(self):
        return self._valid

    # Converts coord (as 2-tuple) to dict.
    def coord_to_dict(self, coord):
        return {
            'x': coord[0],
            'y': coord[1]
        }

    # Converts list of coords (2-tuple) to list of dicts
    def coords_to_dicts(self, coords):
        return list(map(lambda x : self.coord_to_dict(x), coords))


class input_parser(parser):

    def __init__(self):
        self.robots = []
        self.polygons = []
        super().__init__()

    def parse_robots(self, robot_str):
        robot_str = robot_str.replace("),(", ");(")
        robot_coords = robot_str.split(";")
        for coord in robot_coords:
            coord = coord.replace("(", "")
            coord = coord.replace(")", "")
            self.robots.append((float(coord.split(",")[0]), float(coord.split(",")[1])))

    def coords_are_clockwise(self, coords):
        sum = 0
        for i, coord in enumerate(coords):
            next_coord = (0.0,0.0)
            try:
                next_coord = coords[i+1]
            except Exception:
                pass
            sum += (next_coord[0] - coord[0])*(next_coord[1] + coord[1])
        return sum > 0

    def parse_polygons(self, poly_str):
        polygons = poly_str.split(";")
        for poly_str in polygons:
            poly_str = poly_str.replace("),(", ");(")
            coords = poly_str.split(";")
            poly = []
            for coord in coords:
                coord = coord.replace("(", "")
                coord = coord.replace(")", "")
                poly.append((float(coord.split(",")[0]), float(coord.split(",")[1])))
            if not self.coords_are_clockwise(poly):
                poly.reverse()
            self.polygons.append(poly)

    def parse(self, input):
        self.robots = []
        self.index = 0
        self.polygons = []
        self._valid = None
        try:
            input = input.replace(" ","")
            self.index = int(input.split(":")[0])
            rest = input.split(":")[1]
            robot_str = rest.split("#")[0]
            self.parse_robots(robot_str)
            if len(rest.split("#"))>1:
                poly_str = rest.split("#")[1]
                self.parse_polygons(poly_str)

            self._valid = True
        except Exception:
            self._valid = False


    def to_json(self):
        if not self._valid:
            raise Exception("Input not valid")
        output = {
            'index': self.index,
            'robots': self.coords_to_dicts(self.robots),
            'polygons': list(map(lambda x : self.coords_to_dicts(x), self.polygons))
        }
        return json.dumps(output, ensure_ascii=False)

    # Prints out the contents of the .environmennt file.
    def print_environment(self):
        output = "// OUTER BOUNDARY\n-1000.0  -1000.0\n1000.0  -1000.0\n1000.0  1000.0\n-1000.0  1000.0\n"
        for polygon in self.polygons:
            output = output + "// Polygon x-y coords listed anticlockwise\n"
            for coord in polygon:
                output = output + "{0}  {1}\n".format(coord[0], coord[1])
        return output

    def print_guards(self):
        output = "// Robots x-y\n"
        for robot in self.robots:
            output = output + "{0}  {1}\n".format(robot[0], robot[1])
        return output

class output_parser(parser):

    def __init__(self):
        self.paths = []
        super().__init__()

    def parse_paths(self, path_str):
        paths = path_str.split(";")
        for path_str in paths:
            path_str = path_str.replace("),(", ");(")
            coords = path_str.split(";")
            path = []
            for coord in coords:
                coord = coord.replace("(","")
                coord = coord.replace(")", "")
                path.append((float(coord.split(",")[0]), float(coord.split(",")[1])))
            self.paths.append(path)

    def parse(self, input):
        self.paths = []
        self.index = 0
        self._valid = None
        try:
            input = input.replace(" ","")
            self.index = int(input.split(":")[0])
            path_str = input.split(":")[1]
            self.parse_paths(path_str)
            self._valid = True
        except Exception:
            self._valid = False

    def to_json(self):
        if not self._valid:
            raise Exception("Input is not valid!")
        output = {
            'index': self.index,
            'paths': list(map(lambda x : self.coords_to_dicts(x), self.paths))
        }
        return json.dumps(output, ensure_ascii=False)
