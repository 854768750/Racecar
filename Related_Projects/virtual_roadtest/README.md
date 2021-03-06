# VIRTUAL ROADTEST
A Race track generating tool that uses a genetic algorithm-based approach to test the performance of steering controllers deployed on simulation models of DEPEND lab's F1/10th platform

## Motivation
In order to deploy self driving cars into public roads, the onboard controller would have to provide sufficient evidence to prove its capability to :
  1) Calculate a path to a waypoint (in this case, a given waypoint)
  2) Perform the appropriate maneuvers required to follow calculated path

The virtual roadtest tool automates this testing process by generating multiple racetracks with incrementing difficulty with the objective to make the onboard controllers fail.

<img src="https://github.com/BU-DEPEND-Lab/Racecar/blob/master/Related_Projects/virtual_roadtest/sample_track.png" width="300">

For each test run, real time sensor data is collected to along with multiple other metrics such as completion time etc., for a fitness function that outputs a single fitness value from 0 to 1. The goal of this tool is to minimize the fitness value.

This value is used to determine the most difficult race track among a population of race tracks. After a mutation process, a new population of race tracks is then generated. This process is repeated for a predefined number of 'generations' of the racetrack population.

  
## Requirements
* OpenCV
* setptoctitle:

``` pip install setproctitle ```

* psutil:

``` sudo apt-get install gcc python-dev python-pip ```

``` pip install psutil ```

* All requirements mentioned for F1/10 simulation

## To Run
* to use gazebo headless, set the "gui" argument in racecar_tunnel.launch to "false"


### To compile the planner:

``` g++ -std=c++0x -ggdb `pkg-config --cflags opencv` -o `basename Planning_Gazebo_Customized.cpp .cpp` Planning_Gazebo_Customized.cpp `pkg-config --libs opencv` ```


### To compile map_generator.cpp

``` g++ -std=c++0x -ggdb `pkg-config --cflags opencv` -o `basename map_generator.cpp .cpp` map_generator.cpp `pkg-config --libs opencv` ```

### Start the tool
After setting the populationSize, generations , mutationRate variables in 'genetic_alg.py', execute the following:

``` python genetic_alg.py ```



## Useful commands and notes

### to run the map_generator
* args are line_l, line_w, joint_radius, num_joints, 15 joint angles
* currently, include all 15 joint angles, even if num_joint < 15

e.g: 
``` ./map_generator  40 20 10 14 2 2 -2 2 2.5 -2.1 1 1.5 1.0 1.3 2.3 2.2 2.1 -1.5 -1.5```

### to use RVIZ 

roscd hector_slam_launch/launch
sudo gedit tutorial.launch

uncomment the command for executing rviz

# compile the controller

``` /home/f1/radler/radler.sh --ws_dir /home/f1/catkin_ws/src compile pid_controller.radl --ROS ```


* To compile the planner:

``` g++ -std=c++0x -ggdb `pkg-config --cflags opencv` -o `basename Planning_Gazebo_Customized_GA_version.cpp .cpp` Planning_Gazebo_Customized_GA_version.cpp `pkg-config --libs opencv` ```


* To compile the pid controller:

``` catkin_make ```


* modify pid_controller.cpp under:

``` ~/catkin_ws/src/race/src/radler/pure_pursuit/src/pid_controller.cpp ``` 

* the 'main' function for the radler system is under:

``` ~/catkin_ws/src/ros/pid_controller/src/radl__pid_controller.cpp ```
