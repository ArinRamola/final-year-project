from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import mysql.connector
import subprocess
import os

class Signup_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Signup Form")
        self.root.geometry("1530x800+0+0")
        self.root.resizable(False, False)

        try:
            image_path = r"C:\Users\acer\Desktop\Project\images\login_background.jpg"
            bg_img = Image.open(image_path)
            bg_img = bg_img.resize((1530, 800), Image.Resampling.LANCZOS)
            self.bg = ImageTk.PhotoImage(bg_img)
            bg_label = Label(self.root, image=self.bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.root.configure(bg="#2c3e50")

        signup_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        frame_width = 450
        frame_height = 600
        center_x = (1530 - frame_width) // 2
        center_y = (800 - frame_height) // 2

        signup_frame.place(x=center_x, y=center_y, width=frame_width, height=frame_height)

        title = Label(signup_frame, text="SIGNUP", font=("Helvetica", 24, "bold"), bg="white", fg="#2c3e50")
        title.pack(pady=20)

        name_label = Label(signup_frame, text="Full Name", font=("Helvetica", 12), bg="white", anchor="w")
        name_label.place(x=30, y=70)
        self.name_entry = Entry(signup_frame, font=("Helvetica", 12), bg="#ecf0f1", relief=FLAT)
        self.name_entry.place(x=30, y=95, width=380, height=30)

        username_label = Label(signup_frame, text="Username", font=("Helvetica", 12), bg="white", anchor="w")
        username_label.place(x=30, y=135)
        self.username_entry = Entry(signup_frame, font=("Helvetica", 12), bg="#ecf0f1", relief=FLAT)
        self.username_entry.place(x=30, y=160, width=380, height=30)

        email_label = Label(signup_frame, text="Email", font=("Helvetica", 12), bg="white", anchor="w")
        email_label.place(x=30, y=200)
        self.email_entry = Entry(signup_frame, font=("Helvetica", 12), bg="#ecf0f1", relief=FLAT)
        self.email_entry.place(x=30, y=225, width=380, height=30)

        phone_label = Label(signup_frame, text="Phone Number", font=("Helvetica", 12), bg="white", anchor="w")
        phone_label.place(x=30, y=265)
        self.phone_entry = Entry(signup_frame, font=("Helvetica", 12), bg="#ecf0f1", relief=FLAT)
        self.phone_entry.place(x=30, y=290, width=380, height=30)

        password_label = Label(signup_frame, text="Password (min 8 characters)", font=("Helvetica", 12), bg="white", anchor="w")
        password_label.place(x=30, y=330)
        self.password_entry = Entry(signup_frame, font=("Helvetica", 12), bg="#ecf0f1", relief=FLAT, show="•")
        self.password_entry.place(x=30, y=355, width=380, height=30)

        confirm_label = Label(signup_frame, text="Confirm Password", font=("Helvetica", 12), bg="white", anchor="w")
        confirm_label.place(x=30, y=395)
        self.confirm_entry = Entry(signup_frame, font=("Helvetica", 12), bg="#ecf0f1", relief=FLAT, show="•")
        self.confirm_entry.place(x=30, y=420, width=380, height=30)

        self.show_password_var = IntVar()
        show_password_cb = Checkbutton(signup_frame, text="Show Password", variable=self.show_password_var,
                                       bg="white", font=("Helvetica", 10), command=self.toggle_password)
        show_password_cb.place(x=30, y=455)

        self.terms_var = IntVar()
        terms_cb = Checkbutton(signup_frame, text="I agree to the Terms and Conditions", 
                               variable=self.terms_var, bg="white", font=("Helvetica", 10))
        terms_cb.place(x=30, y=485)

        signup_btn = Button(signup_frame, text="Signup", font=("Helvetica", 13, "bold"), bg="#2ecc71", fg="white",
                            activebackground="#27ae60", activeforeground="white", command=self.signup)
        signup_btn.place(x=30, y=520, width=180, height=40)

        clear_btn = Button(signup_frame, text="Clear", font=("Helvetica", 13, "bold"), bg="#e74c3c", fg="white",
                           activebackground="#c0392b", activeforeground="white", command=self.clear_fields)
        clear_btn.place(x=230, y=520, width=180, height=40)

        signup_btn.bind("<Enter>", lambda e: signup_btn.config(bg="#27ae60"))
        signup_btn.bind("<Leave>", lambda e: signup_btn.config(bg="#2ecc71"))
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#c0392b"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg="#e74c3c"))

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
            self.confirm_entry.config(show="")
        else:
            self.password_entry.config(show="•")
            self.confirm_entry.config(show="•")

    def clear_fields(self):
        self.name_entry.delete(0, END)
        self.username_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.confirm_entry.delete(0, END)

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10

    def signup(self):
        full_name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()

        if not all([full_name, username, email, password, confirm_password]):
            messagebox.showerror("Error", "All fields except phone are required!")
            return

        if not self.terms_var.get():
            messagebox.showerror("Error", "You must agree to the Terms and Conditions")
            return

        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address!")
            return

        if phone and not self.validate_phone(phone):
            messagebox.showerror("Error", "Phone number must be 10 digits!")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Adiarinkadaddy@22041426",
                database="security"
            )
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO log (username, password, fullname, email, phone)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (username, password, full_name, email, phone)

            cursor.execute(insert_query, values)
            connection.commit()

            messagebox.showinfo("Success", f"Account created successfully for {full_name}!")

            self.clear_fields()
            self.open_login_window()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def open_login_window(self):
        self.root.quit()
        try:
            subprocess.Popen([self.get_venv_python_path(), "login.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open login.py: {e}")

    def get_venv_python_path(self):
        return os.path.join(os.getcwd(), ".venv", "Scripts", "python")

if __name__ == "__main__":
    root = Tk()
    app = Signup_Window(root)
    root.mainloop()
