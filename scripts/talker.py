#!/usr/bin/env python
#encoding: utf8

import rospy
from std_msgs.msg import String

rospy.init_node("talker")

pub = rospy.Publisher("chatter", String, queue_size=10)
rate = rospy.Rate(1)

while not rospy.is_shutdown():
    hello_str = String()
    hello_str.data = "hello world %s" % rospy.get_time()
    
    pub.publish(hello_str)
    print "published: ", hello_str.data
    rate.sleep()
