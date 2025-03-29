import matplotlib.pyplot as plt
import glob
import cv2

# files = glob.glob("/home/banban/Pictures/**/*.png")

files = glob.glob("/home/banban/minipupper_control/src/mini_mini/mini_mini/images/*.png")

files = sorted(files)

print(files[0])

msg = cv2.imread(files[0])

cv2.imshow("image", msg)

cv2.waitKey(0)
cv2.destroyAllWindows()
