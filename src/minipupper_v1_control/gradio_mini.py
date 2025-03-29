import numpy as np
#アプリ構成 修正中
import gradio as gr
import os

def mini_change(lf1,lf2,lf3,rf1,rf2,rf3,lb1,lb2,lb3,rb1,rb2,rb3):
    
    joint = [lf1,lf2,lf3,rf1,rf2,rf3,lb1,lb2,lb3,rb1,rb2,rb3]
    
    joints = np.array(joint)*np.pi/180.0
    
    return joints


mini = os.path.join(os.path.dirname(__file__), "/home/banban/Pictures/minipupper/mini_calibrate.png")

#インターフェイス作成
demo = gr.Blocks()

# my_theme = gr.Theme.from_hub('NoCrypt/miku')

#'ysharma/llamas' しまうま
#'ysharma/steampunk'　茶色×
#'HaleyCH/HaleyCH_Theme'　水色　best1 
#'xiaobaiyuan/theme_land'　美女　best2       2
#'ysharma/huggingface' huggingface　赤×
#'earneleh/paris'　青っぽいグラデーション
#'dwancin/theme@==0.1.1' 黄色×
#'freddyaboulton/test-blue' ×
#'NoCrypt/miku'　ミク　best3　　　　　　　　　　1
# with gr.Blocks(theme=my_theme) as demo:

with gr.Blocks() as demo:
    gr.Markdown( # Markdownを使うと、文章を表示できる 4つの半角で改行
    """
    **mini_pupper_getup!!**    
    Start trying to various your image.
    """)
    
    output = gr.Image(type="pil", value=mini)
    with gr.Row():
        
        with gr.Column():
            leg0 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lf1") #value start , step 1
            leg1 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lf2")
            leg2 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lf3")
            leg6 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lb1")
            leg7 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lb2")
            leg8 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="lb3")
            
        with gr.Column():
            leg3 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rf1")
            leg4 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rf2")
            leg5 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rf3")
            leg9 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rb1")
            leg10 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rb2")
            leg11 = gr.Slider(minimum=-180,maximum=180,value=0,step=1, interactive=True,label="rb3")
            
            
    
    change_button1 = gr.Button("(*'▽')いざ開始(*'▽')" ,scale = 1) # Buttonを使うと、ボタンを作成できる,ボタン共通
  
    
    
     
    change_button1.click( #書き方
        fn = mini_change,
        inputs = [leg0,leg1,leg2,leg3,leg4,leg5,leg6,leg7,leg8,leg9,leg10,leg11],
        outputs = [output],
        
    )

    

demo.launch(share = True)













# #アプリ構成 修正中
# import gradio as gr

# def hsv_change(input_img, h_deg, s_mag, v_mag):

#     img = cv2.imread(input_img) # 画像の読み込み
#     img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) # 色空間をBGRからHSVに変換
#     h_deg = int(h_deg) #色相(Hue)の回転度数
#     s_mag = float(s_mag) # 彩度(Saturation)の倍率
#     v_mag = float(v_mag) # 明度(Value)の倍率
    
#     img_hsv[:,:,(0)] = img_hsv[:,:,(0)]+h_deg # 色相の計算
#     img_hsv[:,:,(1)] = img_hsv[:,:,(1)]*s_mag # 彩度の計算
#     img_hsv[:,:,(2)] = img_hsv[:,:,(2)]*v_mag # 明度の計算
#     img_bgr = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2RGB) # 色空間をHSVからRGBに変換
 

#     return img_bgr


# #インターフェイス作成
# demo = gr.Blocks()

# # my_theme = gr.Theme.from_hub('NoCrypt/miku')

