
# https://kuruton.hatenablog.com/entry/2020/07/16/105306#%E3%83%AA%E3%82%B9%E3%83%88%E3%81%A8%E3%81%97%E3%81%A6%E5%8F%97%E3%81%91%E5%8F%96%E3%82%8B-1
# https://magazine.techacademy.jp/magazine/49549
import rclpy
from rclpy.node import Node
import numpy as np
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

        # timer_period = 0.5  # seconds
        # self.timer = self.create_timer(timer_period, self.publish_joint)
        # self.i = 0

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


def main():
    rclpy.init()
    s = Commander()

    # joint = list(map(float, input("input\n").split(", ")))   enter

    joint = [0.0, 10.0, 0.0,
             0.0, 10.0, 0.0,
             0.0, 80.0, -110.0,
             0.0, 80.0, -110.0]
    joints = np.array(joint)*np.pi/180.0
    s.publish_joint(joints)

    time.sleep(1.0)

    joint = [0.0, 10.0, 0.0,
             -40.0, 10.0, 0.0,
             0.0, 80.0, -110.0,
             0.0, 80.0, -110.0]
    joints = np.array(joint)*np.pi/180.0

    s.publish_joint(joints)

    time.sleep(1.0)

    joint = [0.0, 100.0, -120.0,
             -20.0, 10.0, 0.0,
             0.0, 80.0, -110.0,
             0.0, 80.0, -110.0]
    joints = np.array(joint)*np.pi/180.0
    s.publish_joint(joints)

    joints = np.array(joint)*np.pi/180.0
    s.publish_joint(joints)

    # rclpy.spin(commander) error
    rclpy.shutdown()
    print('終了')


if __name__ == '__main__':
    main()
