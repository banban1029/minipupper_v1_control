import openai
import base64
import glob
import os
from openai import OpenAI
client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

# completion = client.completions.create(
#     model="gpt-3.5-turbo-instruct",
#     prompt="Say this is a test",
#     max_tokens=7,
#     temperature=0
# )

# print(completion.choices[0].text)


# APIキーの設定
openai.api_key = os.environ["OPENAI_API_KEY"]


client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {'role': 'system', 'content': 'あなたは犬型ロボットで従順なペットです。今から飼い主があなたに命令をします。'},
        {'role': 'system', 'content': '''次のtemplateに従って命令を実行してください。
             
            template = “[action]\n[face]\n”
            
            [action]="座る" or "伏せる" or "お手" or ”表情を変える”
            [face]= 自分にどのような表情をしてほしいか。”喜び" or "悲しみ" or "怒り" or "癒やし"のうちどれかを選んでください。
        
            '''},

        # ここで設定（会話相手の人格など）を変更できます。
        {"role": "user", "content": input()}
        # ここにユーザーの発言が入ります。
    ],
    temperature=0.0,
    # 創造性を調整します。1.0が上限です。
)


# print(response.choices[0])
print(response.choices[0].message.content)
