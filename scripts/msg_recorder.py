#!/usr/bin/env python
#encoding: utf8

import rospy
from std_msgs.msg import String
import rosbag

import time
import os

sub_count = 0  #ファイルに書き込むサイズ制限用
file_count = 0
data_dir = os.path.dirname(__file__) + "/../data/"

bag = rosbag.Bag(data_dir + "test.bag", 'w')

def callback(message, id):
    global file_count, sub_count, bag

    if str(id) == "0":
        if sub_count < 20:
            print "recieved: /chatter"
            #print message.data
            try:
                bag.write("/chatter", message)
                sub_count += 1
            except:
                pass
        else:
            bag.close()
            sub_count = 0
            file_count += 1
            FILENAME = data_dir + "test" + str(file_count) + ".bag"
            bag = rosbag.Bag(FILENAME, 'w')
    else:
        print "recieved: /reporter"
        bag.close()

        before = str(bag.filename)
        renamed_file = data_dir + str(message.data) + ".bag"

        with rosbag.Bag(renamed_file, "w") as renamebag:
            for topic, msg, time in rosbag.Bag(before).read_messages():
                renamebag.write(topic, msg, time)
        os.remove(before)
        
        file_count += 1
        FILENAME = data_dir + "test" + str(file_count) + ".bag"
        bag = rosbag.Bag(FILENAME, 'w')
        
    
    

if __name__ == "__main__":
    rospy.init_node("listener")
    record_topic = rospy.Subscriber("/chatter", String, callback, callback_args=0)

    reporter = rospy.Subscriber("/reporter", String, callback, callback_args=1)

    rospy.spin()

    bag.close()
    time.sleep(1)
