
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


import PIL
from PIL import Image
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from MangDang.mini_pupper.display import Display
import os
import numpy as np
import glob
import os

num = 0
count = 1.0

joint = [0.0, 45.0, -90.0,
         0.0, 45.0, -90.0,
         0.0, 45.0, -90.0,
         0.0, 45.0, -90.0]
joints = np.array(joint)*np.pi/180.0

dt = 0.2

# ファイル先
files = glob.glob(
    "/home/banban/minipupper_control/src/mini_mini/mini_mini/images/*.png")
files = sorted(files)

face_file = 0


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

        self.display_publisher = self.create_publisher(
            Image, 'mini_pupper_lcd/image_raw', 10)

        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.publish_joint)
        self.i = 0
        self.timer = self.create_timer(timer_period, self.publish_display)

        # self.hardware_interface = HardwareInterface()

    def publish_joint(self, q):
        msg = JointTrajectory()
        # msg.header.stamp = self.get_clock().now().to_msg()
        msg.joint_names = self.joint_names
        msg.points = [JointTrajectoryPoint()]

        msg.points[0].positions = [
            float(q[0]), float(q[1]), float(q[2]), float(q[3]),
            float(q[4]), float(q[5]), float(q[6]), float(q[7]),
            float(q[8]), float(q[9]), float(q[10]), float(q[11])]

        self.publisher_joint.publish(msg)

    def publish_display(self, file_num):
        # ｂｇｒ８必須

        file = files[file_num]

        self.bridge = CvBridge()
        self.cv_image = cv2.imread(file, cv2.IMREAD_COLOR)

        img_msg = self.bridge.cv2_to_imgmsg(self.cv_image, encoding="bgr8")
        self.display_publisher.publish(img_msg)
        self.get_logger().info("Publishing image")

    def calibrate(self):
        global joint, joints, dt, num, count

        joint = [0.0, 45.0, -90.0,
                 0.0, 45.0, -90.0,
                 0.0, 45.0, -90.0,
                 0.0, 45.0, -90.0]

        print('joint:', joint)

        joints = np.array(joint)*np.pi/180.0

        self.publish_joint(joints)

        time.sleep(2.0)

    def up_down(self):

        global joint, joints, dt, num, count

        st = 0.2
        num1 = 5
        num2 = 400
        dtg = 0.001
        for i in range(int(num2/2)):
            joint[2] += st
            joint[5] += st
            joint[8] += st
            joint[11] += st
            joints = np.array(joint)*np.pi/180.0

            self.publish_joint(joints)
            time.sleep(dtg)

        for i in range(int(num1)):

            for i in range(num2):

                joint[2] -= st
                joint[5] -= st
                joint[8] -= st
                joint[11] -= st
                joints = np.array(joint)*np.pi/180.0
                self.publish_joint(joints)
                time.sleep(dtg)

            for i in range(int(num2)):
                joint[2] += st
                joint[5] += st
                joint[8] += st
                joint[11] += st
                joints = np.array(joint)*np.pi/180.0
                self.publish_joint(joints)
                time.sleep(dtg)

        for i in range(int(num2/2)):
            joint[2] -= st
            joint[5] -= st
            joint[8] -= st
            joint[11] -= st

            joints = np.array(joint)*np.pi/180.0
            self.publish_joint(joints)

            time.sleep(dtg)

    def create(self):
        global joint, joints, dt, num, count

        lf1 = float(input('lf1:'))
        lf2 = float(input('lf2:'))
        lf3 = float(input('lf3:'))
        rf1 = float(input('rf1:'))
        rf2 = float(input('rf2:'))
        rf3 = float(input('rf3:'))
        lb1 = float(input('lb1:'))
        lb2 = float(input('lb2:'))
        lb3 = float(input('lb3:'))
        rb1 = float(input('rb1:'))
        rb2 = float(input('rb2:'))
        rb3 = float(input('rb3:'))

        # 初期ポーズへゆっくり移動させる
        joint = [lf1, lf2, lf3,
                 rf1, rf2, rf3,
                 lb1, lb2, lb3,
                 rb1, rb2, rb3]

    def sleep(self):
        global joint, joints, dt
        joint = [0.0, 45.0, -120.0,
                 0.0, 45.0, -120.0,
                 0.0, 45.0, -120.0,
                 0.0, 45.0, -120.0]

    def sit(self):
        global joint, joints, dt
        joint = [0.0, 10.0, 0.0,
                 0.0, 10.0, 0.0,
                 0.0, 80.0, -110.0,
                 0.0, 80.0, -110.0]

    def left_right(self):
        global joint, joints, dt
        # ノードクラスのインスタンス

        st = 0.2
        num1 = 1
        num2 = 200

        for i in range(int(num2/2)):
            joint[0] += st
            joint[3] += st
            joint[6] += st
            joint[9] += st

            joints = np.array(joint)*np.pi/180.0
            self.publish_joint(joints)

            time.sleep(0.01)

        for i in range(int(num1)):

            for i in range(num2):

                if (i == 0):
                    num = 200

                joint[0] -= st
                joint[3] -= st
                joint[6] -= st
                joint[9] -= st

                joints = np.array(joint)*np.pi/180.0
                self.publish_joint(joints)
                time.sleep(0.01)
            for i in range(int(num2)):
                joint[0] += st
                joint[3] += st
                joint[6] += st
                joint[9] += st

                joints = np.array(joint)*np.pi/180.0
                self.publish_joint(joints)
                time.sleep(0.01)
        for i in range(int(num2/2)):
            joint[0] -= st
            joint[3] -= st
            joint[6] -= st
            joint[9] -= st

            joints = np.array(joint)*np.pi/180.0
            self.publish_joint(joints)
            time.sleep(0.01)

    def face_key(self):

        global face_file, files

        print('num:', face_file)
        # 押されたキーによって場合分けして処理
        key = input('0,1...: ')

        face_file = int(key)

        if (face_file > len(files)-1):
            face_file = len(files)-1
            print("再入力")
            self.face_key()

        self.publish_display(face_file)

    def sitting(self):
        global joint, joints, dt, num, count, face_file, files
        joint = [-6, -95, 76, 6, -95, 76, 0, 63, -67, 0, 63, -67]
        # joints = np.array(joint)*np.pi/180.0
        # self.publish_joint(joints)
        # time.sleep(0.01)

    def sitting2(self):  # toilet
        global joint, joints, dt, num, count, face_file, files

        self.calibrate()
        joint = [0, 45, -90, 0, 45, -8, 0, 45, -90, 0, 45, -90]

        joints = np.array(joint)*np.pi/180.0
        self.publish_joint(joints)
        time.sleep(2.0)

        joint = [0, 45, -90, 0, -9, -8, 0, 45, -90, 0, 45, -90]

        joints = np.array(joint)*np.pi/180.0
        self.publish_joint(joints)
        time.sleep(2.0)

        joint = [0, 45, -90, 0, -9, -8, 0, 45, -90, 0, 45, -134]

        joints = np.array(joint)*np.pi/180.0
        self.publish_joint(joints)
        time.sleep(2.0)

        joint = [0, 45, -90, 0, -9, -8, 0, 45, -90, 18, 45, -134]

        joints = np.array(joint)*np.pi/180.0
        self.publish_joint(joints)
        time.sleep(2.0)

    def command(self):
        global joint, joints, dt, num, count, face_file

        try:
            while True:
                # 変更前の値を保持
                joint_prev = joint.copy()

                # 目標関節値とともに送る目標時間
                dt = 0

                # 押されたキーによって場合分けして処理

                print('num:', num)
                print('count:', count)
                print('num_file:', face_file)

                # 押されたキーによって場合分けして処理
                key = input('0,1,2,3,4,5,6,7,8,9,10,11: ')

                if key == '0':
                    self.sitting()
                elif key == '1':
                    self.sitting2()
                elif key == '2':
                    num = 2
                elif key == '3':
                    num = 3
                elif key == '4':
                    num = 4
                elif key == '5':
                    num = 5
                elif key == '6':
                    num = 6
                elif key == '7':
                    num = 7
                elif key == '8':
                    num = 8
                elif key == '9':
                    num = 9
                elif key == '10':
                    num = 10
                elif key == '11':
                    num = 11

                elif key == '*':
                    count += 0.10
                    print('count:', count)
                elif key == '/':
                    count -= 0.10
                    print('count:', count)

                elif key == '+':
                    joint[num] += count

                elif key == '-':
                    joint[num] -= count

                elif key == 'a':  # スペースキー
                    self.calibrate()
                elif key == 'b':
                    self.sleep()
                elif key == 'c':
                    self.sit()
                elif key == 'd':
                    count = int(input('count:'))

                    print('count:', count)

                elif key == 'e':
                    self.left_right()

                elif key == 'f':
                    joint[0] += count
                    joint[3] += count
                    joint[6] -= count
                    joint[9] -= count

                # 上下運動
                elif key == 'g':
                    self.up_down()

                elif key == 'h':
                    joint = [-30.0, 120.0, -110.0,
                             -10.0, 20.0, -30.0,
                             0.0, 80.0, -50.0,
                             0.0, 70.0, -50.0]

                elif key == ' ':
                    self.create()

                # 顔の表示
                elif key == 'D':
                    self.face_key()

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

                    self.publish_joint(joints)
                    publish = True

                # パブリッシュした場合は，設定時間と同じだけ停止
                if publish:
                    time.sleep(dt)

                time.sleep(0.01)
        except KeyboardInterrupt:
            pass


def main():

    rclpy.init()

    # ノードクラスのインスタンス
    commander = Commander()

    # 最初の指令をパブリッシュする前に少し待つ
    time.sleep(1.0)

    commander.calibrate()

    # キーボード入力のための設定
    print('1, 2, 3, 4, 5, 6, 7, 8, 9, 0キーを押して関節を動かす')
    print('スペースキーを押して起立状態にする')
    print('Escキーを押して終了')

    commander.command()

    commander.calibrate()

    rclpy.spin(commander)
    rclpy.shutdown()
    print('終了')


if __name__ == '__main__':
    main()


# cd mini_control
# ros2 run mini_control test1008
