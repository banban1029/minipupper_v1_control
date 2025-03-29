
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


from io import BytesIO
# from PIL import Image 被りでエラー
import base64


from openai import OpenAI
import openai
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()


# ファイル先
files = glob.glob(
    "/home/banban/minipupper_control/src/mini_mini/mini_mini/images/*.png")
files = sorted(files)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


base64_image_7 = encode_image(files[7])
base64_image_8 = encode_image(files[8])
base64_image_9 = encode_image(files[9])
base64_image_11 = encode_image(files[11])
folder_name = "/home/banban/minipupper_control/src/mini_mini/mini_mini/outimage/"
filename = "image.png"


class Commander(Node):

    def __init__(self):
        super().__init__('commander')

        self.display_publisher = self.create_publisher(
            Image, 'mini_pupper_lcd/image_raw', 10)

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

    def make_face(self, making, feeling):

        instruction = "Please" + feeling + "emotions\n" + making

        # テキストからの画像生成の実行
        response = client.images.generate(
            model="dall-e-3",
            prompt=instruction,  # cute cat eared maid character in a cafe"
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="b64_json",

        )

        print(response.data[0].b64_json)
        # base64を画像ファイルとして保存

        # image_stream = BytesIO(image_data)
        # print(image_stream)

        # image = Image.open(image_stream)

        # image.show()  # 画像表示
        print("SEIKOU")

        name = folder_name + '/' + filename

        image.save(name)

        # image.save(name)

        print(name)

        rgb = self.publish_display(name)

        return rgb

    def encode_image(self, input_audio):

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                  "role": "user",  # "Genarate prompts what’s in these image to make ?"
                  "content": [
                      {"type": "text", "text": "These are face. Read the features from these images and create prompts that can generate images in a format similar to these."},
                      {"type": "text", "text": '''画像全体を通して次のtemplateに従って命令に沿うプロンプトを一つ作成してください

                        template = “[color]\n[pattern]\n[features]”

                        [color]= 色の指定、色の種類、色の濃さなど
                        [pattern]= 模様の種類、配置、大きさなど
                        [features]= 画像の特徴、目の形、鼻の形、口の形、顔の形、髪の形、髪の色、服の形、服の色、服の柄、服の装飾など
                        '''},

                      {
                          "type": "image_url",
                          "image_url": {
                              "url": f"data:image/jpeg;base64,{base64_image_7}"
                          },
                      },
                      {
                          "type": "image_url",
                          "image_url": {
                              "url": f"data:image/jpeg;base64,{base64_image_8}"
                          },
                      },
                      {
                          "type": "image_url",
                          "image_url": {
                              "url": f"data:image/jpeg;base64,{base64_image_9}"
                          },
                      },
                      {
                          "type": "image_url",
                          "image_url": {
                              "url": f"data:image/jpeg;base64,{base64_image_11}"
                          },
                      },

                  ],
                }
            ],
            max_tokens=300,
        )

        data = response.choices[0].message.content
        feeling = self.speech_to_text(input_audio)

        img = self.make_face(data, feeling)

        return response.choices[0].message.content, img

    # 音声からテキストへの変換関数
    def speech_to_text(self, input_audio):
        audio_file = open(input_audio, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return transcript

    def mini_gradio(self):

        with gr.Blocks() as demo:
            gr.Markdown(  # Markdownを使うと、文章を表示できる 4つの半角で改行
                """
            **mini_pupper_getup!!**    
            Start trying to various your image.
            """)

            with gr.Tab("voice"):
                with gr.Row():
                    voice = gr.components.Audio(
                        source="microphone", autoplay=True, type="filepath")
                    msg2 = gr.Textbox(lines=1, label="out voice")

                with gr.Row():
                    gr.Image(
                        type="pil", value=files[12], label="mini_pupper")

                    # type="pil", label="makeimage"
                    make_image = gr.Image(type="filepath", label="face")

                    gr.Image(
                        type="pil", value=files[13], label="mini_pupper")
                with gr.Row():
                    makeface = gr.components.Audio(
                        source="microphone", autoplay=True, type="filepath", label="makeface")
                    msg3 = gr.Textbox(lines=1, label="out voice")

            # change_button1 = gr.Button("(*'▽')いざ開始(*'▽')" ,scale = 1) # Buttonを使うと、ボタンを作成できる,ボタン共通
            # live = True
            # self.leg0.input(  # 書き方
            #     fn=self.mini_change,
            #     inputs=[self.leg0, self.leg1, self.leg2, self.leg3, self.leg4, self.leg5,
            #             self.leg6, self.leg7, self.leg8, self.leg9, self.leg10, self.leg11],
            # )

            # action#################################################################################

            # そのまま起動https://discuss.huggingface.co/t/state-handling-and-live-mode-in-gradio-blocks/31837/2

            makeface.change(
                fn=self.encode_image,
                inputs=[makeface],
                outputs=[msg3, make_image],
            )

            demo.launch(share=True)


def main():
    # ROSクライアントの初期化
    rclpy.init()

    # ノードクラスのインスタンス
    commander = Commander()

    commander.mini_gradio()

    rclpy.spin(commander)
    rclpy.shutdown()

    print('終了')


if __name__ == '__main__':
    main()
