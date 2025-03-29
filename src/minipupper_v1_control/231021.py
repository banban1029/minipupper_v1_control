
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np



class PublisherNode(Node):
    # def __init__(self):
    #     super().__init__('image_publisher')
    #     self.publisher = self.create_publisher(Image, 'mini_pupper_lcd/image_raw', 10)
    #     self.bridge = CvBridge()

    # def publish_image(self, cv_image):
    #     ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
    #     self.publisher.publish(ros_image)
        
        
    def __init__(self):
        super().__init__('image_publisher')
        self.publisher = self.create_publisher(Image, 'mini_pupper_lcd/image_raw', 10)
        self.bridge = CvBridge()



def main(args=None):
    rclpy.init(args=args)

    publisher_node = PublisherNode()
    
    cv_image = cv2.imread('~/mini_pupper_bsp/Display/hop.png')

    # ここで必要な画像を取得または生成する
    # 例: cv_image = cv2.imread('example_image.jpg')

    rate = publisher_node.create_rate(1)  # 1 Hzのレートで画像をパブリッシュする

    while rclpy.ok():
        # ここでcv_imageを取得または生成する
        # 例: cv_image = cv2.imread('example_image.jpg')
        
        cv_image = cv2.imread('~/mini_pupper_bsp/Display/hop.png')


        publisher_node.publish_image(cv_image)
        rate.sleep()

    publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

