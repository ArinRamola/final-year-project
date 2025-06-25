import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234
HANDSHAKE = b'CHATAPPv1\n'

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

class ChatClientWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Messenger Client")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=4)
        self.root.grid_rowconfigure(2, weight=1)

        top_frame = tk.Frame(self.root, width=600, height=100, bg=DARK_GREY)
        top_frame.grid(row=0, column=0, sticky=tk.NSEW)

        middle_frame = tk.Frame(self.root, width=600, height=400, bg=MEDIUM_GREY)
        middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

        bottom_frame = tk.Frame(self.root, width=600, height=100, bg=DARK_GREY)
        bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

        username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
        username_label.pack(side=tk.LEFT, padx=10)

        self.username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
        self.username_textbox.pack(side=tk.LEFT)

        self.username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.connect)
        self.username_button.pack(side=tk.LEFT, padx=15)

        self.message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
        self.message_textbox.pack(side=tk.LEFT, padx=10)

        self.message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.send_message)
        self.message_button.pack(side=tk.LEFT, padx=10)

        self.message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
        self.message_box.config(state=tk.DISABLED)
        self.message_box.pack(side=tk.TOP)

    def add_message(self, message):
        self.message_box.config(state=tk.NORMAL)
        self.message_box.insert(tk.END, message + '\n')
        self.message_box.config(state=tk.DISABLED)
        self.message_box.see(tk.END)

    def connect(self):
        try:
            self.client.connect((HOST, PORT))
            self.add_message("[SERVER] Connected to server")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server {HOST}:{PORT}\n{e}")
            return

        username = self.username_textbox.get().strip()
        if username:
            try:
                self.client.sendall(HANDSHAKE)
                self.client.sendall(username.encode('utf-8'))
            except Exception as e:
                messagebox.showerror("Send Error", f"Failed to send handshake/username: {e}")
                return
        else:
            messagebox.showerror("Invalid username", "Username cannot be empty")
            return

        threading.Thread(target=self.listen_for_messages_from_server, daemon=True).start()
        self.username_textbox.config(state=tk.DISABLED)
        self.username_button.config(state=tk.DISABLED)

    def send_message(self):
        message = self.message_textbox.get().strip()
        if message:
            try:
                self.client.sendall(message.encode('utf-8'))
                self.message_textbox.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Send Error", f"Failed to send message: {e}")
        else:
            messagebox.showerror("Empty message", "Message cannot be empty")

    def listen_for_messages_from_server(self):
        while True:
            try:
                message = self.client.recv(2048).decode('utf-8')
                if message:
                    if '~' in message:
                        username, content = message.split('~', 1)
                        self.add_message(f"[{username}] {content}")
                    else:
                        self.add_message(message)
                else:
                    self.add_message("[SERVER] Connection closed by server.")
                    break
            except Exception as e:
                self.add_message(f"[ERROR] {e}")
                break
