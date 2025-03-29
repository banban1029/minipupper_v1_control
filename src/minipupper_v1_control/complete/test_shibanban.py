
# https://note.com/msfmnkns/n/n846bd5a61583
import glob
import base64
import os
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


base64_image_15 = encode_image(files[15])

base64_image_16 = encode_image(files[16])


client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
          "role": "user",
          "content": [
              {"type": "text", "text": "これは何の画像ですか？"},
              {
                  "type": "image_url",
                  "image_url": {
                      "url":  f"data:image/jpeg;base64,{base64_image_15}",
                  },
              },
              {
                  "type": "image_url",
                  "image_url": {
                      "url":  f"data:image/jpeg;base64,{base64_image_16}",
                  },
              },

          ],
        }
    ],
    max_tokens=1000,
)

# print(response.choices[0])
print("回答:" + response.choices[0].message.content)

# # print(response.choices[0])
# print("回答:" + response.choices[0].message.content)
