import rosbag
from std_msgs.msg import String

import time

bag = rosbag.Bag("../data/test.bag", 'w')

try:
    str = String()
    str.data = "hello"

    bag.write("chatter", str)
    time.sleep(2)
finally:
    bag.close()
