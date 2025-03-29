# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.






import numpy as np
import math
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from MangDang.mini_pupper.HardwareInterface import HardwareInterface
import time



class Commander(Node):

    def __init__(self):
        super().__init__('commander')
        self.joint_names = [
            'lf1_position', 'lf2_position', 'lf3_position', 
            'rf1_position', 'rf2_position', 'rf3_position',
            'lb1_position', 'lb2_position', 'lb3_position',
            'rb1_position', 'rb2_position', 'rb3_position']
        
        self.publisher_joint = self.create_publisher(
            JointTrajectory, '/joint_group_effort_controller/joint_trajectory', 10)
        
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.publish_joint)
        self.i = 0
    
        #self.hardware_interface = HardwareInterface()
        
        

    def publish_joint(self,q,time):
        msg = JointTrajectory()
        #msg.header.stamp = self.get_clock().now().to_msg()
        msg.joint_names = self.joint_names
        msg.points = [JointTrajectoryPoint()]
        
        msg.points[0].positions = [
            float(q[0]), float(q[1]), float(q[2]), float(q[3]), 
            float(q[4]), float(q[5]), float(q[6]), float(q[7]),
            float(q[8]), float(q[9]), float(q[10]), float(q[11])]
        
    
        self.publisher_joint.publish(msg)
        
        
        

def main():
    # ROSクライアントの初期化
    rclpy.init()

    # ノードクラスのインスタンス
    commander = Commander()

    
    # 最初の指令をパブリッシュする前に少し待つ
    time.sleep(1.0)

    # 初期ポーズへゆっくり移動させる
    joint = [0.0, 0.0, 0.0, 0.0, 
             45.0, 45.0, 45.0, 45.0,
             -45.0, -45.0, -45.0, -45.0 ]
    
    print('joint:' ,joint)
    
    joints = np.array(joint)*np.pi/180.0
    
    dt = 5
    
    
    commander.publish_joint(joints, dt)
    
    
    
    
    # キーボード入力のための設定
    print('1, 2, 3, 4, 5, 6, 7, 8, 9, 0キーを押して関節を動かす')
    print('スペースキーを押して起立状態にする')
    print('Escキーを押して終了')
    
    # key  = input() # 標準入力からキーを読み込む
    # print(key)     # 読み込んだキーの値を標準出力へ出力

    # Ctrl+cでエラーにならないようにKeyboardInterruptを捕まえる
    try:
        while True:
            # 変更前の値を保持
            joint_prev = joint.copy()
            

            # 目標関節値とともに送る目標時間
            dt = 0.2

            # 押されたキーによって場合分けして処理
            key = input('1,2,3,4,5,6,7,8,9,0: ')
            if key == 'q':
                joint[0] += 1
            elif key == 'a':
                joint[0] -= 1
            elif key == 'z':
                joint[1] += 1
            elif key == 'w':
                joint[1] -= 1
            elif key == 's':
                joint[2] += 1
            elif key == 'x':
                joint[2] -= 1
            elif key == 'e':
                joint[3] += 1
            elif key == 'd':
                joint[3] -= 1
            elif key == 'c':
                joint[4] += 1
            elif key == 'r':
                joint[4] -= 1
            elif key == 'f':
                joint[5] += 1
            elif key == 'v':
                joint[5] -= 1
            elif key == 't':
                joint[6] += 1
            elif key == 'g':
                joint[6] -= 1
            elif key == 'b':
                joint[7] += 1
            elif key == 'y':
                joint[7] -= 1
            elif key == 'h':
                joint[8] += 1
            elif key == 'n':
                joint[8] -= 1
            elif key == 'u':
                joint[9] += 1
            elif key == 'j':
                joint[9] -= 1
            elif key == 'm':
                joint[10] += 1
            elif key == 'i':
                joint[10] -= 1
            elif key == 'k':
                joint[11] += 1
            elif key == ',':
                joint[11] -= 1
                
            elif key == ' ':  # スペースキー
                joint = [0.0, 0.0, 0.0, 0.0, 
                         45.0, 45.0, 45.0, 45.0,
                        -45.0, -45.0, -45.0, -45.0 ]
                dt = 1.0
            elif key == '-1':
                break
        
            # 変化があればパブリッシュ
            publish = False
            if joint != joint_prev:
                print((f'joint: [{joint[0]:.2f}, {joint[1]:.2f}, '
                       f'{joint[2]:.2f}, {joint[3]:.2f}, '
                       f'{joint[4]:.2f}, {joint[5]:.2f}, '
                       f'{joint[6]:.2f}, {joint[7]:.2f}, '
                       f'{joint[8]:.2f}, {joint[9]:.2f}, '
                       f'{joint[10]:.2f}, {joint[11]:.2f}]'))
                
                
                joints = np.array(joint)*np.pi/180.0
                
                print('joint:' ,joint)
                
                commander.publish_joint(joints, dt)
                publish = True
            
            
            # パブリッシュした場合は，設定時間と同じだけ停止
            if publish:
                time.sleep(dt)
                
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass

    # 終了ポーズへゆっくり移動させる
    joint = [0.0, 0.0, 0.0, 0.0, 
             45.0, 45.0, 45.0, 45.0,
             -45.0, -45.0, -45.0, -45.0 ]
    
    print('joint:' ,joint)
    
    joints = np.array(joint)*np.pi/180.0
    
    dt = 5
    commander.publish_joint(joints, dt)
    
    
    
    
    
    rclpy.spin(commander)
    rclpy.shutdown()
    print('終了')

if __name__ == '__main__':
    main()
    
    
    

# cd mini_control
# ros2 run mini_control test1008

