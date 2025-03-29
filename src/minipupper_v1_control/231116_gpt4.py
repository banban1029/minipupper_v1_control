# https://chmod774.com/gpt4-vision-api/

import glob
import base64
import os

import openai

from openai import OpenAI

# APIキーの設定
openai.api_key = os.environ["OPENAI_API_KEY"]

# client = OpenAI()

# response = client.chat.completions.create(
#     model="gpt-4-vision-preview",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "この画像は何?"},
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
#                     },
#                 },
#             ],
#         }
#     ],
#     max_tokens=300,
# )

# print(response.choices[0])


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


files = glob.glob(
    "/home/banban/minipupper_control/src/mini_mini/mini_mini/images/*.png")
files = sorted(files)


# 例 /Users/user/images_folder/image.png
image_path = files[0]
base64_image = encode_image(image_path)

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "この画像の女性を熱意を持って褒めてください"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        }
    ],
    max_tokens=300,
)

# print(response.choices[0])
print("回答:" + response.choices[0].message.content)
