from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
import threading
import google.generativeai as genai
import os

# Recommended: Set your API key securely
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyAaxeRhne_YryZq1nf1YdjUOtjyKertAEM"))


class Assistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini AI Assistant")
        self.root.geometry("700x700")
        self.root.configure(bg="#f2f2f2")

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TEntry", font=("Segoe UI", 11))
        style.configure("TLabel", font=("Segoe UI", 12))
        
        # Title Bar
        title_bar = Frame(self.root, bg="#1E90FF", height=50)
        title_bar.pack(fill=X)

        title_label = Label(title_bar, text="🤖 AI Query Resolver", font=("Segoe UI", 16, "bold"), fg="white", bg="#1E90FF", pady=10)
        title_label.pack(side=LEFT, padx=20)

        # Chat Display Area
        self.chat_display = scrolledtext.ScrolledText(self.root, font=("Consolas", 12), wrap=WORD, bg="white", relief=FLAT)
        self.chat_display.pack(padx=20, pady=(20, 10), fill=BOTH, expand=True)
        self.chat_display.config(state=DISABLED)

        # Input Frame
        input_frame = Frame(self.root, bg="#f2f2f2")
        input_frame.pack(fill=X, padx=20, pady=(0, 20))

        self.user_input = ttk.Entry(input_frame)
        self.user_input.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))

        send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_button.pack(side=RIGHT)

        # Bind Enter key to send message
        self.root.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        user_msg = self.user_input.get().strip()
        if user_msg:
            self.display_message("You", user_msg)
            self.user_input.delete(0, END)
            threading.Thread(target=self.get_response, args=(user_msg,), daemon=True).start()

    def display_message(self, sender, message):
        self.chat_display.config(state=NORMAL)
        self.chat_display.insert(END, f"{sender}: {message}\n\n")
        self.chat_display.config(state=DISABLED)
        self.chat_display.see(END)

    def get_response(self, user_msg):
        try:
            response = self.get_gemini_response(user_msg)
        except Exception as e:
            response = f"Error: {e}"
        self.display_message("Gemini", response)

    def get_gemini_response(self, prompt):
        try:
            model = genai.GenerativeModel('models/gemini-2.0-flash')
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Failed to connect to Gemini: {e}"