# #'ysharma/llamas' しまうま
# #'ysharma/steampunk'　茶色×
# #'HaleyCH/HaleyCH_Theme'　水色　best1 
# #'xiaobaiyuan/theme_land'　美女　best2       2
# #'ysharma/huggingface' huggingface　赤×
# #'earneleh/paris'　青っぽいグラデーション
# #'dwancin/theme@==0.1.1' 黄色×
# #'freddyaboulton/test-blue' ×
# #'NoCrypt/miku'　ミク　best3　　　　　　　　　　1
# # with gr.Blocks(theme=my_theme) as demo:
# with gr.Blocks() as demo:
#     gr.Markdown( # Markdownを使うと、文章を表示できる 4つの半角で改行
#     """
#     **次世代のAIbot搭載の画像編集アプリ!**    
#     Start trying to various your image.

#     """)

#     with gr.Tab("画像色相、彩度、明度編集"): # Tabを使うと、タブを作成できる
        
#         with gr.Row().style(equal_height=True):# Columnを使うと、縦に並べることができる
#             change_h = gr.Slider(minimum=0,maximum=180,value=0,step=1, interactive=True,label="色相何度回転")
#             change_s = gr.Slider(minimum=0,maximum=5,value=1,step=0.1, interactive=True, label="何倍、彩度を上げるか")
#             change_v = gr.Slider(minimum=0,maximum=5,value=1,step=0.1, interactive=True, label="何倍、明度を上げるか")
        
#         with gr.Row():

#             with gr.Column():
#                 with gr.Accordion("機能説明"): # Accordionを使うと、折りたたみができる
#                        gr.Markdown(
#                        """ h : 色相(色の種類) 0-180°で表現               
#                            s : 彩度(色の鮮やかさ) 0-100%で表現    
#                            v : 明度(色の明るさ) 0-100%で表現
#                        """)
#                 image_input1 = gr.Image(type="filepath",label="変換前", scale = 2)

#             with gr.Column():
                
#                 change_button1 = gr.Button("(*'▽')いざ開始(*'▽')" ,scale = 1) # Buttonを使うと、ボタンを作成できる,ボタン共通

#                 image_output1 = gr.Image(label="変換結果", scale = 2)

       
#     with gr.Tab("画像合成編集"):
#         with gr.Row().style(equal_height=True):

#             with gr.Column(): # Rowを使うと、横に並べることができる
#                 image_inputa = gr.Image(type="filepath",label="基画像")
#                 with gr.Accordion("機能説明書"): # Accordionを使うと、折りたたみができる
#                     gr.Markdown(
#                     """    
#                     基画像x,yは基写真のサイズを変えるものです。    
#                     x,y座標は基写真の背景上での位置を変えるものです。    
#                     """)
    

#                 image_inputb = gr.Image(type="filepath",label="背景画像")

#             with gr.Column():
#                 x_size = gr.Slider(scale = 1,minimum=0,maximum=300,value=300,step=50, interactive=True, label="基画像x")
#                 y_size = gr.Slider(scale = 1,minimum=0,maximum=300,value=300,step=50, interactive=True, label="基画像y")

#                 x_change = gr.Slider(scale = 1,minimum=0,maximum=300,value=10,step=5, interactive=True, label="x座標")
#                 y_change = gr.Slider(scale = 1,minimum=0,maximum=100,value=10,step=5, interactive=True, label="y座標")
#                 image_outputc = gr.Image(scale = 2,label="変換結果")
#                 change_button2 = gr.Button("(#^^#)いざ開始(#^^#)")
        
        
#     with gr.Tab("ボタン色変換編集"):
#         with gr.Row():

#             with gr.Column(): # Rowを使うと、横に並べることができる
#                 original_color = gr.Radio(["赤", "オレンジ","黄", "黄緑", "緑","青", "紫"], label="before_color") 
#                 change_color = gr.Radio(["赤", "オレンジ","黄", "黄緑", "緑","青", "紫"], label="after_color")
#                 change_button3 = gr.Button("(≧▽≦)いざ開始(≧▽≦)")
#                 with gr.Accordion("機能説明書"): # Accordionを使うと、折りたたみができる
#                         gr.Markdown(
#                         """
#                         .　 　7色対応しています　 　.        
#                         　　　　　基画像    
#                         　 　　before ⇒ after       
#                         　 　  　　　変換    
#                          自分の好きな色にしてみてください    
                               
