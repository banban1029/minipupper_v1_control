
# https://ichi.pro/python-o-shiyoshita-kao-no-hyojo-kara-no-kanjo-ninshiki-no-kyukyoku-no-gaido-110937080276223
from fer import FER

# %matplotlib inline
# pip install tensorflow[and-cuda]
# GPUE error reboot
# nvidia-smi


import matplotlib.pyplot as plt


import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
with tf.device('/GPU:0'):

    # image_path = "/home/banban/minipupper_control/src/mini_mini/mini_mini/images/greatshot.png"
    test_image_one = plt.imread(
        "/home/banban/minipupper_control/src/mini_mini/mini_mini/images/11_trot.png")
    emo_detector = FER(mtcnn=True)
    # Capture all the emotions on the image
    captured_emotions = emo_detector.detect_emotions(test_image_one)
    # Print all captured emotions with the image
    print(captured_emotions)
    plt.imshow(test_image_one)

    # Use the top Emotion() function to call for the dominant emotion in the image
    dominant_emotion, emotion_score = emo_detector.top_emotion(test_image_one)
    print(dominant_emotion, emotion_score)


# apt-get update
