#!/usr/bin/env python
#encoding: utf8

import rospy
from std_msgs.msg import String
import rosbag

import time
import os

sub_count = 0
file_count = 0
bag = rosbag.Bag(os.path.dirname(__file__) + "/../data/test.bag", 'w')

def callback(message, id):
    global file_count, sub_count, bag

    if str(id) == "0":
        if sub_count < 20:
            print "recieved: /chatter"
            print message.data
            try:
                bag.write("/chatter", message)
                sub_count += 1
            except:
                pass
        else:
            bag.close()
            sub_count = 0
            file_count += 1
            FILENAME = os.path.dirname(__file__) + "/../data/test" + str(file_count) + ".bag"
            bag = rosbag.Bag(FILENAME, 'w')
    else:
        print "recieved: /reporter"
        bag.close()

        before = str(bag.filename)
        renamed_file = os.path.dirname(__file__) + "/../data/test" + str(message.data)+".bag"

        with rosbag.Bag(renamed_file, "w") as renamebag:
            for topic, msg, time in rosbag.Bag(before).read_messages():
                renamebag.write(topic, msg, time)
        os.remove(before)
        
        file_count += 1
        FILENAME = os.path.dirname(__file__) + "/../data/test" + str(file_count) + ".bag"
        #print "file name: ", os.path.dirname(__file__) + "/../data/test"
        bag = rosbag.Bag(FILENAME, 'w')
        
    
    

if __name__ == "__main__":
    rospy.init_node("listener")
    sub = rospy.Subscriber("/chatter", String, callback, callback_args=0)
    sub2 = rospy.Subscriber("/reporter", String, callback, callback_args=1)

    rospy.spin()

    bag.close()
    time.sleep(1)
