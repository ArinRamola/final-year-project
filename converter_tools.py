# converter_tools.py
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from docx2pdf import convert as docx_to_pdf
from pdf2docx import Converter
from PIL import Image
import os

class ConverterTools:
    def __init__(self, root):
        self.root = root
        self.root.title("Converters - Word/PDF/Image Tools")
        self.root.geometry("800x500+350+150")
        self.root.config(bg="white")

        # Title
        title = Label(self.root, text="Converters - Word ↔ PDF & Image Resizer", font=("Arial", 20, "bold"), bg="purple", fg="white")
        title.pack(side=TOP, fill=X)

        # Buttons
        word_to_pdf_btn = Button(self.root, text="Word to PDF", command=self.word_to_pdf, width=30, height=2, bg="green", fg="white")
        word_to_pdf_btn.place(x=100, y=100)

        pdf_to_word_btn = Button(self.root, text="PDF to Word", command=self.pdf_to_word, width=30, height=2, bg="blue", fg="white")
        pdf_to_word_btn.place(x=400, y=100)

        resize_image_btn = Button(self.root, text="Resize Image", command=self.resize_image, width=30, height=2, bg="orange", fg="white")
        resize_image_btn.place(x=250, y=250)

    def word_to_pdf(self):
        file_path = filedialog.askopenfilename(title="Select Word File", filetypes=[("Word Files", "*.docx")])
        if file_path:
            output_folder = filedialog.askdirectory(title="Select Output Folder")
            try:
                docx_to_pdf(file_path, output_folder)
                messagebox.showinfo("Success", "Word file converted to PDF successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Conversion Failed!\n{str(e)}")

    def pdf_to_word(self):
        file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            output_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Files", "*.docx")])
            try:
                cv = Converter(file_path)
                cv.convert(output_path)
                cv.close()
                messagebox.showinfo("Success", "PDF converted to Word successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Conversion Failed!\n{str(e)}")

    def resize_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            width = simpledialog.askinteger("Input", "Enter new width:", minvalue=100, maxvalue=5000)
            height = simpledialog.askinteger("Input", "Enter new height:", minvalue=100, maxvalue=5000)
            if width and height:
                try:
                    img = Image.open(file_path)
                    img_resized = img.resize((width, height))
                    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG Files", "*.jpg"), ("PNG Files", "*.png")])
                    if save_path:
                        img_resized.save(save_path)
                        messagebox.showinfo("Success", "Image resized and saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Image Resizing Failed!\n{str(e)}")
