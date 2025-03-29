
# # GPU
# import torch
# torch.cuda.is_available()
# print(torch.cuda.is_available())

import sys
sys.path.append('/home/banban/mini_pupper_bsp/Python_Module/MangDang/')


import gradio as gr
import numpy as np
import math
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from MangDang.mini_pupper.HardwareInterface import HardwareInterface
from geometry_msgs.msg import Twist
import time
import glob


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


from openai import OpenAI
import openai
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

# from gtts import gTTS


# アプリ構成 修正中

joint = [0.0, 45.0, -90.0,
         0.0, 45.0, -90.0,
         0.0, 45.0, -90.0,
         0.0, 45.0, -90.0]
joints = np.array(joint)*np.pi/180.0

walk_command = -1
walk = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])  # angular np.array


# ファイル先
files = glob.glob(
    "/home/banban/mini_ws/minipupper_v1_control/images/*.png")
files = sorted(files)
print(len(files))


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

        self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # timer_period = 0.5  # seconds
        # self.timer = self.create_timer(timer_period, self.publish_joint)
        # self.timer = self.create_timer(timer_period, self.publish_display)
        # self.timer = self.create_timer(timer_period, self.publish_cmd)

        # self.hardware_interface = HardwareInterface()

    def publish_cmd(self, data):
        msg = Twist()
        msg.linear.x = float(data[0])
        msg.linear.y = float(data[1])
        msg.linear.z = float(data[2])
        msg.angular.x = float(data[3])
        msg.angular.y = float(data[4])
        msg.angular.z = float(data[5])

        self.cmd_publisher.publish(msg)

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

    def publish_display(self, data):
        # ｂｇｒ８必須

        self.bridge = CvBridge()
        self.cv_image = cv2.imread(data, cv2.IMREAD_COLOR)

        img_msg = self.bridge.cv2_to_imgmsg(self.cv_image, encoding="bgr8")
        self.display_publisher.publish(img_msg)
        self.get_logger().info("Publishing image")

        output = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)  # gradioはRGB
        # return img_msg
        return output

    def mini_change(self, lf1, lf2, lf3, rf1, rf2, rf3, lb1, lb2, lb3, rb1, rb2, rb3):

        global joint, joints

        joint = [lf1, lf2, lf3, rf1, rf2, rf3, lb1, lb2, lb3, rb1, rb2, rb3]

        joints = np.array(joint)*np.pi/180.0

        print('joint:', joint)

        self.publish_joint(joints)

        return joint

    def count_walk(self, linear_x, linear_y, linear_z, angular_x, angular_y, angular_z):
        global walk

        walk = [linear_x, linear_y, linear_z, angular_x, angular_y, angular_z]

        print('walk:', walk)

        self.publish_cmd(walk)

        return walk

    def calibrate(self):
        global joint, joints
        joint = [0.0, 45.0, -90.0,
                 0.0, 45.0, -90.0,
                 0.0, 45.0, -90.0,
                 0.0, 45.0, -90.0]
        joints = np.array(joint)*np.pi/180.0
        self.publish_joint(joints)

        return joint

    def get_up(self):

        self.publish_display(files[11])
        time.sleep(3.0)

        self.calibrate()

    def ini_control(self):
        global walk
        walk = [0.0, 0.0, 0.0,
                0.0, 0.0, 0.0]
        self.publish_cmd(walk)

        return walk

    def sit_down(self):
        global joint, joints

        self.calibrate()

        time.sleep(1.0)

        joint = [0.0, 10.0, 0.0,
                 0.0, 10.0, 0.0,
                 0.0, 45.0, 90.0,
                 0.0, 45.0, 90.0]
        joints = np.array(joint)*np.pi/180.0
        self.publish_joint(joints)

        time.sleep(1.0)

        joint = [0.0, 10.0, 0.0,
                 0.0, 10.0, 0.0,
                 0.0, 80.0, -110.0,
                 0.0, 80.0, -110.0]
        joints = np.array(joint)*np.pi/180.0
        self.publish_joint(joints)

        return joint[0], joint[1], joint[2], joint[3], joint[4], joint[5], joint[6], joint[7], joint[8], joint[9], joint[10], joint[11], joint

    def face_down(self):
        global joint, joints
        joint = [0.0, 45.0, -120.0,
                 0.0, 45.0, -120.0,
                 0.0, 45.0, -120.0,
                 0.0, 45.0, -120.0]
        joints = np.array(joint)*np.pi/180.0
        self.publish_joint(joints)

        return joint[0], joint[1], joint[2], joint[3], joint[4], joint[5], joint[6], joint[7], joint[8], joint[9], joint[10], joint[11], joint

    def the_hand(self):
        global joint, joints

        self.sit_down()
        time.sleep(1.0)

        joint = [40.0, 10.0, 0.0,
                 0.0, 10.0, 0.0,
                 0.0, 80.0, -110.0,
                 0.0, 80.0, -110.0]
        joints = np.array(joint)*np.pi/180.0
        self.publish_joint(joints)

        time.sleep(0.2)

        joint = [20.0, 10.0, 0.0,
                 0.0, 100.0, -120.0,
                 0.0, 80.0, -110.0,
                 0.0, 80.0, -110.0]
        joints = np.array(joint)*np.pi/180.0
        self.publish_joint(joints)

        return joint[0], joint[1], joint[2], joint[3], joint[4], joint[5], joint[6], joint[7], joint[8], joint[9], joint[10], joint[11], joint

    # gptによる会話の関数

    def chat(self, input_text):

        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {'role': 'system', 'content': 'あなたは犬型ロボットで従順なペットです。今から飼い主があなたに命令をします。'},
                {'role': 'system', 'content': '''次のtemplateに従って命令を実行してください。
    
                    template = “[action]\n[face]\n”
    
                    [action]="座る" or "伏せる" or "お手" のうちどれかを選んでください。
                    [face]= 自分にどのような表情をしてほしいか。”喜び" or "悲しみ" or "怒り" or "癒やし"のうちどれかを選んでください。
    
                    '''},

                # ここで設定（会話相手の人格など）を変更できます。
                {"role": "user", "content": input_text}
                # ここにユーザーの発言が入ります。
            ],
            temperature=0.0,
            # 創造性を調整します。1.0が上限です。
        )
        print(response.choices[0].message.content)

        return response.choices[0].message.content

    # 音声からテキストへの変換関数
    def speech_to_text(self, input_audio):
        audio_file = open(input_audio, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return transcript

    # return response.choices[0].message.content
    def record_keywodrs(self, text, keyreords):

        if "座る" in text:
            keyreords.append("座る")
        elif "伏せる" in text:
            keyreords.append("伏せる")
        elif "お手" in text:
            keyreords.append("お手")

        if "喜び" in text:
            keyreords.append("喜び")

        elif "悲しみ" in text:
            keyreords.append("悲しみ")
        elif "怒り" in text:
            keyreords.append("怒り")
        elif "癒やし" in text:
            keyreords.append("癒やし")

        return keyreords

    # voice_option
    def voice_chat(self, input_audio):

        key_recorder = []
        key_recorder.clear()

        # 音声をテキストに
        text = self.speech_to_text(input_audio)

        # gptによる返答
        response_text = self.chat(text)

        # print(response_text)

        self.record_keywodrs(response_text, key_recorder)

        input_action = key_recorder[0]
        input_face = key_recorder[1]

        # print(input_action)
        # print(input_face)

        key_recorder.clear()
        # 返答を音声に
        # return response_audio

        if input_action == "座る":
            self.sit_down()
        elif input_action == "伏せる":
            self.face_down()
        elif input_action == "お手":
            self.the_hand()

        if input_face == "喜び":

            self.publish_display(files[9])

        elif input_face == "悲しみ":
            self.publish_display(files[7])
        elif input_face == "怒り":
            self.publish_display(files[5])
        elif input_face == "癒やし":
            self.publish_display(files[4])

        return input_action, input_face

    def mini_gradio(self):

        global joint, joints, walk

        with gr.Blocks() as demo:
            gr.Markdown(  # Markdownを使うと、文章を表示できる 4つの半角で改行
                """
            **mini_pupper_getup!!**    
            Start trying to various your image.
            """)

            with gr.Tab("calibrate"):

                with gr.Row():

                    gr.Image(
                        type="pil", value=files[10], label="mini_pupper")
                    output = gr.Image(
                        type="pil", value=files[11], label="mini_pupper")
                    gr.Image(
                        type="pil", value=files[5], label="mini_pupper")

                    face_image = gr.Image(type="filepath", label="face")

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

                btn1 = gr.ClearButton(value="calibrate", label="calibrate")

                # msg = gr.Textbox(lines=1, placeholder="now joint")label="calibrate"

                msg = gr.Textbox(lines=1, label="now joint")
                # btn2 = gr.Button(value="face_display",
                #                  label="face_display")  # ,scale=

            with gr.Tab("control"):

                with gr.Row():

                    with gr.Column():

                        sp_linearx = gr.Slider(minimum=-5.0, maximum=5.0, value=0.0, step=0.1,
                                               interactive=True, label="linear_x")  # value start , step 1
                        sp_lineary = gr.Slider(
                            minimum=-5.0, maximum=5.0, value=0.0, step=0.1, interactive=True, label="linear_y")  # value start , step 1)
                        sp_linearz = gr.Slider(
                            minimum=-5.0, maximum=5.0, value=0.0, step=0.1, interactive=True, label="linear_z")

                    with gr.Column():
                        sp_angularx = gr.Slider(
                            minimum=-5.0, maximum=5.0, value=0.0, step=0.1, interactive=True, label="angular_x")
                        sp_angulary = gr.Slider(
                            minimum=-5.0, maximum=5.0, value=0.0, step=0.1, interactive=True, label="angular_y")
                        sp_angularz = gr.Slider(
                            minimum=-5.0, maximum=5.0, value=0.0, step=0.1, interactive=True, label="angular_z")

                btn2 = gr.ClearButton(value="control", label="control")
                msg1 = gr.Textbox(lines=1, label="now control")

            with gr.Tab("action"):

                with gr.Row():

                    sitdown = gr.Button(value="sitdown", label="sitdown")
                    facedown = gr.Button(value="facedown", label="facedown")
                    handup = gr.Button(value="handup", label="handup")

                calibrate = gr.Button(value="calibrate", label="calibrate")

                btn2 = gr.ClearButton(value="control", label="control")

            with gr.Tab("voice"):
                with gr.Row():
                    voice = gr.components.Audio(
                        source="microphone", autoplay=True, type="filepath")
                    msg2 = gr.Textbox(lines=1, label="out voice")

            # change_button1 = gr.Button("(*'▽')いざ開始(*'▽')" ,scale = 1) # Buttonを使うと、ボタンを作成できる,ボタン共通
            # live = True
            # self.leg0.input(  # 書き方
            #     fn=self.mini_change,
            #     inputs=[self.leg0, self.leg1, self.leg2, self.leg3, self.leg4, self.leg5,
            #             self.leg6, self.leg7, self.leg8, self.leg9, self.leg10, self.leg11],
            # )

            # leg_control####################################################################################

            leg0.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
                outputs=[msg],
            )
            leg1.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
                outputs=[msg],
            )
            leg2.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
                outputs=[msg],
            )
            leg3.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
                outputs=[msg],
            )
            leg4.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
                outputs=[msg],
            )
            leg5.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
                outputs=[msg],
            )
            leg6.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
                outputs=[msg],
            )
            leg7.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
                outputs=[msg],
            )
            leg8.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
                outputs=[msg],
            )
            leg9.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
                outputs=[msg],
            )
            leg10.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],
                outputs=[msg],
            )
            leg11.input(  # 書き方
                fn=self.mini_change,
                inputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                        leg6, leg7, leg8, leg9, leg10, leg11],


                outputs=[msg],
            )

            face_image.upload(fn=self.publish_display,
                              inputs=[face_image],
                              outputs=[face_image],)

            btn1.click(
                fn=self.calibrate,
                outputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                         leg6, leg7, leg8, leg9, leg10, leg11])

            # speed_control############################################################################
            btn2.click(
                fn=self.ini_control,

                outputs=[sp_linearx, sp_lineary, sp_linearz, sp_angularx, sp_angulary, sp_angularz])

            sp_linearx.input(  # 書き方
                fn=self.count_walk,
                inputs=[sp_linearx, sp_lineary, sp_linearz,
                        sp_angularx, sp_angulary, sp_angularz],
                outputs=[msg1],
            )
            sp_lineary.input(  # 書き方
                fn=self.count_walk,

                inputs=[sp_linearx, sp_lineary, sp_linearz,
                        sp_angularx, sp_angulary, sp_angularz],
                outputs=[msg1],
            )
            sp_linearz.input(  # 書き方
                fn=self.count_walk,

                inputs=[sp_linearx, sp_lineary, sp_linearz,
                        sp_angularx, sp_angulary, sp_angularz],
                outputs=[msg1],
            )
            sp_angularx.input(  # 書き方
                fn=self.count_walk,

                inputs=[sp_linearx, sp_lineary, sp_linearz,
                        sp_angularx, sp_angulary, sp_angularz],
                outputs=[msg1],
            )
            sp_angulary.input(  # 書き方
                fn=self.count_walk,

                inputs=[sp_linearx, sp_lineary, sp_linearz,
                        sp_angularx, sp_angulary, sp_angularz],
                outputs=[msg1],
            )
            sp_angularz.input(  # 書き方
                fn=self.count_walk,

                inputs=[sp_linearx, sp_lineary, sp_linearz,
                        sp_angularx, sp_angulary, sp_angularz],
                outputs=[msg1],
            )

            # action#################################################################################
            sitdown.click(
                fn=self.sit_down,

                outputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                         leg6, leg7, leg8, leg9, leg10, leg11, msg])
            facedown.click(
                fn=self.face_down,
                outputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                         leg6, leg7, leg8, leg9, leg10, leg11, msg])
            handup.click(
                fn=self.the_hand,
                outputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                         leg6, leg7, leg8, leg9, leg10, leg11, msg])

            calibrate.click(
                fn=self.calibrate,
                outputs=[leg0, leg1, leg2, leg3, leg4, leg5,
                         leg6, leg7, leg8, leg9, leg10, leg11, msg])

            # leg0.value = joint[0]
            # leg1.value = joint[1]
            # leg2.value = joint[2]
            # leg3.value = joint[3]
            # leg4.value = joint[4]
            # leg5.value = joint[5]
            # leg6.value = joint[6]
            # leg7.value = joint[7]
            # leg8.value = joint[8]
            # leg9.value = joint[9]
            # leg10.value = joint[10]
            # leg11.value = joint[11]

            #################################################

            # そのまま起動https://discuss.huggingface.co/t/state-handling-and-live-mode-in-gradio-blocks/31837/2
            voice.change(
                fn=self.voice_chat,
                inputs=[voice],
                outputs=[msg2],


            )
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

    commander.get_up()

    commander.mini_gradio()

    rclpy.spin(commander)
    rclpy.shutdown()

    print('終了')


if __name__ == '__main__':
    main()