from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import mysql.connector
import cv2
from train import Train


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")  # Set a fixed window size
        self.root.title("Student Details")
        self.root.resizable(False, False)  # Disable resizing 

        #=============================variables==========================
        self.var_dept=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_semester=StringVar()
        self.var_std_id=StringVar()
        self.var_std_name=StringVar()
        self.var_div=StringVar()
        self.var_roll=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        self.var_teacher=StringVar()

        # Helper function to load images safely
        def load_image(path, size):
            try:
                img = Image.open(path)
                img = img.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                return None

        # Image Paths
        image_folder = os.path.join(os.getcwd(), "images") 
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
        Label(self.root, image=self.photoimg4).place(x=970, y=0, width=560, height=130) # Change this accordingly

        

        # Background Image
        self.photoimg_bg = load_image(os.path.join(image_folder, "image4.png"), (1530, 710))
        if self.photoimg_bg:
            self.bg_label = Label(self.root, image=self.photoimg_bg)
            self.bg_label.place(x=0, y=130, width=1530, height=710)

        # Title Label
        title_label = Label(self.bg_label, text="STUDENT PORTAL",
                            font=("times new roman", 35, "bold"), bg="white", fg="darkgreen")
        title_label.place(x=0, y=0, width=1530, height=50)

        # Main Frame
        main_frame = Frame(self.bg_label, bd=2, bg="white", relief=RIDGE)
        main_frame.place(x=10, y=55, width=1500, height=600)

        # Left label frame
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details",
                                font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=10, width=730, height=580)

        # Load left image properly
        left_img_path = os.path.join(image_folder, "image2.jpeg")
        self.photoimg_left = load_image(left_img_path, (720, 130))
        if self.photoimg_left:
            f_lbl = Label(Left_frame, image=self.photoimg_left)
            f_lbl.place(x=5, y=0, width=720, height=150)
        
        #Current course
        current_course_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Course Information",
                                font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=135, width=720, height=150)
        
        #Department
        dept_label=Label(current_course_frame, text="Department",font=("times new roman", 12, "bold"),bg="white")
        dept_label.grid(row=0,column=0,padx=10,sticky=W)

        dept_combo=ttk.Combobox(current_course_frame,textvariable=self.var_dept,font=("times new roman", 12, "bold"),width=17,state="readonly")
        dept_combo["values"]=("Select Department","Computer","IT")
        dept_combo.current(0)
        dept_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)
        
        #Course
        course_label=Label(current_course_frame, text="Course",font=("times new roman", 12, "bold"),bg="white")
        course_label.grid(row=0,column=2,padx=10,sticky=W)

        course_combo=ttk.Combobox(current_course_frame,textvariable=self.var_course,font=("times new roman", 12, "bold"),width=17,state="readonly")
        course_combo["values"]=("Select Course","COA","DSA","DBMS","CG")
        course_combo.current(0)
        course_combo.grid(row=0,column=3,padx=2,pady=10,sticky=W)

        #Year
        year_label=Label(current_course_frame, text="Year",font=("times new roman", 12, "bold"),bg="white")
        year_label.grid(row=1,column=0,padx=10,sticky=W)

        year_combo=ttk.Combobox(current_course_frame,textvariable=self.var_year,font=("times new roman", 12, "bold"),width=17,state="readonly")
        year_combo["values"]=("Select Year","2020-21","2021-22","2022-23","2023-24","2024-25")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)

        #Semester
        semester_label=Label(current_course_frame, text="Semester",font=("times new roman", 12, "bold"),bg="white")
        semester_label.grid(row=1,column=2,padx=10,sticky=W)

        semester_combo=ttk.Combobox(current_course_frame,textvariable=self.var_semester,font=("times new roman", 12, "bold"),width=17,state="readonly")
        semester_combo["values"]=("Select Semester","Semester-1","Semester-2")
        semester_combo.current(0)
        semester_combo.grid(row=1,column=3,padx=2,pady=10,sticky=W)

        #Class Student information
        class_student_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Student Information",
                                font=("times new roman", 12, "bold"))
        class_student_frame.place(x=5, y=250, width=720, height=300)
        
        #student ID
        studentId_label=Label(class_student_frame, text="StudentId:",font=("times new roman", 12, "bold"),bg="white")
        studentId_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)

        studentId_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_std_id,font=("times new roman", 12, "bold"))
        studentId_entry.grid(row=0,column=1,padx=10,pady=5,sticky=W)

        #student name
        studentName_label=Label(class_student_frame, text="Student Name:",font=("times new roman", 12, "bold"),bg="white")
        studentName_label.grid(row=0,column=2,padx=10,pady=5,sticky=W)

        studentName_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_std_name,font=("times new roman", 12, "bold"))
        studentName_entry.grid(row=0,column=3,padx=10,pady=5,sticky=W)

        #class division
        class_div_label=Label(class_student_frame, text="Class Division:",font=("times new roman", 12, "bold"),bg="white")
        class_div_label.grid(row=1,column=0,padx=10,pady=5,sticky=W)

        class_div_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_div,font=("times new roman", 12, "bold"))
        class_div_entry.grid(row=1,column=1,padx=10,pady=5,sticky=W)
        
        class_div_combo=ttk.Combobox(class_student_frame,textvariable=self.var_div,font=("times new roman", 12, "bold"),width=18,state="readonly")
        class_div_combo["values"]=("A","B","C")
        class_div_combo.current(0)
        class_div_combo.grid(row=1,column=1,padx=10,pady=5,sticky=W)

        #Roll no
        roll_no_label=Label(class_student_frame, text="Roll no:",font=("times new roman", 12, "bold"),bg="white")
        roll_no_label.grid(row=1,column=2,padx=10,pady=5,sticky=W)

        roll_no_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_roll,font=("times new roman", 12, "bold"))
        roll_no_entry.grid(row=1,column=3,padx=10,pady=5,sticky=W)

        #Gender
        gender_label=Label(class_student_frame, text="Gender:",font=("times new roman", 12, "bold"),bg="white")
        gender_label.grid(row=2,column=0,padx=10,pady=5,sticky=W)
        
        gender_combo=ttk.Combobox(class_student_frame,textvariable=self.var_gender,font=("times new roman", 12, "bold"),width=18,state="readonly")
        gender_combo["values"]=("Male","Female","Other")
        gender_combo.current(0)
        gender_combo.grid(row=2,column=1,padx=10,pady=5,sticky=W)

        #DOB
        dob_label=Label(class_student_frame, text="DOB:",font=("times new roman", 12, "bold"),bg="white")
        dob_label.grid(row=2,column=2,padx=10,pady=5,sticky=W)

        dob_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_dob,font=("times new roman", 12, "bold"))
        dob_entry.grid(row=2,column=3,padx=10,pady=5,sticky=W)

        #Email
        email_label=Label(class_student_frame, text="Email:",font=("times new roman", 12, "bold"),bg="white")
        email_label.grid(row=3,column=0,padx=10,pady=5,sticky=W)

        email_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_email,font=("times new roman", 12, "bold"))
        email_entry.grid(row=3,column=1,padx=10,pady=5,sticky=W)

        #Phone no
        phone_label=Label(class_student_frame, text="Phone no:",font=("times new roman", 12, "bold"),bg="white")
        phone_label.grid(row=3,column=2,padx=10,pady=5,sticky=W)

        phone_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_phone,font=("times new roman", 12, "bold"))
        phone_entry.grid(row=3,column=3,padx=10,pady=5,sticky=W)

        #Address
        address_label=Label(class_student_frame, text="Address:",font=("times new roman", 12, "bold"),bg="white")
        address_label.grid(row=4,column=0,padx=10,pady=5,sticky=W)

        address_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_address,font=("times new roman", 12, "bold"))
        address_entry.grid(row=4,column=1,padx=10,pady=5,sticky=W)

        #Teacher name
        teacher_label=Label(class_student_frame, text="Teacher Name:",font=("times new roman", 12, "bold"),bg="white")
        teacher_label.grid(row=4,column=2,padx=10,pady=5,sticky=W)

        teacher_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_teacher,font=("times new roman", 12, "bold"))
        teacher_entry.grid(row=4,column=3,padx=10,pady=5,sticky=W)

        #radio buttons
        self.var_radio1 = StringVar()
        radiobtn1 = ttk.Radiobutton(class_student_frame, text="Take Photo Sample", variable=self.var_radio1, value="YES")
        radiobtn1.grid(row=6, column=0)

        self.var_radio2 = StringVar()
        radiobtn2 = ttk.Radiobutton(class_student_frame, text="No photo sample", variable=self.var_radio2, value="NO")
        radiobtn2.grid(row=6, column=1)

        #buttons frame
        btn_frame=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=200,width=725,height=35)

        save_btn=Button(btn_frame,text="Save",command=self.add_data,width=19,font=("times new roman", 12, "bold"),bg="blue",fg="white")
        save_btn.grid(row=0,column=0)

        update_btn=Button(btn_frame,text="Update",command=self.update_data,width=19,font=("times new roman", 12, "bold"),bg="blue",fg="white")
        update_btn.grid(row=0,column=1)

        delete_btn=Button(btn_frame,text="Delete",command=self.delete_data,width=19,font=("times new roman", 12, "bold"),bg="blue",fg="white")
        delete_btn.grid(row=0,column=2)

        reset_btn=Button(btn_frame,text="Reset",command=self.reset_data,width=19,font=("times new roman", 12, "bold"),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3)

        btn_frame1=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame1.place(x=0,y=235,width=725,height=35)

        take_photo_btn=Button(btn_frame1,text="Take Photo Sample",command=self.generate_dataset,width=40,font=("times new roman", 12, "bold"),bg="blue",fg="white")
        take_photo_btn.grid(row=0,column=0)

        train_photo_btn = Button(btn_frame1, text="Train Photo", command=self.train_data, width=40, font=("times new roman", 12, "bold"),
                                bg="blue", fg="white")
        train_photo_btn.grid(row=0, column=1)


        # Right label frame
        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=750, y=10, width=720, height=580)

        self.photoimg_right = load_image(os.path.join(image_folder, "image2.jpeg"), (720, 130))
        if self.photoimg_right:
            Label(Right_frame, image=self.photoimg_right).place(x=5, y=0, width=720, height=130)


        # ========================Table Frame===========================
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=210, width=710, height=350)

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)
        
        self.student_table = ttk.Treeview(table_frame,columns=("dep", "course", "year", "sem", "id", "name", "div","roll","gender","dob","email", "phone", "address", "teacher", "photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep",text="Department")
        self.student_table.heading("course",text="Course")
        self.student_table.heading("year",text="Year")
        self.student_table.heading("sem",text="Semester")
        self.student_table.heading("id",text="StudentId")
        self.student_table.heading("name",text="Name")
        self.student_table.heading("div",text="Division")
        self.student_table.heading("roll",text="RollNo")
        self.student_table.heading("gender",text="Gender")
        self.student_table.heading("dob",text="DOB")
        self.student_table.heading("email",text="Email")
        self.student_table.heading("phone",text="Phone")
        self.student_table.heading("address",text="Address")
        self.student_table.heading("teacher",text="Teacher")
        self.student_table.heading("photo",text="PhotoSampleStatus")
        self.student_table["show"]="headings"

        self.student_table.column("dep",width=100)
        self.student_table.column("course",width=100)
        self.student_table.column("year",width=100)
        self.student_table.column("sem",width=100)
        self.student_table.column("id",width=100)
        self.student_table.column("name",width=100)
        self.student_table.column("div",width=100)
        self.student_table.column("roll",width=100)
        self.student_table.column("gender",width=100)
        self.student_table.column("dob",width=100)
        self.student_table.column("email",width=100)
        self.student_table.column("phone",width=100)
        self.student_table.column("address",width=100)
        self.student_table.column("teacher",width=100)
        self.student_table.column("photo",width=150)

        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()

    #==============================================function declaration======================================
    def add_data(self):
        if self.var_dept.get()=="Select  Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",username="root",password="Adiarinkadaddy@22041426",database="facial_recognition")
                my_cursor = conn.cursor()
                my_cursor.execute("INSERT INTO student VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                                                                                                                self.var_dept.get(),
                                                                                                                self.var_course.get(),
                                                                                                                self.var_year.get(),
                                                                                                                self.var_semester.get(),
                                                                                                                self.var_std_id.get(),
                                                                                                                self.var_std_name.get(),
                                                                                                                self.var_div.get(),
                                                                                                                self.var_roll.get(),
                                                                                                                self.var_gender.get(),
                                                                                                                self.var_dob.get(),
                                                                                                                self.var_email.get(),
                                                                                                                self.var_phone.get(),
                                                                                                                self.var_address.get(),
                                                                                                                self.var_teacher.get(),
                                                                                                                self.var_radio1.get()
                                                                                                                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Students detail has been added successfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to :{str(es)}",parent=self.root)
                
    #======================================================fetch data===============================================
    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="Adiarinkadaddy@22041426",database="facial_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from student")
        data = my_cursor.fetchall()
        
        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()
        
    #==========================================================get cursor==============================================
    def get_cursor(self,event=""):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]
        
        self.var_dept.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_semester.set(data[3]),
        self.var_std_id.set(data[4]),
        self.var_std_name.set(data[5]),
        self.var_div.set(data[6]),
        self.var_roll.set(data[7]),
        self.var_gender.set(data[8]),
        self.var_dob.set(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_teacher.set(data[13]),
        self.var_radio1.set(data[14])
        
        
    #=============================================================update function=============================================
    def update_data(self):
        if self.var_dept.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All Fields are required",parent=self.root)
            return
        
        
        try:
            Update = messagebox.askyesno("Update", "Do you want to update the data?", parent=self.root)
            if not Update:
                return
            
            conn = mysql.connector.connect(
              host="localhost",
              username="root",
              password="Adiarinkadaddy@22041426",
              database="facial_recognition"
            )
            my_cursor = conn.cursor()
            
            my_cursor.execute("""
            UPDATE student 
            SET Dept=%s, Course=%s, Year=%s, Semester=%s, Division=%s, 
                Roll=%s, Gender=%s, Dob=%s, Email=%s, Phone=%s, 
                Address=%s, Teacher=%s, PhotoSample=%s 
            WHERE Student_id=%s
            """, (
            self.var_dept.get(),
            self.var_course.get(),
            self.var_year.get(),
            self.var_semester.get(),
            self.var_div.get(),
            self.var_roll.get(),
            self.var_gender.get(),
            self.var_dob.get(),
            self.var_email.get(),
            self.var_phone.get(),
            self.var_address.get(),
            self.var_teacher.get(),
            self.var_radio1.get(),
            self.var_std_id.get()
            ))
            
            conn.commit()
            messagebox.showinfo("Success", "Student details updated successfully", parent=self.root)

            self.fetch_data()
            conn.close()
            
        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    #================================================delete function============================================
    
    def delete_data(self):
        if self.var_std_id.get()=="":
            messagebox.showerror("Error","Student id must be required",parent=self.root)
            return
        
        try:
                delete=messagebox.askyesno("Student Delete","Do you want to delete this student",parent=self.root)
                if not delete:
                    return
                    
                conn = mysql.connector.connect(
                       host="localhost",
                       username="root",
                       password="Adiarinkadaddy@22041426",
                       database="facial_recognition"
                    )
                my_cursor = conn.cursor()
                
                sql="delete from student where Student_id=%s"
                val=(self.var_std_id.get(),)
                my_cursor.execute(sql,val)
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Delete","Successfully delete student detail",parent=self.root)
                self.fetch_data()
                
        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
            
            
            
     #===========================================reset function=======================================
    def reset_data(self):
        self.var_dept.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("Select Division")
        self.var_roll.set("")
        self.var_gender.set("Male")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("")
        
    #======================================Generate data set ot take photo sample=====================
    def generate_dataset(self):
        if self.var_dept.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return
        else:
            try:
                id = int(self.var_std_id.get())

                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="Adiarinkadaddy@22041426",
                    database="facial_recognition"
                )
                my_cursor = conn.cursor()

                update_query = """
                    UPDATE student SET
                        Dept=%s, Course=%s, Year=%s, Semester=%s, Division=%s, 
                        Roll=%s, Gender=%s, Dob=%s, Email=%s, Phone=%s, 
                        Address=%s, Teacher=%s, PhotoSample=%s
                    WHERE Student_id=%s
                """
                data = (
                    self.var_dept.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio1.get(),
                    id
                )

                my_cursor.execute(update_query, data)
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                
                #========================================openCV==========================
                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                
                def face_cropped(img):
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        face_cropped = img[y:y+h, x:x+w]
                        return face_cropped

                # Check for existing images in 'data' folder
                existing_files = [f for f in os.listdir("data") if f.startswith(f"user.{id}.") and f.endswith(".jpg")]
                existing_ids = [int(f.split(".")[2]) for f in existing_files if f.split(".")[2].isdigit()]
                start_id = max(existing_ids, default=0)

                cap = cv2.VideoCapture(0)
                img_id = start_id

                while True:
                    ret, my_frame = cap.read()
                    face = face_cropped(my_frame)
                    if face is not None:
                        img_id += 1
                        face = cv2.resize(face, (450, 450))
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                        file_name_path = f"data/user.{id}.{img_id}.jpg"
                        cv2.imwrite(file_name_path, face)
                        cv2.putText(face, str(img_id), (50,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 2)   
                        cv2.imshow("Cropped Face", face)
                        
                    if cv2.waitKey(1) == 13 or (img_id - start_id) == 100:
                        break
                    
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result", "Generating Dataset Completed Successfully")  

            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
                
    #=======================================Train Photo Logic========================================
    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

                             
if __name__ == "__main__":
    root = Tk()
    app = Student(root)
    root.mainloop()


