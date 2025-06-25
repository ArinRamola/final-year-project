from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os
import mysql.connector

class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Form")
        self.root.geometry("1530x800+0+0")
        self.root.resizable(False, False)

        try:
            bg_img = Image.open("C:/Users/acer/Desktop/Project/images/login_background.jpg")
            bg_img = bg_img.resize((1530, 800), Image.Resampling.LANCZOS)
            self.bg = ImageTk.PhotoImage(bg_img)
            bg_label = Label(self.root, image=self.bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            self.root.configure(bg="#2c3e50")

        login_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        frame_width = 400
        frame_height = 400
        center_x = (1530 - frame_width) // 2
        center_y = (800 - frame_height) // 2
        login_frame.place(x=center_x, y=center_y, width=frame_width, height=frame_height)

        title = Label(login_frame, text="LOGIN", font=("Helvetica", 24, "bold"), bg="white", fg="#2c3e50")
        title.pack(pady=20)

        username_label = Label(login_frame, text="Username", font=("Helvetica", 14), bg="white", anchor="w")
        username_label.place(x=30, y=80)
        self.username_entry = Entry(login_frame, font=("Helvetica", 13), bg="#ecf0f1", relief=FLAT)
        self.username_entry.place(x=30, y=110, width=340, height=30)

        password_label = Label(login_frame, text="Password", font=("Helvetica", 14), bg="white", anchor="w")
        password_label.place(x=30, y=150)
        self.password_entry = Entry(login_frame, font=("Helvetica", 13), bg="#ecf0f1", relief=FLAT, show="*")
        self.password_entry.place(x=30, y=180, width=340, height=30)

        self.show_password_var = IntVar()
        show_password_cb = Checkbutton(login_frame, text="Show Password", variable=self.show_password_var,
                                       bg="white", font=("Helvetica", 10), command=self.toggle_password)
        show_password_cb.place(x=30, y=220)

        self.login_btn = Button(login_frame, text="Login", font=("Helvetica", 13, "bold"), bg="#2ecc71", fg="white",
                                activebackground="#27ae60", activeforeground="white", command=self.login, cursor="hand2")
        self.login_btn.place(x=30, y=260, width=150, height=40)

        self.clear_btn = Button(login_frame, text="Clear", font=("Helvetica", 13, "bold"), bg="#e74c3c", fg="white",
                                activebackground="#c0392b", activeforeground="white", command=self.clear_fields, cursor="hand2")
        self.clear_btn.place(x=220, y=260, width=150, height=40)

        signup_btn = Button(login_frame, text="Sign Up", font=("Helvetica", 12, "underline"), bg="white", fg="#2980b9",
                            bd=0, activebackground="white", activeforeground="#3498db", command=self.open_signup, cursor="hand2")
        signup_btn.place(x=150, y=320)

        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#27ae60"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg="#2ecc71"))
        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg="#c0392b"))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg="#e74c3c"))

    def toggle_password(self):
        self.password_entry.config(show="" if self.show_password_var.get() else "*")

    def clear_fields(self):
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required!")
        elif self.validate_login(username, password):
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.open_main()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def validate_login(self, username, password):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adiarinkadaddy@22041426",
                database="security"
            )
            cursor = connection.cursor()
            query = "SELECT * FROM log WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            if user:
                return True
            else:
                return False
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def open_main(self):
        try:
            subprocess.Popen([self.get_venv_python_path(), "main.py"])
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open main.py: {e}")

    def open_signup(self):
        self.root.destroy()
        try:
            subprocess.Popen([self.get_venv_python_path(), "sign_up.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open sign_up.py: {e}")

    def get_venv_python_path(self):
        return os.path.join(os.getcwd(), ".venv", "Scripts", "python")

if __name__ == "__main__":
    root = Tk()
    app = Login_Window(root)
    root.mainloop()
