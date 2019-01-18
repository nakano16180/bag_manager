## message recorder
### 使い方

端末４つ立ち上げる
terminal:1

```
$ roscore
```
terminal:2

```
$ rosrun bag_manager msg_recorder.py
```
terminal:3

```
$ rosrun bag_manager talker.py
```
terminal:4

```
$ rostopic pub reporter std_msgs/String "msg_reporter"
```

talker.pyからpublishされたメッセージはbag_manager/data/test.bagに格納される。