
# https://aiacademy.jp/media/?p=3492

#!pip install diffusers==0.8.0 transformers scipy ftfy
# packageでアンインストール　　

# import matplotlib.pyplot as plt
# import torch
# from torch import autocast
# from diffusers import StableDiffusionPipeline

# access_token = """

# # モデルのダウンロード
# model = StableDiffusionPipeline.from_pretrained(
#     "CompVis/stable-diffusion-v1-4", use_auth_token=access_token)
# model.to("cuda")


# num = 1  # 生成したい画像枚数
# prompt = "Horse flying in the sky"  # 生成させたいもととなる文章

# for i in range(num):
#     image = model(prompt)["sample"][0]
#     # 保存
#     image.save(
#         f"/home/banban/minipupper_control/src/mini_mini/mini_mini/outimage/{i}.png")

#     # outputsフォルダに保存された画像を描画
# for i in range(num):
#     plt.imshow(plt.imread(
#         f"/home/banban/minipupper_control/src/mini_mini/mini_mini/outimage/{i}.png"))
#     plt.axis('off')
#     plt.show()

#     plt.imshow(plt.imread(
#         f"/home/banban/minipupper_control/src/mini_mini/mini_mini/outimage/{i}.png"))


import torch
from diffusers import StableDiffusionPipeline
from torch import autocast

MODEL_ID = "CompVis/stable-diffusion-v1-4"
DEVICE = "cuda"
YOUR_TOKEN = ""  # input topken

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID, revision="fp16", torch_dtype=torch.float16, use_auth_token=YOUR_TOKEN)
pipe.to(DEVICE)

prompt = "a dog painted by Katsuhika Hokusai"

with autocast(DEVICE):
    image = pipe(prompt, guidance_scale=7.5)["sample"][0]
    image.save("test.png")
