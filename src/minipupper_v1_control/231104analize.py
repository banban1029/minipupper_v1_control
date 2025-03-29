# 必要なライブラリをインポート
import spacy
import tkinter as tk
import re
import os
import glob


# files = glob.glob(
#     "/home/banban/minipupper_control/src/mini_mini/mini_mini/images/*.png")
# files = sorted(files)


files = glob.glob(
    "/home/banban/minipupper_control/src/mini_mini/mini_mini/images/*")
files = sorted(files)

# tkinterを用いてGUIを作成
root = tk.Tk()  # ウィンドウを作成
root.title(u'東京工業大学高村先生の作成した単語感情極性対応表を用いたGiNZAによる感情分析プログラム')
root.geometry('670x450')  # ウィンドウのサイズを設定
img = tk.PhotoImage(file=files[12])  # イメージを読み込み
cvs = tk.Canvas(width=670, height=400)  # イメージを載せるキャンバスのサイズ
cvs.pack()
cvs.create_image(330, 200, image=img)  # イメージのサイズ設定
txt = '分析したい文章を入力してください。感情スコア(0～100点)を表示します。'
msg = tk.Label(text=txt, fg='black', bg='green yellow')  # テキスト（ラベル）を設定
msg.place(x=10, y=10)  # テキスト（ラベル）を設置

path = os.getcwd()  # パスを取得

nlp = spacy.load('ja_ginza_electra')  # GiNZAのロード
t = 1


def feel():  # ボタンを押したらこの関数を実行
    global t  # ラベルの位置を決めるための変数
    s = textF.get()  # 入力したテキストを取得
    msg = tk.Label(text=s, fg='black', bg='white')  # テキスト（ラベル）を設定
    msg.place(x=10, y=10+t*30)  # テキスト（ラベル）を設置
    t = t+1
    textF.delete(0, 'end')  # テキストボックスの文字を削除
    doc = nlp(s)  # GiNZAによる入力したテキストの解析
    words = []  # 分割した単語を保持する配列
    score = 0
    for sent in doc.sents:  # 文章群の中から文章を一つずつ抽出
        for token in sent:  # 文章の中から形態素を一つずつ抽出
            if token.pos_ == 'PROPN' or token.pos_ == 'NOUN':  # 名詞を抽出
                words.append(token.lemma_)  # 原形をリストに追加
    with open('/home/banban/minipupper_control/src/mini_mini/mini_mini/toukou_pn.txt', encoding='cp1252') as f:  # コーパスを読み込み　ANSI
        text = f.read()  # 文字を読み込み
        dic = re.split('\n|:', text)  # 改行と：で分割
    for word in words:
        for i in range(int(len(dic)/4)):
            if dic[4*i+2] == '名詞':  # 属性が名詞の場合
                if dic[4*i] == word or dic[4*i+1] == word:
                    score = score+float(dic[4*i+3])  # 単語の極性を足し合わせる
    a = len(words)  # 文章に含まれていた名詞の数を保持
    for sent in doc.sents:  # 文章群の中から文章を一つずつ抽出
        for token in sent:  # 文章の中から形態素を一つずつ抽出
            if token.pos_ == 'VERB' or token.pos_ == 'ADJ' or token.pos_ == 'ADV':  # 用言を抽出
                words.append(token.lemma_)  # 原形をリストに追加
    with open('/home/banban/minipupper_control/src/mini_mini/mini_mini/toukou_pn.txt', encoding='cp1252') as f:  # コーパスを読み込み　ANSI
        text = f.read()  # 文字を読み込み
        dic = re.split('\n|:', text)  # 改行と：で分割
    for word in words:
        for i in range(int(len(dic)/4)):
            if dic[4*i+2] == '動詞' or dic[4*i+2] == '形容詞' or dic[4*i+2] == '副詞':  # 属性が動詞、形容詞、副詞の場合
                if dic[4*i] == word or dic[4*i+1] == word:
                    score = score+float(dic[4*i+3])  # 単語の極性を足し合わせる
    b = len(words)  # 文章に含まれていた用言の数を保持

    c = (((score/(a+b))+1)*50)  # 得られた極性の和を単語数で割る
    msg = tk.Label(text='文章中の感情スコアは'+str(c)+'点)',
                   fg='black', bg='green yellow')  # 感情スコアを表示
    msg.place(x=10, y=10+t*30)
    # 感情スコアに応じて音声を再生
    if c > 75:
        os.system('ずんだもん喜.wav')
    elif c >= 50 and c <= 75:
        os.system('ずんだもんえーと.wav')
    elif c < 50:
        os.system('ずんだもん落.wav')
    t = t+1


# ボタンとテキストボックスの定義
btn = tk.Button(root, text='送信', font=(
    'utf-8_sig', 10), bg='cyan', command=feel)
btn.pack(side='right')
textF = tk.Entry(root, font=('utf-8_sig', 15), width=64)
textF.pack(side='right')
# 画面の保持
root.mainloop()
