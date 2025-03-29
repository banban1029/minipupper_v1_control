


import numpy as np
import math
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from MangDang.mini_pupper.HardwareInterface import HardwareInterface
import time

import numpy as np
#アプリ構成 修正中
import gradio as gr
import os
joint = [0.0, 0.0, 0.0, 0.0,
            45.0, 45.0, 45.0, 45.0,
            -45.0, -45.0, -45.0, -45.0]

joints = np.array(joint)*np.pi/180.0
dt = 5
    


def mini_change(lf1,lf2,lf3,rf1,rf2,rf3,lb1,lb2,lb3,rb1,rb2,rb3):
    
    joint = [lf1,lf2,lf3,rf1,rf2,rf3,lb1,lb2,lb3,rb1,rb2,rb3]
    
    joints = np.array(joint)*np.pi/180.0
    
    print('joint:' ,joints)
    
    
    
    return joints



mini = os.path.join(os.path.dirname(__file__), "/home/banban/Pictures/minipupper/mini_calibrate.png")


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
        

   
#インターフェイス作成
demo = gr.Blocks()

with gr.Blocks() as demo:
    gr.Markdown( # Markdownを使うと、文章を表示できる 4つの半角で改行
    """
    **mini_pupper_getup!!**    
    Start trying to various your image.
    """)
    
    output = gr.Image(type="pil", value=mini)
    
    with gr.Row():
        
        with gr.Column():
            leg0 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lf1") #value start , step 1
            leg1 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lf2")
            leg2 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lf3")
            leg6 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lb1")
            leg7 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lb2")
            leg8 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lb3")
            
        with gr.Column():
            leg3 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rf1")
            leg4 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rf2")
            leg5 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rf3")
            leg9 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rb1")
            leg10 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rb2")
            leg11 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rb3")
            
            
    
    # change_button1 = gr.Button("(*'▽')いざ開始(*'▽')" ,scale = 1) # Buttonを使うと、ボタンを作成できる,ボタン共通
    #live = True
    
    leg0.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )
    leg1.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )
    leg2.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )  
    leg3.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )
    leg4.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )
    leg5.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )
    leg6.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )
    leg7.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )
    leg8.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )
    leg9.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )
    leg10.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )
    leg11.input( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    )
    
    
    
        
    
    
    
     
    # change_button1.click( #書き方
    #     fn = mini_change,
    #     inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
    #     #outputs = [output],
        
        
        
    
    
        

def main():
    # ROSクライアントの初期化
    rclpy.init()

    # ノードクラスのインスタンス
    commander = Commander()

    
    # 最初の指令をパブリッシュする前に少し待つ
    time.sleep(1.0)

    # 初期ポーズへゆっくり移動させる
    
    

    demo.launch(share = True)
    
    
    commander.publish_joint(joints, dt)
    print('joint:' ,joints)
    
    
    #rclpy.spin(commander)
    rclpy.shutdown()
    
    print('終了')

if __name__ == '__main__':
    main()
    
    

    
