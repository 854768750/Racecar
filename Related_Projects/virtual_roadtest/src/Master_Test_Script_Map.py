#####################################################
# to compile radler based controller:
# /home/f1/radler/radler.sh --ws_dir /home/f1/catkin_ws/src compile ~/catkin_ws/src/race/src/radler/f1_tenth/f1_tenth.radl --ROS
#####################################################

#!/usr/bin/env python
import os
import subprocess
import sys
import time
import threading
import signal
import logging
from setproctitle import *
from os.path import expanduser
from os import listdir
import numpy as np

global fitness_value

setproctitle('master_test') # set process name for ROS to identify

TIMEALLOWED = 3000 # seconds -  change to a large number(e.g. 5 minutes) for actual tests
home = expanduser("~")

""" Clear all existing generated files"""

""" claculate fitness """

def CalculateFitness(metric1, metric2, metric3, metric4):
     fitness = np.mean([metric1 ,metric2, metric3, metric4])  
     return fitness
	
""" runs roslaunch file to implement test run in gazebo and terminates once the robot reaches its goal"""

def ROS():
    global fitness_value
    try:
        """ Execute child processes"""  
        cmd1 = 'roslaunch racecar_gazebo racecar_tunnel.launch'
        simulation1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
        ros_node_pid1 = os.getpgid(simulation1.pid)

        time.sleep(4)

        cmd2 = 'roslaunch hector_slam_launch tutorial.launch'
        simulation2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
        ros_node_pid2 = os.getpgid(simulation2.pid)
        
        time.sleep(10)
        cmd3 = '/' + home +'/catkin_ws/devel/lib/pid_controller/controller_gateway'
        simulation3 = subprocess.Popen(cmd3, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
        ros_node_pid3 = os.getpgid(simulation3.pid)
        
        time.sleep(5)

        cmd4 = '/' + home +'/catkin_ws/devel/lib/pid_controller/pid_controller'
        simulation4 = subprocess.Popen(cmd4, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
        ros_node_pid4 = os.getpgid(simulation4.pid)
  
  
        cmd5 = 'rosrun virtual_roadtest metrics_node.py'
        metrics_process = subprocess.Popen(cmd5, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
        ros_node_pid5 = os.getpgid(metrics_process.pid)
        (output,err)= metrics_process.communicate()  
  
  
  
        """ Kill child processes after TIMEOUT - Goal never reached"""  
        time.sleep(TIMEALLOWED)
        logging.info('FAIL - Timout - Goal not reached within 30 seconds...')

        subprocess.call('killall gzserver', shell=True)
    
        time.sleep(2)
        os.killpg(ros_node_pid1, signal.SIGTERM)  # Send the signal to all the process groups
        time.sleep(2)
        os.killpg(ros_node_pid2, signal.SIGTERM)  # Send the signal to all the process groups
        time.sleep(2)
        os.killpg(ros_node_pid3, signal.SIGTERM)  # Send the signal to all the process groups
        time.sleep(2)
        os.killpg(ros_node_pid4, signal.SIGTERM)  # Send the signal to all the process groups
  
        time.sleep(2)
        os.killpg(ros_node_pid5, signal.SIGTERM)  # Send the signal to all the process groups
        i = 1
        while True:
                line = metrics_process.stdout.readline()
                if line != '':
                # minDist
                    if (i == 1):
                        minDist = float(line.rstrip())
                    elif (i == 2):
                        maxSpeed = float(line.rstrip())
                    elif (i == 3):
                        AvgSpeed = float(line.rstrip())
                    elif (i == 4):
                        AvgSteering = float(line.rstrip())            
                    i += 1
                else:
                    break
        fitness_value = CalculateFitness(minDist, maxSpeed, AvgSpeed, AvgSteering)
        
    #""" Kill child processes after signal from Pure Pursuit Controller that GOAL has been reached"""      
    except KeyboardInterrupt:
        print "SUCCESS - KILL CALLED after receiving GOAL REACHED signal"
        subprocess.call('killall gzserver', shell=True)

        time.sleep(2)
        os.killpg(ros_node_pid1, signal.SIGTERM)  # Send the signal to all the process groups
        time.sleep(2)
        os.killpg(ros_node_pid2, signal.SIGTERM)  # Send the signal to all the process groups
        time.sleep(2)		
        os.killpg(ros_node_pid3, signal.SIGTERM)  # Send the signal to all the process groups
        time.sleep(2)
        os.killpg(ros_node_pid4, signal.SIGTERM)  # Send the signal to all the process groups
  
        time.sleep(2)
        os.killpg(ros_node_pid5, signal.SIGTERM)  # Send the signal to all the process groups
  
        i = 1
        while True:
            line = metrics_process.stdout.readline()
            if line != '':
                # minDist
                if (i == 1):
                    minDist = float(line.rstrip())
                elif (i == 2):
                    maxSpeed = float(line.rstrip())
                elif (i == 3):
                    AvgSpeed = float(line.rstrip())
                elif (i == 4):
                    AvgSteering = float(line.rstrip())            
                i += 1
                
            else:
                break
        fitness_value = CalculateFitness(minDist, maxSpeed, AvgSpeed, AvgSteering)
  
  
	print "Test run script - KILLED ALL"

	logging.info('Ending test run...')

def WorldGenerator(j1,j2,j3,j4,j5,j6,j7,j8,j9,j10,j11,j12,j13,j14,j15):
    os.chdir(home+'/catkin_ws/src/virtual_racetrack/virtual_roadtest/src/map')
    
    line_l = "40" # length of line segment
    line_w = "40" # width of line segment
    radius = "20" # radius of joint - keep same as half of line_w
    num_joints = "15"
    arguments = line_l + " " + line_w + " " + radius + " " + num_joints + " " + \
                str(j1) + " " + str(j2) + " " + str(j3) + " " +str(j4) + " " + \
                str(j5) + " " +  str(j6) + " " + str(j7) + " " + str(j8) + " " + \
                str(j9) + " " + str(j10) + " " + str(j11) + " " + str(j12) + " " + \
                str(j13) + " " + str(j14) + " " + str(j15)
    
    subprocess.call('./map_generator ' + arguments, shell=True) 
    logging.info('WorldGenerator ending...')


def PathGenerator():
	os.chdir(home+'/catkin_ws/src/race/src')
	subprocess.call('./Planning_Gazebo_Customized', shell=True)
	logging.info('Path Generated...')


# values for j1 - j15 come from GA
def TestRun(j1,j2,j3,j4,j5,j6,j7,j8,j9,j10,j11,j12,j13,j14,j15):   
	global fitness_value
	home = expanduser("~")
	logging.basicConfig(filename=home+'/catkin_ws/src/virtual_racetrack/virtual_roadtest/log/test_logs.log', 
                     level=logging.DEBUG,format='%(asctime)s:%(levelname)s:%(message)s')
                     
	logging.info('-----------Begin TestRun-------------')
 
 	# Generate world
	WorldGenerator(j1,j2,j3,j4,j5,j6,j7,j8,j9,j10,j11,j12,j13,j14,j15)
 	print('WorldGenerator ended')

	time.sleep(2)

	# Generate Path
	PathGenerator()
	ls = listdir(home+'/catkin_ws/src/race/src')
	while('path.txt' not in ls):
		ls = listdir(home+'/catkin_ws/src/race/src')
		pass

	logging.info('Step 2 - PathGenerator ended')
	time.sleep(2) # occasional segmentation fault in path planner


	''' Test Run'''
	ROS()
	logging.info('Step 3 - ROS ended')
	time.sleep(10)

	logging.info('-----------End of TestRun-------------')

	print('Test Run ended')
  	os.remove(home+'/catkin_ws/src/race/src/path.txt')
	os.remove(home+'/catkin_ws/src/virtual_racetrack/virtual_roadtest/src/map/final.png')
	return fitness_value



if __name__ == '__main__':
    TestRun()