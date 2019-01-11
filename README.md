## message recorder
### 使い方

端末４つ立ち上げる
terminal:1

```
$ roscore
```
terminal:2

```
$ rosrun bag_manager talker.py
```
terminal:3

```
$ roscd bag_manager/scripts
$ python msg_recorder.py
```
terminal:4

```
$ rostopic pub reporter std_msgs/String "msg_reporter"
```

talker.pyからpublishされたメッセージはbag_manager/data/test.bagに格納される。  
terminal:4で任意のメッセージを投げた時はterminal:4で投げたメッセージがbag_manager/data/にメッセージ.bagで格納される。  
（上の場合、bag_manager/data/msg_reporter.bagとなる）