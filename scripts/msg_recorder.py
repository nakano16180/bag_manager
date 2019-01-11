#!/usr/bin/env python
#encoding: utf8

import rospy
from std_msgs.msg import String
import rosbag


sub_count = 0
#bag = rosbag.Bag("../data/test.bag", 'w')

def callback(message, id):
    global sub_count

    if str(id) == "0":
        bag = rosbag.Bag("../data/test.bag", 'w')
        print "recieved: /chatter"
        print message.data
        try:
            bag.write("/chatter", message)
        finally:
            bag.close()
    else:
        print "recieved: /reporter"
        FILENAME = "../data/"+ message.data + ".bag"
        #print "file name: ", FILENAME
        bag = rosbag.Bag(FILENAME, 'w')
        try:
            bag.write("/reporter", message)
        finally:
            bag.close()
    
    

if __name__ == "__main__":
    rospy.init_node("listener")
    sub = rospy.Subscriber("/chatter", String, callback, callback_args=0)
    sub2 = rospy.Subscriber("/reporter", String, callback, callback_args=1)

    rospy.spin()
