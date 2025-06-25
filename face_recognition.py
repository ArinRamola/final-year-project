from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
import mysql.connector
from time import strftime
from datetime import datetime

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition")
        self.root.resizable(False, False)
        
        title_label = Label(self.root, text="FACE RECOGNITION",
                            font=("times new roman", 35, "bold"), bg="white", fg="green")
        title_label.place(x=0, y=0, width=1530, height=50)
        
        img_left = Image.open("images/FaceDetectionImage.png")
        img_left = img_left.resize((650, 700), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)

        lbl_left = Label(self.root, image=self.photoimg_left)
        lbl_left.place(x=0, y=55, width=650, height=700)

        img_right = Image.open("images/FaceScan.png")
        img_right = img_right.resize((950, 700), Image.Resampling.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)

        lbl_right = Label(self.root, image=self.photoimg_right)
        lbl_right.place(x=650, y=55, width=950, height=700)
        
        self.button = Button(lbl_right, command=self.face_recognition, text="Face Recognition",
                             cursor="hand2", font=("times new roman", 18, "bold"),
                             bg="darkgreen", fg="white")
        self.button.place(x=380, y=615, width=200, height=40)
        
    def mark_attendance(self, i, r, n, d):
        filename = "Attendance.csv"
        
        if not os.path.exists(filename):
            with open(filename, "w", newline="\n") as f:
                f.write("Student_ID,Roll,Name,Department,Time,Date,Status\n")
        
        now = datetime.now()
        today_date = now.strftime("%d/%m/%Y")
        already_marked = False
        
        try:
            with open(filename, "r", newline="\n") as f:
                lines = f.readlines()
                if len(lines) > 1:
                    for line in lines[1:]:
                        if line.strip():
                            entry = line.strip().split(",")
                            if len(entry) >= 6:
                                if entry[0] == str(i) and entry[5] == today_date:
                                    already_marked = True
                                    break
        except Exception as e:
            print(f"Error reading attendance file: {e}")
            return
        
        if not already_marked:
            try:
                with open(filename, "a", newline="\n") as f:
                    dtString = now.strftime("%H:%M:%S")
                    f.write(f"{i},{r},{n},{d},{dtString},{today_date},Present\n")
                    print(f"Attendance marked for {n} (ID: {i})")
            except Exception as e:
                print(f"Error writing to attendance file: {e}")
        else:
            print(f"Attendance already marked today for {n} (ID: {i})")

    def face_recognition(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            coord = []

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                conn = None
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        username="root",
                        password="Adiarinkadaddy@22041426",
                        database="facial_recognition"
                    )
                    my_cursor = conn.cursor()

                    my_cursor.execute("SELECT Name FROM student WHERE Student_id = %s", (id,))
                    n = my_cursor.fetchone()
                    n = "+".join(n) if n else "Unknown"

                    my_cursor.execute("SELECT Roll FROM student WHERE Student_id = %s", (id,))
                    r = my_cursor.fetchone()
                    r = "+".join(r) if r else "Unknown"

                    my_cursor.execute("SELECT Dept FROM student WHERE Student_id = %s", (id,))
                    d = my_cursor.fetchone()
                    d = "+".join(d) if d else "Unknown"
                    
                    my_cursor.execute("SELECT Student_id FROM student WHERE Student_id = %s", (id,))
                    i = my_cursor.fetchone()
                    i = "+".join(i) if i else "Unknown"

                except mysql.connector.Error as err:
                    print(f"Database error: {err}")
                    i, r, n, d = "Unknown", "Unknown", "Unknown", "Unknown"
                finally:
                    if conn and conn.is_connected():
                        conn.close()

                if confidence > 77:
                    cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name: {n}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Roll: {r}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    self.mark_attendance(i, r, n, d)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                coord = [x, y, w, h]

            return coord

        def recognize(img, clf, faceCascade):
            draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Welcome to Face Recognition", img)

            if cv2.waitKey(1) == 13:
                break

        video_cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    app = Face_Recognition(root)
    root.mainloop()
