#!/usr/bin/env python
#encoding: utf8

import rospy
from std_msgs.msg import String
import rosbag

import os
import time, signal, argparse
import common
logger = common.genlogger()


size_thres = 6441  #ファイルに書き込むサイズ制限用(byte)
time_thres = None  #600 # second
file_count = 0
start_time = 0

data_dir = os.path.dirname(__file__) + "/../data/"

reporter_time = []

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default=common.TMP_PATH)
    parser.add_argument("--prefix", default=common.BAG_PREFIX)
    parser.add_argument("--topics", type=str, nargs='+',
        default=["/velodyne_packets", "/image_raw", "/can_info"])
    parser.add_argument("--size", type=int, default=10)   # [GB]
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    args.dir = common.normpath(args.dir)
    common.gendir(args.dir) # create directory
    return args

def callback(message, id):

    if str(id[0]) == "0":
        print id[1]  # topic name
    else:  # イベント発生時の処理
        print "recieved: "+str(id[1])
        reporter_time.append(rospy.get_time())
        print reporter_time[0], reporter_time[-1]
        
    
    

if __name__ == "__main__":
    import sys
    rospy.init_node("listener")

     # signal handler for soft-kill
    is_shutdown = False
    def sigterm(): 
        global is_shutdown
        is_shutdown = True
    signal.signal(signal.SIGALRM, sigterm)
    logger.info("kill by Ctrl-C")
    # rosbag record command
    args = getargs()
    if args.all:
        topics = "--all"
        logger.info("record all topics")
    else:
        topics = " ".join(args.topics)
        logger.info("record topics: {}".format(topics))
     # prepare record
    prefix = "{}/{}".format(args.dir, args.prefix)
    logger.info("save directory: {}".format(args.dir))
    logger.info("rosbag prefix: {}_*.bag".format(prefix))
    # execute command
    cmd = "rosbag record --split --size {} -o {} {}"
    cmd = cmd.format(args.size*1024, prefix, topics)
    logger.info("execute command: {}".format(cmd))
    #pid = common.execmd(cmd, blocking=False) # non-blocking

    topic_name = "/chatter"
    record_topic = rospy.Subscriber(topic_name, String, callback, callback_args=[0, topic_name])
    topic_name = "/chatter2"
    record_topic2 = rospy.Subscriber(topic_name, String, callback, callback_args=[0, topic_name])

    topic_name = "/reporter"
    reporter = rospy.Subscriber(topic_name, String, callback, callback_args=[1, topic_name])

    rospy.spin()
