#!/usr/bin/python

from visibility import graph
import pyvisgraph as vg
from utils import parser
from collections import deque
import sys
import math
import getopt
import os.path


def main(argv):
    '''
    Parses command line args and calls appropriate function
    '''
    input_file = ""
    output_file = ""
    help_string = "Usage: main.py -n <number_to-run> -a <algorithm> -i <input_file> -o \
            <output_file>"

    try:
        opts, _ = getopt.getopt(argv, "hn:a:i:o:", ["number=", "algorithm=",
                                                    "ifile=", "ofile="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)

    algorithm = default_schedule
    number = 30

    for opt, arg in opts:
        if opt == "-h":
            print(help_string)
            sys.exit()
        elif opt in ("-n", "--number"):
            number = int(arg)
        elif opt in ("-a", "--algorithm"):
            if arg == "greedy-claim":
                algorithm = greedy_claim_schedule
            elif arg == "greedy-dynamic":
                algorithm = greedy_dynamic_schedule
            else:
                print("Algorithm: " + str(arg) + " does not exist, use \
                      greedy-claim, greedy-dynamic or omit the option \
                      for the default")
                sys.exit(1)
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    if not os.path.isfile(input_file):
        print("Input file does not exist")
        sys.exit(1)

    if output_file == "":
        output_file = "output.mat"

    if os.path.isfile(output_file):
        print("Specified output file already exists")
        sys.exit(1)

    try:
        problemset_file = open(input_file)
        print("Opened " + input_file)
    except IOError:
        print("Unable to open input file")
        sys.exit(1)

    solve(problemset_file, algorithm, number)


def solve(problemset_file, algorithm, number):
    """
    Solves a problem given to it
    """
    _parser = parser.input_parser()
    parsed_string = "Problems parsed: "
    """
    Our problems are stored in a map<int, (robots:[point],polygons:[[point]])>
    """
    problemset = {}

    for problem in problemset_file:
        _parser.parse(problem)
        parsed_string += str(_parser.index) + ";"
        problemset[_parser.index] = (_parser.robots, _parser.polygons)

    print(parsed_string)

    """
    # for debugging
    for i in range(1, 5):
        print(str(problemset[i]))
    """

    for i in range(1, number):
        # reset these trackers
        global awake
        awake = {}
        global claimed
        claimed = {}
        global distance_to_travel
        distance_to_travel = {}
        global stopped
        stopped = set([])
        # a solution is our list of paths
        solution = []
        problem = problemset[i]
        robots = problem[0]
        obstacles = problem[1]

        # get the wakeup order for the problem
        schedule = algorithm(problem)
        first_robot = schedule.popleft()
        awake[robots.index(first_robot)] = first_robot
        # get the visibility graph
        try:
            _vis_graph = graph.vis_graph(i, robots, obstacles)
        except ValueError:
            _vis_graph = None

        # perform simulation
        simulationRunning = True
        while simulationRunning:
            simulationRunning = False
            for robot in robots:
                if robots.index(robot) not in awake.keys():
                    simulationRunning = True
                    break

            # update positions
            remaining_movement = 10.0
            while (remaining_movement > 0):
                # find distance to closest target
                next_robot_id = None
                min_distance = 9999

                for robot in robots:
                    robot_id = robots.index(robot)
                    if ((robot_id in awake.keys())
                        and (robot_id not in claimed.keys())
                       and (len(schedule) == 0)):
                        stopped.add(robot_id)
                        print("Robots stopped: " + str(stopped))
                    if ((robot_id in awake.keys())
                        and (robot_id not in claimed.keys())
                       and (len(schedule) > 0)):
                        try:
                            next_target = schedule.popleft()
                            claimed[robot_id] = next_target
                            if _vis_graph is not None:
                                min_len = _vis_graph.get_shortest_path_length(
                                    vg.Point(awake[robot_id][0], awake[robot_id][1]),
                                    vg.Point(next_target[0], next_target[1]))
                            else:
                                min_len = math.sqrt(
                                    math.pow(awake[robot_id][0]
                                             - claimed[robot_id][0], 2) +
                                    math.pow(awake[robot_id][1]
                                             - claimed[robot_id][1], 2))

                            # need to put robot in distance_to_travel with its
                            # distance
                            print("Distance between " + str(robot) + " and " + str(next_target) + " is " + str(min_len))
                            distance_to_travel[robot_id] = min_len

                        except IndexError:
                            stopped.add(robot_id)
                            print("Robot stopped: " + str(stopped))
                    if (robot_id in awake.keys()) and (robot_id not in stopped):
                        if distance_to_travel[robot_id] < min_distance:
                            min_distance = distance_to_travel[robot_id]
                            next_robot_id = robot_id

                # if no robot close enough to awaken
                if min_distance > remaining_movement:
                    move_bots(remaining_movement)
                    remaining_movement = 0

                # if a robot close enough to awaken
                if min_distance <= remaining_movement:
                    move_bots(min_distance)
                    remaining_movement -= min_distance

                    # set target
                    wakeup_target = claimed[next_robot_id]
                    wakeup_id = robots.index(wakeup_target)
                    # wake target
                    awake[wakeup_id] = wakeup_target
                    print("Woke up " + str(wakeup_id))

                    # free up the waker
                    del claimed[next_robot_id]

                    # here we need to do something about forming the path

        print("Problem " + str(i) + "done")


def move_bots(distance):
    """
    Moves the robots
    """
    print("Move bots")
    for robot_id in awake.keys():
        if robot_id not in stopped:
            # Move robot to target along x axis
            new_x = awake[robot_id][0] + ((claimed[robot_id][0] -
                                          awake[robot_id][0]) * distance /
                                          distance_to_travel[robot_id])
            # Move robot to target along y axis
            new_y = awake[robot_id][1] + ((claimed[robot_id][1] -
                                          awake[robot_id][1]) * distance /
                                          distance_to_travel[robot_id])
            awake[robot_id] = (new_x, new_y)
            print("New robot " + str(robot_id) + " position: " + str(awake[robot_id]))
            # Update distance left to travel
            distance_to_travel[robot_id] -= distance


def default_schedule(problem):
    """
    Default schedule algorithm
    """
    _schedule = deque()
    print(str(problem))
    for robot in problem[0]:
        print("Adding " + str(robot))
        _schedule.append(robot)

    return _schedule


def greedy_claim_schedule(problem):
    """
    Greedy claim schedule algorithm
    """


def greedy_dynamic_schedule(problem):
    """
    Greedy dynamic schedule algorithm
    """


if __name__ == '__main__':
    main(sys.argv[1:])
