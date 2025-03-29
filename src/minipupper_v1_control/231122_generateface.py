
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

base64_image_0 = encode_image(files[0])
base64_image_1 = encode_image(files[1])
base64_image_2 = encode_image(files[2])
base64_image_3 = encode_image(files[3])
base64_image_4 = encode_image(files[4])
base64_image_5 = encode_image(files[5])
base64_image_6 = encode_image(files[6])
base64_image_7 = encode_image(files[7])
base64_image_8 = encode_image(files[8])
base64_image_9 = encode_image(files[9])
base64_image_10 = encode_image(files[10])
base64_image_11 = encode_image(files[11])
base64_image_12 = encode_image(files[12])
base64_image_14 = encode_image(files[14])


client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
          "role": "user",  # "Genarate prompts what’s in these image to make ?"
          "content": [
              {"type": "text", "text": "Read the features from these images and create prompts that can generate images in a format similar to these."},
              {
                  "type": "image_url",
                  "image_url": {
                      "url": f"data:image/jpeg;base64,{base64_image_3}"
                  },
              },
              {
                  "type": "image_url",
                  "image_url": {
                      "url": f"data:image/jpeg;base64,{base64_image_4}"
                  },
              },
              {
                  "type": "image_url",
                  "image_url": {
                      "url": f"data:image/jpeg;base64,{base64_image_5}"
                  },
              },
              {
                  "type": "image_url",
                  "image_url": {
                      "url": f"data:image/jpeg;base64,{base64_image_6}"
                  },
              },
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
                      "url": f"data:image/jpeg;base64,{base64_image_10}"
                  },
              },
              {
                  "type": "image_url",
                  "image_url": {
                      "url": f"data:image/jpeg;base64,{base64_image_11}"
                  },
              },
              {
                  "type": "image_url",
                  "image_url": {
                      "url": f"data:image/jpeg;base64,{base64_image_14}"
                  },
              },







          ],
        }
    ],
    max_tokens=300,
)

# print(response.choices[0])
print("回答:" + response.choices[0].message.content)

# # print(response.choices[0])
# print("回答:" + response.choices[0].message.content)
