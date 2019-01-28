#!/usr/bin/env python
#encoding: utf8

import rospy
from std_msgs.msg import String

rospy.init_node("tester")

pub = rospy.Publisher("reporter", String, queue_size=10)
rate = rospy.Rate(0.5)

count = 0

while not rospy.is_shutdown():
    hello_str = String()
    hello_str.data = "report" + str(count)
    
    pub.publish(hello_str)
    print "published: ", hello_str.data

    count += 1
    rate.sleep()
