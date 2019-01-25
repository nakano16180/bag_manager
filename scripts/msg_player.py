import rosbag

import time
import yaml, json

def bag_read(msg, indent):
    try:
        for s in type(msg).__slots__:
            print indent*"    ", s
            bag_read(msg.__getattribute__(s), int(indent+1))
    except:
        print indent*"    ", msg

def get_info(bag_file):
    return yaml.load(rosbag.Bag(bag_file, 'r')._get_yaml_info())


info = get_info("../data/test.bag")
print json.dumps(info, indent=4)

bag = rosbag.Bag("../data/test.bag")

for topic, msg, t in bag.read_messages():
    #print msg
    bag_read(msg, 0)
    time.sleep(1)
    
bag.close()