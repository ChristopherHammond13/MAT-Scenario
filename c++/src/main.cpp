/*
=========A VisiLibity Example Program=========
This program provides a text interface which will

(1) read an environment and guard locations from files given as
command line arguments,

(2) check the geometric validity of these inputs (edges of the
environment do not cross each other, guards are contained in the
environment, etc.),

(3) display environment and guards' data and statistics, and

(4) compute and display the visibility polygon of a guard chosen by
    the user.

The environment representation and the guard locations can be read
from any files in the (human-readable) format demonstrated in
example.environment and example.guards.

Instructions: use the accompanying makefile to compile, then from
command line run
./main [environment file] [guards file]
,e.g., using the example files included with your VisiLibity download,
./main example.environment example.guards
*/

#include "visilibity.hpp"  //VisiLibity header file
#include <cmath>         //Puts math functions in std namespace
#include <cstdlib>       //Gives rand, srand, exit
#include <ctime>         //Gives Unix time
#include <fstream>       //File I/O
#include <iostream>      //std I/O
#include <cstring>       //Gives C-string manipulation
#include <string>        //Gives string class
#include <iomanip>       // Precision setting!
#include <sstream>       //Gives string streams
#include <vector>        //std vectors
#include <map>           //std map
#include <set>           //std set
#include <deque>         //std deque
#include <utility>       //utility for std pair
//#define NDEBUG           //Turns off assert.
#include <cassert>


//ASCII escape sequences for colored terminal text.
std::string alert("\a");       //Beep
std::string normal("\x1b[0m"); //Designated fg color default bg color
std::string red("\x1b[31m");         
std::string red_blink("\x1b[5;31m");
std::string black("\E[30;47m");
std::string green("\E[32m");
std::string yellow("\E[33;40m");
std::string blue("\E[34;47m");
std::string magenta("\x1b[35m");
std::string cyan("\E[36m");
std::string white_bold("\E[1;37;40m");
std::string clear_display("\E[2J");
    
std::map<unsigned, VisiLibity::Point> awake;
std::map<unsigned, VisiLibity::Point> claimed;
std::map<unsigned, double> distance_to_travel;
std::set<unsigned> stopped;

void solve(VisiLibity::Environment, VisiLibity::Guards, double epsilon);
void solve(VisiLibity::Environment, VisiLibity::Guards, double);
void move_bots(double distance);

