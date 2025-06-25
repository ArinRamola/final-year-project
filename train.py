from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import cv2
import numpy as np

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Training Data")
        self.root.resizable(False, False)

        title_label = Label(self.root, text="TRAIN DATA SET",
                            font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_label.place(x=0, y=0, width=1530, height=50)
        
        img_top = Image.open("images/FaceDetectionImage.png")
        img_top = img_top.resize((1530, 325), Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        lbl_top = Label(self.root, image=self.photoimg_top)
        lbl_top.place(x=0, y=55, width=1530, height=325)
        
        self.button = Button(self.root, text="Train Data", command=self.train_classifier,
                             cursor="hand2", font=("times new roman", 30, "bold"),
                             bg="red", fg="white")
        self.button.place(x=0, y=380, width=1530, height=60)
        
        img_bottom = Image.open("images/FaceDetectionImage.png")
        img_bottom = img_top.resize((1530, 325), Image.Resampling.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_top)

        lbl_bottom = Label(self.root, image=self.photoimg_bottom)
        lbl_bottom.place(x=0, y=440, width=1530, height=325)
        
    def train_classifier(self):
        data_dir = "data"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(".jpg")]

        faces = []
        ids = []

        for image_path in path:
            img = Image.open(image_path).convert('L')
            image_np = np.array(img, 'uint8')

            filename = os.path.split(image_path)[1]
            try:
                id = int(filename.split('.')[1])
            except (IndexError, ValueError):
                print(f"Skipping file with invalid name: {filename}")
                continue

            faces.append(image_np)
            ids.append(id)
            cv2.imshow("Training", image_np)
            cv2.waitKey(1) == 13

        if not faces:
            messagebox.showerror("Error", "No valid training images found in 'data' folder")
            return

        ids = np.array(ids)

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Training data set completed successfully")
