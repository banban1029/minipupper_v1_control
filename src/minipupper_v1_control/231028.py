
import PIL
from PIL import Image
import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from MangDang.mini_pupper.display import Display
import os
import numpy as np
import glob
import os

import time


#ファイル先
files = glob.glob("/home/banban/minipupper_control/src/mini_mini/mini_mini/images/*.png")
files = sorted(files)


class DisplayPublisher(Node):

    def __init__(self):
        super().__init__('display_publisher')
        
        
        self.display_publisher= self.create_publisher(
            Image, 'mini_pupper_lcd/image_raw',10)
        
        timer_period = 0.5  # seconds
        self.bridge = CvBridge()
        self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.image_path = "/home/banban/Pictures/minipupper/mini_calibrate.png"
        # self.cv_image = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        
        
        self.cv_image = cv2.imread(files[1], cv2.IMREAD_COLOR)
        
    def timer_callback(self):
        # ｂｇｒ８必須
        img_msg = self.bridge.cv2_to_imgmsg(self.cv_image, encoding="bgr8")
        self.display_publisher.publish(img_msg)
        self.get_logger().info("Publishing image")
            
     


def main(args=None):
    rclpy.init(args=args)

    display_node = DisplayPublisher()
    
    # image = os.path.join(os.path.dirname(__file__), "/home/banban/Pictures/minipupper/mini_calibrate.png")
    
    
    # image = PIL.Image.open('/home/banban/Pictures/minipupper/mini_calibrate.png')
    
    
        
    # filename = '/home/banban/Pictures/minipupper/mini_calibrate.png'
    
    # files = glob.glob("images/*.png")
    
    # image = cv2.imread(files[0])  # 画像ファイルのパスを指定
        
    # image = cv2.imread()
    
    # files = glob.glob("/home/banban/Pictures/**/*.png")

    # files = sorted(files)
    
    # msg = cv2.imread(files[0])
    
    
    
    
    # display_node.publisher_display(msg)
    
    
    
    
    rclpy.spin(display_node)

    display_node.destroy_node()
    rclpy.shutdown()
    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    main()