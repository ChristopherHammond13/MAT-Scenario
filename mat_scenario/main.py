#!/usr/bin/python

from visibility import graph
from utils import parser
from collections import deque
import sys
import getopt
import os.path


awake = []
claimed = {}
distance_to_travel = {}


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
            number = arg
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
        awake = []
        claimed = {}
        distance_to_travel = {}
        # a solution is our list of paths
        solution = []
        problem = problemset[i]
        robots = problem[0]
        obstacles = problem[1]

        # get the wakeup order for the problem
        schedule = algorithm(problem)
        awake.append(schedule.popleft())
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
                if robot not in awake:
                    simulationRunning = True
                    break

            # update positions
            remaining_movement = 1.0
            while (remaining_movement > 0):
                # find distance to closest target
                next_robot = None
                min_distance = 9999

                for robot in robots:
                    if ((robot in awake) and (robot not in claimed)
                       and (len(schedule) == 0)):
                        print("Robot stopped")
                    if ((robot in awake) and (robot not in claimed)
                       and (len(schedule) > 0)):
                        try:
                            next_target = schedule.popleft()
                            claimed[robot] = next_target
                            if _vis_graph is not None:
                                shortest_path = _vis_graph.get_shortest_path(
                                    robot, next_target)
                            else:
                                shortest_path = [(robot[0], robot[1]),
                                                 (claimed[robot][0],
                                                  claimed[robot][1])]
                            # need to put robot in distance_to_travel with its
                            # distance

                        except IndexError:
                            print("Robot stopped")
                    if robot in awake:
                        if distance_to_travel[robot] < min_distance:
                            min_distance = distance_to_travel[robot]
                            next_robot = robot

                # if no robot close enough to awaken
                if min_distance > remaining_movement:
                    move_bots(remaining_movement)
                    remaining_movement = 0

                # if a robot close enough to awaken
                if min_distance <= remaining_movement:
                    move_bots(min_distance)
                    remaining_movement -= min_distance

                    # set target
                    wakeup_target = claimed[next_robot]
                    # wake target
                    awake.append(wakeup_target)
                    # free up the waker
                    del claimed[next_robot]

                    # here we need to do something about forming the path


def move_bots(distance):
    """
    Moves the robots
    """
    for robot in awake:
        # Move robot x
        robot[0] += ((claimed[robot][0] - robot[0]) * distance /
                     distance_to_travel[robot])
        # Move robot y
        robot[1] += ((claimed[robot][1] - robot[1]) * distance /
                     distance_to_travel[robot])
        # Update distance left to travel
        distance_to_travel[robot] -= distance


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
