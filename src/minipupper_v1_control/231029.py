

import numpy as np
import math
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from MangDang.mini_pupper.HardwareInterface import HardwareInterface
import time
import glob


import numpy as np
# アプリ構成 修正中
import gradio as gr
import os

joint = [0.0, 45.0, -90.0,
         0.0, 45.0, -90.0,
         0.0, 45.0, -90.0,
         0.0, 45.0, -90.0]
joints = np.array(joint)*np.pi/180.0


# ファイル先
files = glob.glob(
    "/home/banban/minipupper_control/src/mini_mini/mini_mini/images/*.png")
files = sorted(files)


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

    def mini_change(self, lf1, lf2, lf3, rf1, rf2, rf3, lb1, lb2, lb3, rb1, rb2, rb3):

        global joint, joints

        joint = [lf1, lf2, lf3, rf1, rf2, rf3, lb1, lb2, lb3, rb1, rb2, rb3]

        joints = np.array(joint)*np.pi/180.0

        print('joint:', joints)

        self.publish_joint(joints)

    def calibrate(self):
        global joint, joints
        joint = [0.0, 45.0, -90.0,
                 0.0, 45.0, -90.0,
                 0.0, 45.0, -90.0,
                 0.0, 45.0, -90.0]
        joints = np.array(joint)*np.pi/180.0
        self.publish_joint(joints)

    def mini_gradio(self):

        with gr.Blocks() as demo:
            gr.Markdown(  # Markdownを使うと、文章を表示できる 4つの半角で改行
                """
            **mini_pupper_getup!!**    
            Start trying to various your image.
            """)

            with gr.Row():
                output = gr.Image(
                    type="pil", value=files[3], label="mini_pupper")

                btn = gr.Button(value="calibrate", label="calibrate")

            with gr.Row():
                with gr.Column():
                    leg0 = gr.Slider(minimum=-180, maximum=180, value=0.0, step=1,
                                     interactive=True, label="lf1")  # value start , step 1
                    leg1 = gr.Slider(
                        minimum=-180, maximum=180, value=45.0, step=1, interactive=True, label="lf2")
                    leg2 = gr.Slider(
                        minimum=-180, maximum=180, value=-90.0, step=1, interactive=True, label="lf3")
                    leg6 = gr.Slider(
                        minimum=-180, maximum=180, value=0.0, step=1, interactive=True, label="lb1")
                    leg7 = gr.Slider(
                        minimum=-180, maximum=180, value=45.0, step=1, interactive=True, label="lb2")
                    leg8 = gr.Slider(
                        minimum=-180, maximum=180, value=-90.0, step=1, interactive=True, label="lb3")
                with gr.Column():
                    leg3 = gr.Slider(
                        minimum=-180, maximum=180, value=0.0, step=1, interactive=True, label="rf1")
                    leg4 = gr.Slider(
                        minimum=-180, maximum=180, value=45.0, step=1, interactive=True, label="rf2")
                    leg5 = gr.Slider(
                        minimum=-180, maximum=180, value=-90.0, step=1, interactive=True, label="rf3")
                    leg9 = gr.Slider(
                        minimum=-180, maximum=180, value=0.0, step=1, interactive=True, label="rb1")
                    leg10 = gr.Slider(
                        minimum=-180, maximum=180, value=45.0, step=1, interactive=True, label="rb2")
                    leg11 = gr.Slider(
                        minimum=-180, maximum=180, value=-90.0, step=1, interactive=True, label="rb3")
            # change_button1 = gr.Button("(*'▽')いざ開始(*'▽')" ,scale = 1) # Buttonを使うと、ボタンを作成できる,ボタン共通
            # live = True
            # self.leg0.input(  # 書き方
            #     fn=self.mini_change,
            #     inputs=[self.leg0, self.leg1, self.leg2, self.leg3, self.leg4, self.leg5,
            #             self.leg6, self.leg7, self.leg8, self.leg9, self.leg10, self.leg11],
            # )
            leg0.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )
            leg1.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )
            leg2.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )
            leg3.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )
            leg4.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )
            leg5.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )
            leg6.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )
            leg7.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )
            leg8.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )
            leg9.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )
            leg10.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )
            leg11.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
            )

            btn.click(
                fn=self.publish_joint,
                inputs=[joints],)

            # change_button1.click( #書き方
            #     fn = mini_change,
            #     inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
            #     #outputs = [output],

            demo.launch(share=True)


def main():
    # ROSクライアントの初期化
    rclpy.init()

    # ノードクラスのインスタンス
    commander = Commander()

    # 最初の指令をパブリッシュする前に少し待つ
    time.sleep(1.0)

    # 初期ポーズへゆっくり移動させる
    # demo.launch(share=True)
    commander.mini_gradio()

    rclpy.spin(commander)
    rclpy.shutdown()

    print('終了')


if __name__ == '__main__':
    main()
