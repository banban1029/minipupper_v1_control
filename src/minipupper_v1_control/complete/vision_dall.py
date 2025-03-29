
# https://note.com/msfmnkns/n/n846bd5a61583
import glob
import base64
import os


from io import BytesIO
from PIL import Image


import openai


from openai import OpenAI

# APIキーの設定
openai.api_key = os.environ["OPENAI_API_KEY"]


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


files = glob.glob(
    "/home/banban/minipupper_control/src/mini_mini/mini_mini/images/*.png")
files = sorted(files)

# data
base64_image_3 = encode_image(files[3])
base64_image_4 = encode_image(files[4])
base64_image_7 = encode_image(files[7])
base64_image_8 = encode_image(files[8])
base64_image_9 = encode_image(files[9])
base64_image_11 = encode_image(files[11])
base64_image_14 = encode_image(files[14])
folder_name = "/home/banban/minipupper_control/src/mini_mini/mini_mini/outimage/"
filename = "image.png"

client = OpenAI()


def encode_image():

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

    print(response.choices[0].message.content)
    return response.choices[0].message.content


def make_face(making, feeling):

    # テキストからの画像生成の実行
    response = client.images.generate(
        model="dall-e-3",
        prompt=making+feeling,  # cute cat eared maid character in a cafe"
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="b64_json",


    )

    # base64を画像ファイルとして保存
    image_data = base64.b64decode(response.data[0].b64_json)
    image_stream = BytesIO(image_data)
    image = Image.open(image_stream)
    image.save("image.png")

    image.show()  # 画像表示
    print("SEIKOU")

    image.save(folder_name + '/' + filename)


def main():
    feeling = "shy face"
    data = encode_image()
    make_face(data, feeling)


if __name__ == '__main__':
    main()