//=========================Main=========================//
int main(int argc, char *argv[])
{

  //Check input validity
  if(argc > 3){
    std::cerr << "Error: too many input arguments" << std::endl;
    exit(1);
  }


  //Set iostream floating-point display format
  const int IOS_PRECISION = 10;
  std::cout.setf(std::ios::fixed);
  std::cout.setf(std::ios::showpoint);
  std::cout.precision(IOS_PRECISION);


  //Seed the rand() fnc w/Unix time
  //(only necessary once at the beginning of the program)
  std::srand( std::time( NULL ) ); rand();


  //Set geometric robustness constant
  //:WARNING: 
  //may need to modify epsilon for Environments with greatly varying
  //scale of features
  // Ilya Constant
  double epsilon = 0.000000001;
  std::cout << green << "The robustness constant epsilon is set to "
	    << epsilon << normal << std::endl;


  /*----------Load Geometry from Files----------*/


  //Load geometric environment model from file
  std::cout << "Loading environment file ";
  std::string environment_file(argv[1]);
  //Print environment filename to screen
  std::cout << environment_file << " . . . ";
  //Construct Environment object from file
  VisiLibity::Environment my_environment(environment_file);
  std::cout << green << "OK" << normal << std::endl;


  //Load guard positions from file
  std::cout << "Loading guards file ";
  std::string guards_file(argv[2]);
  //Print guards filename to screen
  std::cout << guards_file << " . . . ";
  //Construct Guards object from file
  VisiLibity::Guards my_guards(guards_file);
  std::cout << green << "OK" << normal << std::endl;


  /*----------Check Validity of Geometry----------*/


  //Check Environment is epsilon-valid
  std::cout << "Validating environment model . . . ";
  if(  my_environment.is_valid( epsilon )  )
    std::cout << green << "OK" << normal << std::endl;
  else{
    std::cout << std::endl << red << "Warning:  Environment model "
	      << "is invalid." << std::endl
	      << "A valid environment model must have" << std::endl
	      << "   1) outer boundary and holes pairwise "
	      << "epsilon -disjoint simple polygons" << std::endl
	      << "   (no two features should come "
	      << "within epsilon of each other)," << std::endl 
	      << "   2) outer boundary is oriented ccw, and" 
	      << std::endl
	      << "   3) holes are oriented cw."
	      << std::endl
	      << normal; 
    exit(1);
  }


  //Check Guards are all in the Environment
  std::cout << "Checking all robots are "
	    << "in the environment and noncolocated . . . ";
  my_guards.snap_to_boundary_of(my_environment, epsilon);
  my_guards.snap_to_vertices_of(my_environment, epsilon);
  for(unsigned i=0; i<my_guards.N(); i++){
    if( !my_guards[i].in(my_environment, epsilon) ){
      std::cout << std::endl << red 
		<< "Warning:  robot " << i 
		<< " not in the environment."
		<< normal << std::endl;
      exit(1);
    }
  }
  if( !my_guards.noncolocated(epsilon) ){
    std::cout << std::endl << red 
	      << "Warning:  Some robots are colocated." 
	      <<  normal << std::endl;
    exit(1);
  }
  else
    std::cout << green << "OK" << normal << std::endl;



  /*----------Print Data and Statistics to Screen----------*/

    /*
  //Environment data
  std::cout << "The environment model is:" << std::endl;
  std::cout << magenta << my_environment << normal;


  //Environment stats
  std::cout << "This environment has " << cyan 
	    << my_environment.n() << " vertices, " 
	    << my_environment.r() << " reflex vertices, " 
	    << my_environment.h() << " holes, "
	    << "area " << my_environment.area() << ", "
	    << "boundary length " 
	    << my_environment.boundary_length() << ", "
	    << "diameter " 
	    << my_environment.diameter() << "."
	    << normal << std::endl;


  //Guards data
  std::cout << "The guards' positions are:" << std::endl;
  std::cout << magenta << my_guards << normal;


  //Guards stats
  std::cout << "There are " << cyan << my_guards.N() 
	    << " guards." << normal << std::endl;
  */


  /*----------Compute the Visibility Polygon 
                   of a Guard Chosen by User----------*/
 
 
  //Prompt user
  /*
  int guard_choice(0);
  std::cout << "Which guard would you like "
	    <<"to compute the visibility polygon of "
	    << "(0, 1, 2, ...)? " << std::endl;
  std::cin >> guard_choice; std::cout << normal;

	 
  //Compute and display visibility polygon
  VisiLibity::Visibility_Polygon
    my_visibility_polygon(my_guards[guard_choice], my_environment, epsilon);
  std::cout << "The visibility polygon is" << std::endl
	    << magenta << my_visibility_polygon << normal
	    << std::endl;
  
  //To save the visibility polygon in an Environment file
  VisiLibity::Environment(my_visibility_polygon)
    .write_to_file("./example_visibility_polygon.cin", IOS_PRECISION);
  */

    solve(my_environment, my_guards, epsilon);

  return 0;
}

