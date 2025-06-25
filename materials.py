from tkinter import *
from tkinter import filedialog, messagebox
import os
import shutil
import subprocess
import sys

class MaterialWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Material & Previous Year Papers")
        self.root.geometry("800x600+350+100")
        self.root.config(bg="white")
        self.root.lift()

        self.materials_dir = os.path.abspath('Materials')
        self.class_material_dir = os.path.join(self.materials_dir, 'ClassMaterial')
        self.previous_papers_dir = os.path.join(self.materials_dir, 'PreviousPapers')
        os.makedirs(self.class_material_dir, exist_ok=True)
        os.makedirs(self.previous_papers_dir, exist_ok=True)

        title = Label(self.root, text="Study Materials and Exam Papers", font=("Arial", 20, "bold"), bg="navy", fg="white")
        title.place(x=0, y=0, width=800, height=60)

        Button(self.root, text="Upload Class Material", command=self.upload_class_material,
               width=30, height=2, bg="green", fg="white").place(x=100, y=80)
        Button(self.root, text="View Class Materials", command=self.view_class_material,
               width=30, height=2, bg="blue", fg="white").place(x=400, y=80)

        Button(self.root, text="Upload Previous Year Paper", command=self.upload_exam_paper,
               width=30, height=2, bg="green", fg="white").place(x=100, y=180)
        Button(self.root, text="View Previous Year Papers", command=self.view_exam_papers,
               width=30, height=2, bg="blue", fg="white").place(x=400, y=180)

        self.root.update()

    def upload_class_material(self):
        file_path = filedialog.askopenfilename(title="Select Class Material", filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")])
        if file_path:
            try:
                dest_path = os.path.join(self.class_material_dir, os.path.basename(file_path))
                shutil.copy(file_path, dest_path)
                messagebox.showinfo("Success", "Class Material Uploaded Successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Upload Failed!\n{str(e)}")

    def upload_exam_paper(self):
        file_path = filedialog.askopenfilename(title="Select Previous Year Paper", filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")])
        if file_path:
            try:
                dest_path = os.path.join(self.previous_papers_dir, os.path.basename(file_path))
                shutil.copy(file_path, dest_path)
                messagebox.showinfo("Success", "Exam Paper Uploaded Successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Upload Failed!\n{str(e)}")

    def view_class_material(self):
        self.view_files(self.class_material_dir)

    def view_exam_papers(self):
        self.view_files(self.previous_papers_dir)

    def view_files(self, folder_path):
        view_window = Toplevel(self.root)
        view_window.title("Files List")
        view_window.geometry("500x450+400+150")
        view_window.config(bg="white")

        try:
            files = os.listdir(folder_path)
        except FileNotFoundError:
            messagebox.showerror("Error", "Directory not found!")
            return

        listbox = Listbox(view_window, font=("Arial", 12))
        listbox.pack(fill=BOTH, expand=True, padx=10, pady=10)

        if not files:
            listbox.insert(END, "No files found in this directory")
        else:
            for file in sorted(files):
                listbox.insert(END, file)

        def open_selected_file():
            selected = listbox.curselection()
            if selected:
                file_name = listbox.get(selected[0]).strip()
                full_path = os.path.join(folder_path, file_name)

                if not os.path.exists(full_path):
                    messagebox.showerror("Error", "File does not exist!")
                    return

                try:
                    if os.name == 'nt':
                        os.startfile(full_path)
                    else:
                        subprocess.run(['open', full_path] if sys.platform == 'darwin' else ['xdg-open', full_path])
                except Exception as e:
                    messagebox.showerror("Error", f"Cannot open file:\n{str(e)}\nPath: {full_path}")

        def delete_selected_file():
            selected = listbox.curselection()
            if selected:
                file_name = listbox.get(selected[0]).strip()
                full_path = os.path.join(folder_path, file_name)

                if not os.path.exists(full_path):
                    messagebox.showerror("Error", "File does not exist!")
                    return

                confirm = messagebox.askyesno("Delete Confirmation", f"Delete this file permanently?\n{file_name}")
                if confirm:
                    try:
                        os.remove(full_path)
                        listbox.delete(selected[0])
                        messagebox.showinfo("Success", "File deleted successfully!")
                    except Exception as e:
                        messagebox.showerror("Error", f"Delete failed:\n{str(e)}")

        button_frame = Frame(view_window, bg="white")
        button_frame.pack(fill=X, pady=10)

        open_button = Button(button_frame, text="Open File", command=open_selected_file, width=15, height=1, bg="green", fg="white")
        open_button.pack(side=LEFT, padx=20)

        delete_button = Button(button_frame, text="Delete File", command=delete_selected_file, width=15, height=1, bg="red", fg="white")
        delete_button.pack(side=RIGHT, padx=20)
