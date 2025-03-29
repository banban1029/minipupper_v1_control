
import rclpy
from rclpy.node import Node
from MangDang.mini_pupper.HardwareInterface import HardwareInterface
import time
from geometry_msgs.msg import Twist


class Test(Node):
    def __init__(self):
        super().__init__('cmdmake_node')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.publish_cmd)

    def publish_cmd(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        self.publisher.publish(msg)


def main():
    rclpy.init()
    node = Test()

    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

    # rospy.init_node('tcmdvel_publisher')
    # test = Test()
    # # 直進
    # test.pub_x()
    # # 旋回
    # test.pub_z()

   # {"op": "publish", "topic": "/cmd_vel", "msg": {"linear": {"x": 0.0, "y": 0.0, "z": 0.0}, "angular": {"x": 0.0, "y": 0.0, "z": 0.0}}

    # # 直進
    # def pub_x(self):
    #     # 目的の距離と速度を設定
    #     dist = 1.0 # [m]
    #     speed = 0.2 # [m/s]
    #     target_time = dist / speed # [s]

    #     # Twist 型のデータ
    #     t = Twist()
    #     t.linear.x = speed
    #     t.angular.z = 0

    #     # 開始の時刻を保存
    #     start_time = time.time()
    #     # 経過した時刻を取得
    #     end_time = time.time()

    #     # target_time を越えるまで走行
    #     rate = rospy.Rate(30)
    #     while end_time - start_time <= target_time:
    #         self.pub.publish(t)
    #         end_time = time.time()
    #         rate.sleep()

    # # 旋回
    # def pub_z(self):
    #     # 目的の角度と速度を設定
    #     theta = 180.0 # [deg]
    #     speed = 90.0 # [deg/s]
    #     target_time = theta / speed # [s]

    #     # Twist 型のデータ
    #     t = Twist()
    #     t.linear.x = 0
    #     t.angular.z = speed * 3.1415 / 180.0 # [rad]

    #     # 開始の時刻を保存
    #     start_time = time.time()
    #     # 経過した時刻を取得
    #     end_time = time.time()

    #     # target_time を越えるまで走行
    #     rate = rospy.Rate(30)
    #     while end_time - start_time <= target_time:
    #         self.pub.publish(t)
    #         end_time = time.time()
    #         rate.sleep()
