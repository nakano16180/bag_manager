# encoding: utf8
import rosbag
from std_msgs.msg import String

import time
import yaml

# 以下の処理でtest.bagに書き込まれるのは最後のhello3
def bag_write1():
    bag = rosbag.Bag("../data/test.bag", 'w')
    print bag.filename
    try:
        str = String()
        str.data = "hello"
        print "write: ", str.data

        bag.write("chatter", str)
        time.sleep(2)
    finally:
        bag.close()

    bag = rosbag.Bag("../data/test.bag", 'w')
    try:
        str = String()
        str.data = "hello2"
        print "write: ", str.data

        bag.write("chatter", str)
        time.sleep(2)
    finally:
        bag.close()

    bag = rosbag.Bag("../data/test.bag", 'w')
    try:
        str = String()
        str.data = "hello3"
        print "write: ", str.data

        bag.write("chatter", str)
        time.sleep(2)
    finally:
        bag.close()

####################################################
# 以下の処理ならhello1からhello3まで書き込まれる
def bag_write2():
    bag = rosbag.Bag("../data/test1.bag", 'w')
    print bag.filename
    try:
        str = String()
        str.data = "hello1"
        print "write: ", str.data

        bag.write("chatter", str)
        time.sleep(2)

        str.data = "hello2"
        print "write: ", str.data

        bag.write("chatter", str)
        time.sleep(2)

        str.data = "hello3"
        print "write: ", str.data

        bag.write("chatter", str)
        time.sleep(2)
    finally:
        bag.close()

def create_empty_file():
    bag = rosbag.Bag("../data/test0.bag", 'w')
    print bag.filename
    print bag.size
    bag.close()
    info = yaml.load(rosbag.Bag(bag.filename, 'r')._get_yaml_info())
    print info["size"]

    print "----------------------------------"
    bag = rosbag.Bag("../data/test0.bag", 'w')
    print bag.filename
    print bag.size
    str = String()
    str.data = "hello1"
    bag.write("chatter", str)
    time.sleep(1)
    print bag.size
    bag.close()
    info = yaml.load(rosbag.Bag(bag.filename, 'r')._get_yaml_info())
    print info["size"]

#bag_write1()
#bag_write2()
create_empty_file()