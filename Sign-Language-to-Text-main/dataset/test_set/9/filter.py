from PIL import Image

for i in range(960,1200):
    file = "9/" + str(i) + ".jpg"
    img = Image.open(file)
    imgGray = img.convert('L')
    bw_img = "bw_" + str(i) + ".jpg"
    imgGray.save(bw_img)