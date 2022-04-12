from distutils.command.upload import upload
from fileinput import filename
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from keras.preprocessing import image
import cv2
import numpy as np
from keras.models import model_from_json


root = Tk()
root.title("Sign Language to Text convertor")
root.geometry("1022x594")
root.iconbitmap("my_icon.ico")
background_image = PhotoImage(file="photu.png")
my_label = Label(root, image=background_image).place(relwidth=1, relheight=1)

def upload_file():
    f_types = [("Jpg files", "*.jpg"), ("PNG files", "*.png"), ("Jpeg files", "*.jpeg")]
    filename = filedialog.askopenfilename(filetypes=f_types)
    display_img = ImageTk.PhotoImage(file=filename)
    e1 = Label(root, image=display_img).place(x=457, y=230)
    file = str(filename)
    frame = cv2.imread(file)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img, (5, 5), 2)
    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imwrite(file, res)

    # making prediction
    fil_img = image.load_img(file, target_size=(128, 128), color_mode="grayscale")
    test_image = image.img_to_array(fil_img)
    test_image = np.expand_dims(test_image, axis=0)

    json_file = open("model-bw.json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model-bw.h5")

    result = loaded_model.predict(test_image)
    lis = [i for i in range(9)]
    prediction = {}
    prediction["blank"] = result[0][0]
    inde = 0
    sum = 0
    for i in lis:
        prediction[i] = result[0][inde]
        inde += 1
    max = 0
    output = 0
    for key, value in prediction.items():
        if key == "blank":
            continue
        sum += value
        if value > max:
            max = value
            output = key

    l3 = Label(root, text=str(output + 1), font="arial 24 bold", fg="white", width = 3, height = 1, bg="grey").place(x=640, y=455).pack()
    e1["image"] = display_img


def myIns():
    messagebox.showinfo("Instructions","1.Place your hand in front of the webcam.\n2.Show the Sign Language number in the square frame.\n3.Please wait till the image is processed.\n4.You will now get the desired output below.")

def myAbout():
    messagebox.showinfo("About", f"Sign Language to text {chr(169)}\nSahil, Saatvik, Anushka, Vithi")

btn_about = Button(padx=3,pady=3,bd=1,fg="blue",activeforeground="hotpink",activebackground="grey",font=("verdana", 10, "bold"),text="About",command=myAbout,borderwidth=0,).place(y=0, x=969)

btn_ins = Button(padx=3,pady=3,bd=1,fg="blue",activeforeground="hotpink",activebackground="grey",font=("verdana", 10, "bold"),text="Instruction",command=myIns,borderwidth=0,).place(y=0, x=0)

f1 = Frame(root, bg="white", bd=5, relief=SUNKEN).place(x=457, y=230, height=128, width=128)

button1 = Button(root,text="Choose File",fg="blue",activeforeground="hotpink",activebackground="grey",font=("verdana", 10, "bold"),width=13,height=1,command=lambda: upload_file(),).place(x=460, y=380)

root.mainloop()

