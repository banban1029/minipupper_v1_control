
import PIL
from PIL import Image
import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from MangDang.mini_pupper.display import Display

import numpy as np
import glob
import os

import time


# ファイル先
files = glob.glob(
    "/home/banban/minipupper_control/src/mini_mini/mini_mini/images/*.png")
files = sorted(files)

num_file = 0


def keybord():
    global num_file

    print('num:', num_file)
    # 押されたキーによって場合分けして処理
    key = input('0,1...: ')

    num_file = int(key)

    if (num_file > len(files)-1):
        num_file = len(files)-1
        print("再入力")
        keybord()


class DisplayPublisher(Node):

    def __init__(self):
        super().__init__('display_publisher')

        self.display_publisher = self.create_publisher(
            Image, 'mini_pupper_lcd/image_raw', 10)

        timer_period = 0.5  # seconds

        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        # ｂｇｒ８必須

        keybord()

        file = files[num_file]

        self.bridge = CvBridge()
        self.cv_image = cv2.imread(file, cv2.IMREAD_COLOR)

        img_msg = self.bridge.cv2_to_imgmsg(self.cv_image, encoding="bgr8")
        self.display_publisher.publish(img_msg)
        self.get_logger().info("Publishing image")


def main(args=None):
    global num_file

    rclpy.init(args=args)

    display_node = DisplayPublisher()

    rclpy.spin(display_node)

    display_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
