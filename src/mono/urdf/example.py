#!/usr/bin/env python
from openravepy import *
import numpy, time
env = Environment() # create openrave environment
env.SetViewer('qtcoin') # attach viewer (optional)
env.Load('my_robot.dae') # load a scene
robot = env.GetRobots()[0] # get the first robot
print(planningutils.GetDHParameters(robot))
