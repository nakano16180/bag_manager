#!/usr/bin/env python
#encoding: utf8

import rospy
from std_msgs.msg import String

#def callback(message):
#    rospy.loginfo("I heard %s", message.data)

def callback(message, id):
    if str(id) == "0":
        print "recieved: /chatter"
    else:
        print "recieved: /reporter"

if __name__ == "__main__":
    rospy.init_node("listener")
    sub = rospy.Subscriber("/chatter", String, callback, callback_args=0)
    sub2 = rospy.Subscriber("/reporter", String, callback, callback_args=1)

    rospy.spin()
