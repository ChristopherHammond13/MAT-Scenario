from __future__ import absolute_import
import json
from itertools import imap

class parser(object):

    def __init__(self):
        self._valid = None
        self.index = 0

    def is_valid(self):
        return self._valid

    # Converts coord (as 2-tuple) to dict.
    def coord_to_dict(self, coord):
        return {
            u'x': coord[0],
            u'y': coord[1]
        }

    # Converts list of coords (2-tuple) to list of dicts
    def coords_to_dicts(self, coords):
        return list(imap(lambda x : self.coord_to_dict(x), coords))


class input_parser(parser):

    def __init__(self):
        self.robots = []
        self.polygons = []
        super(input_parser, self).__init__()

    def parse_robots(self, robot_str):
        robot_str = robot_str.replace(u"),(", u");(")
        robot_coords = robot_str.split(u";")
        for coord in robot_coords:
            coord = coord.replace(u"(", u"")
            coord = coord.replace(u")", u"")
            self.robots.append((float(coord.split(u",")[0]), float(coord.split(u",")[1])))

    def parse_polygons(self, poly_str):
        polygons = poly_str.split(u";")
        for poly_str in polygons:
            poly_str = poly_str.replace(u"),(", u");(")
            coords = poly_str.split(u";")
            poly = []
            for coord in coords:
                coord = coord.replace(u"(", u"")
                coord = coord.replace(u")", u"")
                poly.append((float(coord.split(u",")[0]), float(coord.split(u",")[1])))
            self.polygons.append(poly)

    def parse(self, input):
        self.robots = []
        self.index = 0
        self.polygons = []
        self._valid = None
        try:
            input = input.replace(u" ",u"")
            self.index = int(input.split(u":")[0])
            rest = input.split(u":")[1]
            robot_str = rest.split(u"#")[0]
            self.parse_robots(robot_str)
            if len(rest.split(u"#"))>1:
                poly_str = rest.split(u"#")[1]
                self.parse_polygons(poly_str)

            self._valid = True
        except Exception:
            self._valid = False


    def to_json(self):
        if not self._valid:
            raise Exception(u"Input not valid")
        output = {
            u'index': self.index,
            u'robots': self.coords_to_dicts(self.robots),
            u'polygons': list(imap(lambda x : self.coords_to_dicts(x), self.polygons))
        }
        return json.dumps(output, ensure_ascii=False)

class output_parser(parser):

    def __init__(self):
        self.paths = []
        super(output_parser, self).__init__()

    def parse_paths(self, path_str):
        paths = path_str.split(u";")
        for path_str in paths:
            path_str = path_str.replace(u"),(", u");(")
            coords = path_str.split(u";")
            path = []
            for coord in coords:
                coord = coord.replace(u"(",u"")
                coord = coord.replace(u")", u"")
                path.append((float(coord.split(u",")[0]), float(coord.split(u",")[1])))
            self.paths.append(path)

    def parse(self, input):
        self.paths = []
        self.index = 0
        self._valid = None
        try:
            input = input.replace(u" ",u"")
            self.index = int(input.split(u":")[0])
            path_str = input.split(u":")[1]
            self.parse_paths(path_str)
            self._valid = True
        except Exception:
            self._valid = False

    def to_json(self):
        if not self._valid:
            raise Exception(u"Input is not valid!")
        output = {
            u'index': self.index,
            u'paths': list(imap(lambda x : self.coords_to_dicts(x), self.paths))
        }
        return json.dumps(output, ensure_ascii=False)
