from keras.preprocessing import image
import cv2
from PIL import Image

# for i in range(960, 1200):
file = "D:\Mini_Project\dataset\single_prediction/3pls.jpg"
# img = Image.open(file)
# img = image.img_to_array(img)
# imgGray = img.convert('L')
frame = cv2.imread(file)
img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(img, (5, 5), 2)
th3 = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
)
ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# bw_img = "fil_" + str(i) + ".jpg"
# res.save(bw_img)
cv2.imwrite(file, res)
