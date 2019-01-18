#!/usr/bin/env python
#encoding: utf8

import rospy
from std_msgs.msg import String
import rosbag

import time
import os

sub_count = 0
bag = rosbag.Bag(os.path.dirname(__file__) + "/../data/test.bag", 'w')

def callback(message, id):
    global sub_count, bag

    if str(id) == "0":
        print "recieved: /chatter"
        print message.data
        try:
            bag.write("/chatter", message)
        except:
            pass
    else:
        print "recieved: /reporter"
        bag.close()

        sub_count += 1
        FILENAME = os.path.dirname(__file__) + "/../data/test" + str(sub_count) + ".bag"
        #print "file name: ", os.path.dirname(__file__) + "/../data/test"
        bag = rosbag.Bag(FILENAME, 'w')
        
    
    

if __name__ == "__main__":
    rospy.init_node("listener")
    sub = rospy.Subscriber("/chatter", String, callback, callback_args=0)
    sub2 = rospy.Subscriber("/reporter", String, callback, callback_args=1)

    rospy.spin()

    bag.close()
    time.sleep(1)
