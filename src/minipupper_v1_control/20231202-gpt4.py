# https://note.com/npaka/n/ne99c12b77ebc

from io import BytesIO
from PIL import Image
from openai import OpenAI

import glob
import base64
import os

import openai

from openai import OpenAI

# APIキーの設定
openai.api_key = os.environ["OPENAI_API_KEY"]

# クライアントの準備
client = OpenAI()
# テキストからの画像生成の実行
response = client.images.generate(
    model="dall-e-3",
    prompt="yosakoi dancer in a festival",
    size="1024x1024",
    quality="standard",
    n=1,
    response_format="b64_json",
)

folder_name = "/home/banban/minipupper_control/src/mini_mini/mini_mini/outimage/"
filename = "image.png"

# base64を画像ファイルとして保存
image_data = base64.b64decode(response.data[0].b64_json)
image_stream = BytesIO(image_data)
image = Image.open(image_stream)
image.save("image.png")

image.show()  # 画像表示
print("SEIKOU")


image.save(folder_name + '/' + filename)
