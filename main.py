from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import webbrowser

from student import Student
from train import Train
from face_recognition import Face_Recognition
from materials import MaterialWindow
from converter_tools import ConverterTools
from assistant import Assistant
from Attendance import Attendance

from chat.chat_client_window import ChatClientWindow  

class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("EDUVERSE")

        # ================== Background Image ==================
        bg_image = Image.open("images/Background.png")
        bg_image = bg_image.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photo_bg = ImageTk.PhotoImage(bg_image)

        self.bg_label = Label(self.root, image=self.photo_bg)
        self.bg_label.place(x=0, y=130, width=1530, height=710)

                # ================== Header Images ==================
        img1 = Image.open("images/image1.png").resize((150, 130), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimg1).place(x=0, y=0, width=150, height=130)

        img3 = Image.open("images/image3.png").resize((410, 130), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        Label(self.root, image=self.photoimg3).place(x=150, y=0, width=410, height=130)

        img2 = Image.open("images/image2.jpeg").resize((410, 130), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        Label(self.root, image=self.photoimg2).place(x=560, y=0, width=410, height=130)

        img4 = Image.open("images/image3.png").resize((560, 130), Image.Resampling.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)
        Label(self.root, image=self.photoimg4).place(x=970, y=0, width=560, height=130)

        # ================== Title ==================
        title_label = Label(self.bg_label, text="EDUVERSE- Online Learning Platform",
                            font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_label.place(x=0, y=0, width=1530, height=50)

        # ================== Button Definitions ==================

        
        self.create_button("images/student.png", "Student Details", 200, 100, self.students_details)
        self.create_button("images/FaceDetector.png", "Face Detector", 500, 100, self.face_data)
        self.create_button("images/Attendance.png", "Attendance", 800, 100, self.attendance_details)
        self.create_button("images/VideoCall.png", "Video Call", 1100, 100, self.video_call)

        
        self.create_button("images/Assistant_Image.png", "Assistant", 200, 380, self.open_assistant)
        self.create_button("images/chatroom.png", "Chat Room", 500, 380, self.open_chat_room)
        self.create_button("images/resources.png", "Resources", 800, 380, self.open_resources_menu)
        self.create_button("images/Exit.png", "Exit", 1100, 380, self.root.quit)

    def create_button(self, image_path, text, x, y, command=None):
        try:
            img = Image.open(image_path).resize((220, 220), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            photo = None

        btn_img = Button(self.bg_label, image=photo, bd=0, cursor="hand2", command=command)
        btn_img.image = photo 
        btn_img.place(x=x, y=y, width=220, height=220)

        btn_text = Button(self.bg_label, text=text, bd=0, cursor="hand2",
                          font=("times new roman", 15, "bold"), bg="darkblue", fg="white", command=command)
        btn_text.place(x=x, y=y + 200 + 20, width=220, height=40)

    # ================== Button Functions ==================
    def students_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)
    
    def face_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)
    
    def open_material_window(self):
        self.new_window = Toplevel(self.root)
        self.app = MaterialWindow(self.new_window)
        
    def open_converter_tools(self):
        self.new_window = Toplevel(self.root)
        self.app = ConverterTools(self.new_window)

    def video_call(self):
        url = "http://localhost:8000"
        webbrowser.open(url)
        
    def open_assistant(self):
        self.new_window = Toplevel(self.root)
        self.app = Assistant(self.new_window)

    def attendance_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def open_chat_room(self):
        self.new_window = Toplevel(self.root)
        self.app = ChatClientWindow(self.new_window)

    def open_resources_menu(self):
        menu_win = Toplevel(self.root)
        menu_win.title("Resources")
        menu_win.geometry("300x200")
        menu_win.resizable(False, False)
        Label(menu_win, text="Select Resource", font=("times new roman", 18, "bold")).pack(pady=20)
        Button(menu_win, text="Material", font=("times new roman", 15), width=15, command=lambda: [menu_win.destroy(), self.open_material_window()]).pack(pady=10)
        Button(menu_win, text="Tools", font=("times new roman", 15), width=15, command=lambda: [menu_win.destroy(), self.open_converter_tools()]).pack(pady=10)

# ================== Main Function ==================
if __name__ == "__main__":
    root = Tk()
    app = FaceRecognitionSystem(root)
    root.mainloop()
