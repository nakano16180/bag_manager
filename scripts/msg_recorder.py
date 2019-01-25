#!/usr/bin/env python
#encoding: utf8

import rospy
from std_msgs.msg import String
import rosbag

import time
import os
import yaml

sub_count = 6441  #ファイルに書き込むサイズ制限用(byte)
file_count = 0
start_time = 0

data_dir = os.path.dirname(__file__) + "/../data/"

bag = rosbag.Bag(data_dir + "test.bag", 'w')

def callback(message, id):
    global file_count, sub_count, start_time, bag

    if str(id) == "0":
        if bag.size < sub_count:  # 通常時書き込みの条件.  (rospy.get_time() - start_time) < 600 などにすると時間でローテーションできる
            try:
                bag.write("/chatter", message)
                print bag.size
                print rospy.get_time() - start_time  # second
            except:
                pass
        else:
            bag.close()
            file_count += 1
            #info = yaml.load(rosbag.Bag(bag.filename, 'r')._get_yaml_info())
            #print info["size"]
            FILENAME = data_dir + "test" + str(file_count) + ".bag"
            bag = rosbag.Bag(FILENAME, 'w')
            print bag.filename
    else:  # イベント発生時の処理
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

    start_time = rospy.get_time()
    record_topic = rospy.Subscriber("/chatter", String, callback, callback_args=0)

    reporter = rospy.Subscriber("/reporter", String, callback, callback_args=1)

    rospy.spin()

    bag.close()
    time.sleep(1)
