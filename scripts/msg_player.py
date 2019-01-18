import rosbag

import time

def bag_read(msg, indent):
    try:
        for s in type(msg).__slots__:
            print indent*"    ", s
            bag_read(msg.__getattribute__(s), int(indent+1))
    except:
        print indent*"    ", msg

bag = rosbag.Bag("../data/test.bag")

for topic, msg, t in bag.read_messages():
    #print msg
    bag_read(msg, 0)
    time.sleep(1)
    
bag.close()