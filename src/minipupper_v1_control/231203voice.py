# https://bocek.co.jp/media/ai-development/849/
# https://weel.co.jp/media/gpt-4-turbo
# https://www.nextsurprise.jp/568/
# https://book.st-hakky.com/data-science/open-ai-api-in-python/

# https://stackoverflow.com/questions/77469966/openai-api-error-you-tried-to-access-openai-completion-but-this-is-no-longer
# completions.create  now　　　response.choices[0].message.content
# Completion.create  old　　　　response["choices"][0]["message"]["content"]
# https://github.com/openai/openai-python/discussions/742
# https://stackoverflow.com/questions/77444332/openai-python-package-error-chatcompletion-object-is-not-subscriptable

from openai import OpenAI
import glob
import base64
import openai
import gradio as gr
# from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io

import os
import openai


# APIキーの設定
openai.api_key = os.environ["OPENAI_API_KEY"]


client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

# APIキーの設定
openai.api_key = os.environ["OPENAI_API_KEY"]


client = OpenAI()


def chat(input_text):

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
def speech_to_text(input_audio):
    audio_file = open(input_audio, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    return transcript


# # テキストから音声への変換関数
# def text_to_speech(input_text):
#     tts = gTTS(text=input_text, lang="ja")
#     # テキストから音声に変換
#     tts.save("sample.mp3")
#     # 音声ファイルに保存
#     sound = AudioSegment.from_mp3("sample.mp3")
#     sound_speedup = sound.speedup(playback_speed=1.5)
#     # 読み上げスピードを上げる
#     sound_speedup.export("sample.mp3", format="mp3")
#     return "sample.mp3"
# 音声会話アプリの関数（今までの関数の組み合わせ）


def record_keywodrs(text, keyreords):

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


def voice_chat(input_audio):

    key_recorder = []
    key_recorder.clear()

    text = speech_to_text(input_audio)

    # 音声をテキストに
    response_text = chat(text)

    print(response_text)

    record_keywodrs(response_text, key_recorder)

    input_action = key_recorder[0]
    input_face = key_recorder[1]

    print(input_action)
    print(input_face)

    key_recorder.clear()
    # 返答を音声に
    # return response_audio


# Gradioインターフェース
gr.Interface(
    fn=voice_chat,
    inputs=gr.components.Audio(source="microphone", type="filepath"),
    # outputs=gr.components.Audio(type="numpy"),
    outputs=gr.components.Audio(type="numpy"),
    examples=[],
).launch()
