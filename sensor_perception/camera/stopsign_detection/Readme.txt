Stop sign detection based on OpenCV haarcascade LBP detector. Node is written in c++ and OpenCV Cuda library for GPU acceleration. The code has been tested on Nvidia TK1 with ROS Indigo and Ubuntu 14.04.


## How to build ##

copy the packge source folder to <your/work/space/src>.

$ cd <your/work/space>
$ catkin_make --pkg stopsign_detection

## How to run ##

$ rosrun stopsign_detection stopsign_detection_node </path/to/stop/sign/detector/xml/flie> <0/1: display off/on>

or:

$ roslaunch stopsign_detection stopsign_detection.launch

## You could switch display on/off in launch file ##
  Display on:
  <arg name="display" value="1" />
  Display off:
  <arg name="display" value="0" />
