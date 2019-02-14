#!/usr/bin/env python
#encoding: utf8

import rospy
from std_msgs.msg import String
import rosbag

import os, glob
import time, signal, argparse
from helper import common, logger
lg = logger.genlogger()


buffer_time_thres = 30  #second

reporter_time = None
reported_count = 0
cmd = None
pid = None

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
    global reporter_time, reported_count, cmd, pid, buffer_time_thres
    if str(id[0]) == "0":
        print "topic: ", id[1]  # topic name
        print "reported count", reported_count
        if not reporter_time == None :
            print "time from reported: ", rospy.get_time() - reporter_time
            if rospy.get_time() - reporter_time > buffer_time_thres:
                reporter_time = None
                os.killpg(pid.pid, signal.SIGINT)

                pid = logger.execmd(cmd, blocking=False) # non-blocking
                print "new pid: ", pid.pid

                reported_bag = sorted(glob.glob(common.TMP_PATH + "/*.bag"))
                print reported_bag[-1]
    else:  # イベント発生時の処理
        print "recieved: "+str(id[1])
        reporter_time = rospy.get_time()
        reported_count += 1
        print "pid: ", pid.pid
        
    
    

if __name__ == "__main__":
    import sys
    rospy.init_node("listener")

     # signal handler for soft-kill
    is_shutdown = False
    def sigterm(): 
        global is_shutdown
        is_shutdown = True
    signal.signal(signal.SIGALRM, sigterm)
    lg.info("kill by Ctrl-C")
    # rosbag record command
    args = getargs()
    if args.all:
        topics = "--all"
        lg.info("record all topics")
    else:
        topics = " ".join(args.topics)
        lg.info("record topics: {}".format(topics))
     # prepare record
    prefix = "{}/{}".format(args.dir, args.prefix)
    lg.info("save directory: {}".format(args.dir))
    lg.info("rosbag prefix: {}_*.bag".format(prefix))
    # execute command
    cmd = "rosbag record --split --size {} -o {} {}"
    cmd = cmd.format(args.size*1024, prefix, topics)
    lg.info("execute command: {}".format(cmd))
    pid = logger.execmd(cmd, blocking=False) # non-blocking
    print "pid: ", pid.pid

    topic_name = "/chatter"
    record_topic = rospy.Subscriber(topic_name, String, callback, callback_args=[0, topic_name])
    topic_name = "/chatter2"
    record_topic2 = rospy.Subscriber(topic_name, String, callback, callback_args=[0, topic_name])

    topic_name = "/reporter"
    reporter = rospy.Subscriber(topic_name, String, callback, callback_args=[1, topic_name])

    rospy.spin()
    os.killpg(pid.pid, signal.SIGINT)