void solve(VisiLibity::Environment environment, VisiLibity::Guards robots, double epsilon) {
    std::cout << "Starting..." << std::endl;

    std::vector<VisiLibity::Polyline> solution;
    // Robot paths needed 
    std::vector<std::pair<unsigned, std::vector<VisiLibity::Point>>> robot_paths;

    std::deque<VisiLibity::Point> schedule;
    // Populate schedule
    for(unsigned i=0; i<robots.N(); i++){
        schedule.push_back(robots[i]);
        std::cout << "Added " << cyan << "Robot " << i
            << normal << " (" << robots[i] << ")"
            << " to the schedule."  
            << std::endl;
    }

    // TODO do we use this or does it work as is?
    VisiLibity::Visibility_Graph vg(robots, environment, epsilon);

    // Get the first robot from the schedule and pop it
    VisiLibity::Point first_robot = schedule.front();
    schedule.pop_front();
    // Wake the first robot
    awake[0] = first_robot;
    std::vector<VisiLibity::Point> init_path;
    init_path.push_back(first_robot);
    robot_paths.push_back(std::make_pair(0, init_path));

    bool simulation_running = true;
    // Perform simulation
    while (simulation_running) {
        simulation_running = false; 
        // Check if there is an asleep robot
        for (unsigned i=0; i<robots.N(); i++) {
            if (awake.find(i) == awake.end()) {
                simulation_running = true;
                break;
            }
        }
        if (!simulation_running) {
            std::cout << "They woke: " << red_blink;
            for (auto &woke : awake) {
                std::cout << woke.first << " ";
            }
            std::cout << normal << std::endl;
        }

        double remaining_movement = 0.5;
        while (remaining_movement > 0) {
            unsigned next_robot_id = 666;
            double min_distance = 10000;

            // Loop through robots
            for (unsigned i=0; i<robots.N(); i++) {
                // Stop robot if schedule empty
                if (awake.find(i) != awake.end() &&
                        claimed.find(i) == claimed.end() &&
                        stopped.find(i) == stopped.end() &&
                        schedule.empty()) {
                    stopped.insert(i); 
                }
                // If robot not claimed and is awake then assign them
                if (awake.find(i) != awake.end() &&
                        claimed.find(i) == claimed.end() && 
                        stopped.find(i) == stopped.end() &&
                        schedule.size() > 0) {
                    // Get the next target robot from the schedule and pop it
                    VisiLibity::Point next_target = schedule.front();
                    schedule.pop_front();

                    claimed[i] = next_target;
                    // get min_len from shortest_path
                    double min_len = environment.shortest_path(awake[i], next_target).length();
                     
                    distance_to_travel[i] = min_len;
                }
                // If robot awake and not stopped then check if distance 
                // to travel is less than min_distance
                if (awake.find(i) != awake.end() &&
                        stopped.find(i) == stopped.end()) {

                    std::map<unsigned, double>::iterator dtt_iter = distance_to_travel.find(i);
                    if (dtt_iter != distance_to_travel.end() &&
                            dtt_iter->second < min_distance) {
                        min_distance = dtt_iter->second;
                        next_robot_id = i;
                    }

                }
            }

            // If no robot is close enough to awaken then move them
            if (min_distance > remaining_movement) {
                move_bots(remaining_movement);
                remaining_movement = 0; // update remaining movement
            }

            // If a robot can awaken another then do so
            if (next_robot_id != 666 &&
                    min_distance <= remaining_movement) {
                move_bots(min_distance); 
                remaining_movement -= min_distance; // update remaining movement

                std::map<unsigned, VisiLibity::Point>::iterator next_robot_iter;
                next_robot_iter = claimed.find(next_robot_id);
                // Get the wakeup target
                VisiLibity::Point wakeup_target = next_robot_iter->second;
                unsigned wakeup_id;
                // Set the wakeup id by finding it in the robots
                for (unsigned i=0; i<robots.N(); i++) {
                    if (robots[i] == wakeup_target) {
                        wakeup_id = i;
                        break;
                    }
                }
                // Wake target
                awake[wakeup_id] = wakeup_target;

                // Add point of woken up robot to the path for the 
                // wakeup target
                std::vector<VisiLibity::Point> new_path;
                new_path.push_back(wakeup_target);
                robot_paths.push_back(std::make_pair(wakeup_id, new_path));

                for (auto &robot_path : robot_paths) {
                    if (next_robot_id == robot_path.first) {
                        robot_path.second.push_back(claimed[next_robot_id]);
                        std::cout << red_blink << "Pushing back" << std::endl;
                        break;
                    }
                }

                // Free up the waker
                claimed.erase(next_robot_iter);
            }
        }
    }
    
    // Loop through robot_paths to build the solution
    // using the shortest path around obstacles
    for (auto &robot_path : robot_paths) {
        std::cout << "Path" << std::endl;
        if (robot_path.second.size() > 1) {
            std::vector<VisiLibity::Point> full_path;    
            for (unsigned i=0; i<robot_path.second.size()-1; i++) {
                VisiLibity::Polyline path = environment.shortest_path(robot_path.second[i], robot_path.second[i+1]);
                for (unsigned j=0; j<path.size(); j++) {
                    full_path.push_back(path[j]);
                }
            }
            solution.push_back(full_path);
        }
    }
    // TODO Format the solution and print to stdout
    std::string solution_string = ""; 
    for (auto &path : solution) {
        unsigned i;
        std::ostringstream stream;
        for (i=0; i<path.size()-1;i++) {
            stream << "(" << std::setprecision(std::numeric_limits<double>::digits10) << path[i].x() << "," << path[i].y() << "),";
        }
        stream << "(" << std::setprecision(std::numeric_limits<double>::digits10) << path[i].x() << "," << path[i].y() << ")";
        solution_string.append(stream.str());
        solution_string.push_back(';');
    }
    
    solution_string.resize(solution_string.length()-1);

    std::cout << solution_string << std::endl;
}

// Moves the bots by a given distance 
void move_bots(double distance) {
    for (auto &robot : awake) {
        // If robot isn't in stopped then move iterator
        unsigned robot_id = robot.first;
        if (stopped.find(robot_id) == stopped.end()) {
            // Get new x position
            double new_x = awake[robot_id].x() + 
                (claimed[robot_id].x() - awake[robot_id].x()) *
                distance / distance_to_travel[robot_id];
            // Get new y position
            double new_y = awake[robot_id].y() + 
                (claimed[robot_id].y() - awake[robot_id].y()) *
                distance / distance_to_travel[robot_id];
            // Move
            awake[robot_id] = VisiLibity::Point(new_x, new_y);
            // Update dtt
            distance_to_travel[robot_id] -= distance;
        }
    }
}
