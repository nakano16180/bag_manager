## message recorder
## インストール

```
$ pip install python-dotenv
```
bag_manager/script/helper/.envにHOME_PATHを追加。

### 使い方

端末3つ立ち上げる
terminal:1

```
$ roslaunch bag_manager talker.launch 
```
terminal:2

```
$ rosrun bag_manager msg_recorder.py --topics /chatter /chatter2
```
terminal:3

```
$ rosrun bag_manager reporter.py 
```

.envファイルに設定したHOME_PATH以下にlog/、tmp/、bag/ディレクトリができる。
正常なtopicの記録はtmp/以下に、エラー検出された時の記録はbag/以下に保存される。