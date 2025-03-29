

import openai
import gradio as gr
# from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io

import os
import openai


# ChatGPTによる会話の関数

# new
from openai import OpenAI


# APIキーの設定
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()


def chat(input_text):
    
    
    completion = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="Say this is a test",
        
        temperature=0
    )


    response = client.chat.completions.create(
        model="gpt-4-1106-preview ",  # "gpt-4-1106-preview",
        messages=[
            {'role': 'system', 'content': 'あなたは犬型ロボットで従順なペットです。今から飼い主があなたに命令をします。'},
            {'role': 'system', 'content': '''次のtemplateに従って命令を実行してください。

                template = “[action]、[face]”

                [action]="座る" or "伏せる" or "お手" or ”表情を変える”
                [face]= どのような表情をしてほしいか。表情の画像生成モデルを作成可能なプロンプト

                '''},

            ここで設定（会話相手の人格など）を変更できます。
            {"role": "user", "content": input_text}
            # ここにユーザーの発言が入ります。

        ],


        # stream=True,


        # temperature=0.0,
        # 創造性を調整します。1.0が上限です。
    )

    result = response.choices[0].message.content

    print(result)

    return result




def mini_gradio():

    with gr.Blocks() as demo:
        gr.Markdown(  # Markdownを使うと、文章を表示できる 4つの半角で改行
            """
        **mini_pupper_getup!!**    
        Start trying to various your image.
        """)
        with gr.Tab("action"):
            with gr.Row():
                action = gr.Textbox(lines=1, label="now control")
                out = gr.Textbox(lines=1, label="now control")

            btn = gr.Button(value="control", label="control")
        # change_button1 = gr.Button("(*'▽')いざ開始(*'▽')" ,scale = 1) # Buttonを使うと、ボタンを作成できる,ボタン共通
        # change_button2 = gr.Button("(*'▽')いざ開始(*'▽')" ,scale = 1) # Buttonを使うと、ボタンを作成できる,ボタン共通

        btn.click(
            fn=chat,
            inputs=[action],
            outputs=[out])

    demo.launch(share=True)


def main():
    mini_gradio()


if __name__ == "__main__":
    main()
