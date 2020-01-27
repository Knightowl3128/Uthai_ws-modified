#!/usr/bin/env python3
from Robot import *
from numpy import *
import matplotlib.pyplot as plt
from traj2 import traj
import rospy
from std_msgs.msg import Float64

rospy.init_node('mono_move')
fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
# creating the robot
body = Robot()
body.name = 'Mono'
# creating the core and the corresponding links
# name, id, mass, direction, mother, child)
core_l = Link('Centre', 0, 5, 'Left', None, 1)
l_1 = Link('Hip_1', 1, 0, 'Left', 0, 2) # zero mass as there is no physical link (ball joint)
l_2 = Link('Hip_2', 2, 1, 'Left', 1, 3)
l_3 = Link('Thigh', 3, 1, 'Left', 2, 4)
l_4 = Link('Knee', 4, 1, 'Left', 3, 5)
l_5 = Link('Ankle', 5, 0, 'Left', 4, None)

core_r = Link('Centre', 0, 5, 'Right', None, 1)
r_1 = Link('Hip_1', 1, 0, 'Right', 0, 2)
r_2 = Link('Hip_2', 2, 1, 'Right', 1, 3)
r_3 = Link('Thigh', 3, 1, 'Right', 2, 4)
r_4 = Link('Knee', 4, 1, 'Right', 3, 5)
r_5 = Link('Ankle', 5, 0, 'Right', 4, None)

l_3.pub = rospy.Publisher('/mono/l_hip_pitch_position/command',Float64,queue_size = 1)
l_4.pub = rospy.Publisher('/mono/l_knee_pitch_position/command',Float64,queue_size = 1)
l_5.pub = rospy.Publisher('/mono/l_ankle_pitch_position/command',Float64,queue_size = 1)

r_3.pub = rospy.Publisher('/mono/r_hip_pitch_position/command',Float64,queue_size = 1)
r_4.pub = rospy.Publisher('/mono/r_knee_pitch_position/command',Float64,queue_size = 1)
r_5.pub = rospy.Publisher('/mono/r_ankle_pitch_position/command',Float64,queue_size = 1)


body.add_link(core_l)
body.add_link(l_1)
body.add_link(l_2)
body.add_link(l_3)
body.add_link(l_4)
body.add_link(l_5)


body.add_link(core_r)
body.add_link(r_1)
body.add_link(r_2)
body.add_link(r_3)
body.add_link(r_4)
body.add_link(r_5)


# d-h parameters
core_l.dh = array([[0.0,   0.0,  0.09, 0.0]])
l_1.dh = array([[0.0,   -0.06,   0.0,  pi/2]])
l_2.dh = array([[0.0,   0.0, 0.0,  pi/2]])
l_3.dh = array([[0.0,   0.0,  0.25, 0.0]])
l_4.dh = array([[0.0,   0.0,  .313,  0.0]])
l_5.dh = array([[0.0,   0.0,  0.045,  0.0]])


core_r.dh = array([[0.0,   0.0,  -0.09, 0.0]])
r_1.dh = array([[0.0,   -0.06,   0.0,  pi/2]])
r_2.dh = array([[0.0,   0.0, 0.0,  pi/2]])
r_3.dh = array([[0.0,   0.0,  0.25, 0.0]])
r_4.dh = array([[0.0,   0.0,  .313,  0.0]])
r_5.dh = array([[0.0,   0.0,  0.045,  0.0]])




# body.set_angle([0,0,-pi/2, 0.3522279392980471, -0.6383816108049025],'Left')
body.set_angle([0,0,-1.5666796536017116, 0.3522279392980471, -0.6383816108049025,pi/2],'Left')
body.set_angle([0,0,-1.5666796536017116, 0.3522279392980471, -0.6383816108049025,pi/2],'Right')

# body.set_angle([0, 0, -pi/2, 0.3522279392980471, -0.6383816108049025],'Right')


foot_height = 0.05
step_size = .05
speed = 0.1
t = 0
switch_timer = 0
left_l = False
switch_timer = 0
foot_origin_ds = 0.09

angles_l = body.inverse_kinematics([foot_origin_ds,0,0],'Left')
angles_r = body.inverse_kinematics([-foot_origin_ds,0,0],'Right')

