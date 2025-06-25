from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
from tkcalendar import DateEntry

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x600+200+100")
        self.root.title("Attendance Management")
        self.root.configure(bg="white")
        self.root.focus_force()

        self.var_start_date = StringVar()
        self.var_end_date = StringVar()

        title = Label(self.root, text="Attendance Records",
                      font=("Helvetica", 20, "bold"), bg="#002B53", fg="white")
        title.pack(side=TOP, fill=X)

        filter_frame = LabelFrame(self.root, text="Filter Records",
                                 font=("Helvetica", 12), bg="white")
        filter_frame.pack(side=TOP, padx=10, pady=10, fill=X)

        Label(filter_frame, text="Start Date:", bg="white").grid(row=0, column=0, padx=5)
        self.start_date = DateEntry(filter_frame, date_pattern="dd/mm/yyyy",
                                    textvariable=self.var_start_date)
        self.start_date.grid(row=0, column=1, padx=5)

        Label(filter_frame, text="End Date:", bg="white").grid(row=0, column=2, padx=5)
        self.end_date = DateEntry(filter_frame, date_pattern="dd/mm/yyyy",
                                  textvariable=self.var_end_date)
        self.end_date.grid(row=0, column=3, padx=5)

        btn_filter = Button(filter_frame, text="Apply Filter", command=self.load_data,
                            bg="#002B53", fg="white", bd=0)
        btn_filter.grid(row=0, column=4, padx=10)

        btn_export = Button(filter_frame, text="Export CSV", command=self.export_csv,
                            bg="green", fg="white", bd=0)
        btn_export.grid(row=0, column=5, padx=10)

        tree_frame = Frame(self.root, bg="white")
        tree_frame.pack(pady=10, fill=BOTH, expand=True)

        scroll_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tree_frame, orient=VERTICAL)

        self.attendance_table = ttk.Treeview(tree_frame, columns=("name", "date", "time", "status"),
                                             yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        self.attendance_table.heading("name", text="Name")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("time", text="Time")
        self.attendance_table.heading("status", text="Status")

        self.attendance_table["show"] = "headings"
        self.attendance_table.pack(fill=BOTH, expand=True)

        self.attendance_table.column("name", width=200, anchor=CENTER)
        self.attendance_table.column("date", width=150, anchor=CENTER)
        self.attendance_table.column("time", width=150, anchor=CENTER)
        self.attendance_table.column("status", width=100, anchor=CENTER)

        self.load_data()

    def load_data(self):
        try:
            records = []
            with open("Attendance.csv", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) == 8:
                        name = parts[2]
                        time = parts[5]
                        date = parts[6]
                        status = parts[7]
                    elif len(parts) == 7:
                        name = parts[2]
                        time = parts[4]
                        date = parts[5]
                        status = parts[6]
                    else:
                        continue
                    records.append([name, date, time, status])

            df = pd.DataFrame(records, columns=["Name", "Date", "Time", "Status"])
            df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

            if self.var_start_date.get() and self.var_end_date.get():
                start_date = datetime.strptime(self.var_start_date.get(), "%d/%m/%Y")
                end_date = datetime.strptime(self.var_end_date.get(), "%d/%m/%Y")
                df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

            for item in self.attendance_table.get_children():
                self.attendance_table.delete(item)

            for _, row in df.iterrows():
                date_str = ""
                if pd.notnull(row["Date"]):
                    date_str = row["Date"].strftime("%d/%m/%Y")
                self.attendance_table.insert("", END, values=(
                    row["Name"],
                    date_str,
                    row["Time"],
                    row["Status"]
                ))

        except FileNotFoundError:
            messagebox.showerror("Error", "Attendance file not found!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}", parent=self.root)

    def export_csv(self):
        try:
            data = []
            for item in self.attendance_table.get_children():
                values = self.attendance_table.item(item)['values']
                data.append({
                    "Name": values[0],
                    "Date": values[1],
                    "Time": values[2],
                    "Status": values[3]
                })

            if data:
                df = pd.DataFrame(data)
                df.to_csv("Filtered_Attendance.csv", index=False)
                messagebox.showinfo("Success", "Data exported to Filtered_Attendance.csv", parent=self.root)
            else:
                messagebox.showwarning("Warning", "No data to export", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
