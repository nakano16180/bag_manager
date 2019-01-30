#!/usr/bin/env python
#encoding: utf8

import rospy
from std_msgs.msg import String
import rosbag

import time
import os
import yaml

size_thres = 6441  #ファイルに書き込むサイズ制限用(byte)
time_thres = None  #600 # second
file_count = 0
start_time = 0

data_dir = os.path.dirname(__file__) + "/../data/"

bag = rosbag.Bag(data_dir + "test.bag", 'w')

def callback(message, id):
    global file_count, size_thres, time_thres, start_time, bag

    if str(id[0]) == "0":
        if size_thres and (bag.size < size_thres):  # 通常時書き込みの条件. 
            try:
                print id[1]  # topic name
                bag.write(id[1], message)
                print bag.size
                print "chunk_th: ", bag.chunk_threshold
                print "chunk_offset: ", bag._get_chunk_offset()
            except:
                pass
        elif time_thres and (rospy.get_time() - start_time) < time_thres:
            try:
                bag.write(id[1], message)
                print bag.size
                print rospy.get_time() - start_time  # second
            except:
                pass
        else:
            bag.close()
            file_count += 1
            
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
    import sys
    rospy.init_node("listener")

    start_time = rospy.get_time()
    #print sys.argv[1:]  # コマンドライン引数
    print rospy.get_published_topics()  # published topic list

    topic_name = "/chatter"
    record_topic = rospy.Subscriber(topic_name, String, callback, callback_args=[0, topic_name])
    topic_name = "/chatter2"
    record_topic2 = rospy.Subscriber(topic_name, String, callback, callback_args=[0, topic_name])

    reporter = rospy.Subscriber("/reporter", String, callback, callback_args=1)

    rospy.spin()

    bag.close()
    time.sleep(1)