#                         """)

#             with gr.Column():
#                 image_input3 = gr.Image(type="filepath",label="基画像")
                
#                 image_output3 = gr.Image(label="変換後")

#     with gr.Tab("voice色変換編集"):
#         with gr.Row():

#             with gr.Column(): # Rowを使うと、横に並べることができる
#                 audio = gr.components.Audio(source="microphone",type="filepath")
#                 change_button4 = gr.Button("(≧▽≦)いざ開始(≧▽≦)")
#                 voice_output = gr.outputs.Textbox(label = "文字起こし結果")
#                 with gr.Accordion("機能説明書"): # Accordionを使うと、折りたたみができる
#                         gr.Markdown(
#                         """
#                         音声により説明しAIが文字起こしを行いその文字をもとに色変換を行う。
#                         赤、オレンジ、黄、黄緑、緑、青、紫の7色に対応しています。                         
#                         　　　　　　　　　　　　　基画像    
#                         　 　　　　　　　　　　before ⇒ after       
#                         　 　  　　　　　　　　　　　変換    

#                         赤から青にしたい場合の例    
#                         「赤から青」、「赤から青にしてください」    
#                         「AIってほんとに凄いのか?、赤から青にしてみろよ」     
                           
#                         """)
                

#             with gr.Column():
#                 image_input4 = gr.Image(type="filepath",label="基画像")
                
#                 image_output4 = gr.Image(label="変換後")
    
#     with gr.Tab("advice_chat"):
#         # チャットボットUI処理
#         gr.Markdown( # Markdownを使うと、文章を表示できる 4つの半角で改行
#         """
#         　**H e l l o.　I　k n o w　a b o u t　HSV. 　I　c a n 　h e l p　y o u r　p h o t o　P r o c e s s i n g 　!　!**　
#         """)
#         chatbot = gr.Chatbot(label="chat_room")
#         input = gr.Textbox(show_label=False, placeholder="メッセージを入力してね").style(container=False)
#         input.submit(fn=advice_chat, inputs=input, outputs=chatbot) # メッセージ送信されたら、AIと会話してチャット欄に全会話内容を表示
#         input.submit(fn=lambda: "", inputs=None, outputs=input) # （上記に加えて）入力欄をクリア

#     with gr.Accordion("どんなアプリ？"): # Accordionを使うと、折りたたみができる
#         gr.Markdown(
#         """Look at me...    
#         私の名前は、banbanです。    
#         夢は、世界一の画像編集アプリを作ることです。    
#         今回作成したのは大きく分けて5つ。    
#         1.色相、彩度、明度変換    
#         2.画像合成    
#         3.ボタン色変換    
#         4.voice色変換    
#         5.advice_chat        
#         このアプリは、今話題のAIをも利用し、    
#         もっと画像編集の楽しさを知り、新しい画像作成ができることを目的としています。    
#         これらの機能を使って、あなたの写真を美しく、綺麗なものに編集してみてください。 
#         """)

    
    
     
#     change_button1.click( #書き方
#         fn = hsv_change,
#         inputs = [image_input1, change_h, change_s, change_v],
#         outputs = image_output1
#     )

#     change_button2.click( #書き方
#         fn = fusion_back,
#         inputs = [image_inputa, image_inputb,x_change,y_change,x_size,y_size],
#         outputs = image_outputc
#     )   

#     change_button3.click( #書き方
#         fn = r_color_change,
#         inputs = [image_input3, original_color, change_color],
#         outputs = image_output3
#     )

#     change_button4.click( #書き方
#         fn = v_color_change,
#         inputs = [image_input4, audio],
#         outputs = [image_output4,voice_output],
#     )

# demo.launch(share = True)