initiate_time = 5


#####initiate##########
spline_1, spline_2, spline_3 = body.transition_angle([-pi / 2, 0, 0],
                        [-1.5707963267948966, 0.3562144559334822, -0.63848537302278],initiate_time)

show = False
while t<initiate_time:
    print(11111)


    angles_l = [0,0,spline_1(t), spline_2(t), spline_3(t),pi/2]
    angles_r = [0, 0, spline_1(t), spline_2(t), spline_3(t), pi / 2]
    body.set_angle(angles_l, 'Left')
    body.set_angle(angles_r, 'Right')
    body.get_all_pos()
    body.ros_publish()
    t += speed
    if show:
        ax.axes.set_xlim3d(left=-1, right=1)
        ax.axes.set_ylim3d(bottom=-1, top=1)
        ax.axes.set_zlim3d(bottom=0, top=.8)
        body.draw_all(ax)
        ax.grid()

        plt.pause(0.000000000000000001)
        ax.cla()

t = 0

while not rospy.is_shutdown():
    print(l_5.end)
    body.CoM = array([[-traj(t)[2], -traj(t)[1], 0.63991906]])

    # body.CoM = array([[a[2], -a[1], 23]])
    if t == 0:
        spline_h = CubicSpline([0,1,2], [0, foot_height,0],bc_type=(((1,0)),(1,0)))
        spline_y = CubicSpline([0, 2], [0, step_size], bc_type=(((1, 0)), (1, 0)))
    if t <= 2 and t != 0:
        angles_l = body.inverse_kinematics([foot_origin_ds,-spline_y(t),spline_h(t)],'Left')
        angles_r = body.inverse_kinematics([-foot_origin_ds, 0, 0], 'Right')

    if not t <= 2:
        if abs(round(switch_timer,5))<= 0.0001:
            if left_l:
                spline_h_l = CubicSpline([0, 1, 2], [0, foot_height, 0], bc_type=(((1, 0)), (1, 0)))
                spline_y_l = CubicSpline([0, 2], [body.links_l[5].end[0, 1], -2*step_size+ body.links_l[5].end[0, 1]],
                                       bc_type=(((1, 0)), (1, 0)))
                swing_leg = 'Left'
                switch_timer = 2.0 + speed
            if not left_l:
                spline_h_r = CubicSpline([0, 1, 2], [0, foot_height, 0], bc_type=(((1, 0)), (1, 0)))
                spline_y_r = CubicSpline([0, 2], [body.links_r[5].end[0, 1], -2*step_size + body.links_r[5].end[0, 1]],
                                       bc_type=(((1, 0)), (1, 0)))
                swing_leg = 'Right'
                switch_timer = 2.0 + speed
            left_l = not left_l


        elif switch_timer>=0.0001:
            switch_timer-=speed

            if swing_leg == 'Left':
                k = 2-switch_timer
                angles_l = body.inverse_kinematics([foot_origin_ds, spline_y_l(k), spline_h_l(k)], 'Left')

                angles_r = body.inverse_kinematics([-foot_origin_ds,r_5.end[0,1],0], 'Right')
            elif swing_leg == 'Right':
                k = 2 - switch_timer
                angles_r = body.inverse_kinematics([-foot_origin_ds, spline_y_r(k), spline_h_r(k)], 'Right')
                angles_l = body.inverse_kinematics([foot_origin_ds,l_5.end[0,1],0], 'Left')
    body.set_angle(angles_l, 'Left')
    body.set_angle(angles_r, 'Right')
    body.get_all_pos()
    body.ros_publish()
    t += speed
    rospy.spin()
    if show:
        ax.axes.set_xlim3d(left=-1, right=1)
        ax.axes.set_ylim3d(bottom=-1, top=1)
        ax.axes.set_zlim3d(bottom=0, top=.8)
        body.draw_all(ax)
        ax.grid()

        plt.pause(0.000000000000000001)
        ax.cla()

plt.figure(2)

time = arange(0,t,speed)
plt.plot(time,Y)
plt.plot(time,traj(time)[1])
plt.show()



