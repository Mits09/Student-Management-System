import mysql.connector
from tkinter import *
from tkinter import messagebox
import sys


def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="W7301@jqir#",
            database="studentdb"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        sys.exit()


def register_user():
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if username and password and confirm_password:
        if password == confirm_password:
            conn = create_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                if cursor.fetchone():
                    messagebox.showerror("Registration Error", "Username already exists!")
                else:
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                    conn.commit()
                    messagebox.showinfo("Registration", "User registered successfully!")
                    register_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Password Error", "Passwords do not match!")
    else:
        messagebox.showerror("Input Error", "Please fill all fields")


def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if username and password:
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            if cursor.fetchone():
                messagebox.showinfo("Login", "Login successful!")
                login_window.destroy()
                open_dashboard()  
            else:
                messagebox.showerror("Login Error", "Invalid username or password!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Input Error", "Please enter both username and password")


def open_login_window():
    global login_window
    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x300")
    
    frame = Frame(login_window)
    frame.pack(pady=30, padx=30)

    Label(frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    global login_username_entry
    login_username_entry = Entry(frame)
    login_username_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(frame, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    global login_password_entry
    login_password_entry = Entry(frame, show="*")
    login_password_entry.grid(row=1, column=1, padx=10, pady=10)

    Button(frame, text="Login", command=login_user).grid(row=2, columnspan=2, pady=20)


def open_register_window():
    global register_window
    register_window = Toplevel(root)
    register_window.title("Register")
    register_window.geometry("300x400")
    
    frame = Frame(register_window)
    frame.pack(pady=30, padx=30)

    Label(frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    global username_entry
    username_entry = Entry(frame)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(frame, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    global password_entry
    password_entry = Entry(frame, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(frame, text="Confirm Password:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    global confirm_password_entry
    confirm_password_entry = Entry(frame, show="*")
    confirm_password_entry.grid(row=2, column=1, padx=10, pady=10)

    Button(frame, text="Register", command=register_user).grid(row=3, columnspan=2, pady=20)


def open_dashboard():
    global dashboard_window
    dashboard_window = Toplevel(root)
    dashboard_window.title("Dashboard")
    dashboard_window.geometry("400x400")

    frame = Frame(dashboard_window)
    frame.pack(pady=30)

    label = Label(frame, text="Welcome to the Dashboard", font=("Arial", 16))
    label.grid(row=0, columnspan=2, pady=20)

    
    Button(frame, text="Mark Attendance", command=mark_attendance).grid(row=1, columnspan=2, pady=10, sticky='ew')
    Button(frame, text="View Performance", command=view_performance).grid(row=2, columnspan=2, pady=10, sticky='ew')
    Button(frame, text="Add Marks", command=add_marks).grid(row=3, columnspan=2, pady=10, sticky='ew')
    Button(frame, text="Evaluate Attendance", command=evaluate_attendance).grid(row=4, columnspan=2, pady=10, sticky='ew')
    Button(frame, text="Add Student", command=open_add_student_window).grid(row=5, columnspan=2, pady=10, sticky='ew')


def open_add_student_window():
    add_student_window = Toplevel(dashboard_window)
    add_student_window.title("Add Student")
    add_student_window.geometry("300x300")
    
    frame = Frame(add_student_window)
    frame.pack(pady=30, padx=30)

    Label(frame, text="Student Name:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    global name_entry
    name_entry = Entry(frame)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(frame, text="Email:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    global email_entry
    email_entry = Entry(frame)
    email_entry.grid(row=1, column=1, padx=10, pady=10)

    Button(frame, text="Add Student", command=add_student).grid(row=2, columnspan=2, pady=20)


def add_student():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    if name and email:
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Students (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            name_entry.delete(0, END)
            email_entry.delete(0, END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Please enter all fields")


def mark_attendance():
    mark_attendance_window = Toplevel(dashboard_window)
    mark_attendance_window.title("Mark Attendance")
    mark_attendance_window.geometry("300x300")
    
    frame = Frame(mark_attendance_window)
    frame.pack(pady=30, padx=30)

    Label(frame, text="Student ID:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    global attendance_stu_id_entry
    attendance_stu_id_entry = Entry(frame)
    attendance_stu_id_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(frame, text="Attendance:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    global attendance_status
    attendance_status = StringVar()
    attendance_status.set("Present")
    OptionMenu(frame, attendance_status, "Present", "Absent").grid(row=1, column=1, padx=10, pady=10)

    Button(frame, text="Mark Attendance", command=mark_attendance_in_db).grid(row=2, columnspan=2, pady=20)


def mark_attendance_in_db():
    stu_id = attendance_stu_id_entry.get().strip()
    status = attendance_status.get()
    if stu_id and status:
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT student_id FROM Students WHERE student_id = %s", (stu_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Student ID does not exist.")
                return
            cursor.execute("INSERT INTO Attendance (student_id, date, status) VALUES (%s, CURDATE(), %s)", (stu_id, status))
            conn.commit()
            messagebox.showinfo("Success", "Attendance marked successfully!")
            attendance_stu_id_entry.delete(0, END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Please enter student ID and select status")

def view_performance():
    view_performance_window = Toplevel(dashboard_window)
    view_performance_window.title("View Performance")
    view_performance_window.geometry("300x300")
    
    frame = Frame(view_performance_window)
    frame.pack(pady=30, padx=30)

    Label(frame, text="Student ID:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    global performance_stu_id_entry
    performance_stu_id_entry = Entry(frame)
    performance_stu_id_entry.grid(row=0, column=1, padx=10, pady=10)

    Button(frame, text="View Performance", command=fetch_performance).grid(row=1, columnspan=2, pady=20)


def fetch_performance():
    stu_id = performance_stu_id_entry.get().strip()
    if stu_id:
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("CALL GetStudentPerformance(%s)", (stu_id,))
            performance_records = cursor.fetchall()
            if performance_records:
                performance_info = "\n".join([f"{record[0]}: {record[1]} - {record[2]} marks" for record in performance_records])
                messagebox.showinfo("Performance", performance_info)
            else:
                messagebox.showerror("Error", "No performance data found for the student.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Please enter a Student ID.")


def add_marks():
    add_marks_window = Toplevel(dashboard_window)
    add_marks_window.title("Add Marks")
    add_marks_window.geometry("300x300")
    
    frame = Frame(add_marks_window)
    frame.pack(pady=30, padx=30)

    Label(frame, text="Student ID:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    global marks_stu_id_entry
    marks_stu_id_entry = Entry(frame)
    marks_stu_id_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(frame, text="Subject:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    global subject_entry
    subject_entry = Entry(frame)
    subject_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(frame, text="Marks (0-100):").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    global marks_entry
    marks_entry = Entry(frame)
    marks_entry.grid(row=2, column=1, padx=10, pady=10)

    Button(frame, text="Add Marks", command=add_marks_to_db).grid(row=3, columnspan=2, pady=20)


def add_marks_to_db():
    stu_id = marks_stu_id_entry.get().strip()
    subject = subject_entry.get().strip()
    marks = marks_entry.get().strip()

    if stu_id and subject and marks:
        try:
            marks = int(marks)
            if marks < 0 or marks > 100:
                messagebox.showerror("Error", "Marks should be between 0 and 100")
                return
        except ValueError:
            messagebox.showerror("Error", "Marks must be a number between 0 and 100")
            return

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT student_id FROM Students WHERE student_id = %s", (stu_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Student ID does not exist.")
                return
            cursor.execute("INSERT INTO Performance (student_id, subject, marks) VALUES (%s, %s, %s)", (stu_id, subject, marks))
            conn.commit()
            messagebox.showinfo("Success", "Marks added successfully!")
            marks_stu_id_entry.delete(0, END)
            subject_entry.delete(0, END)
            marks_entry.delete(0, END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Please fill all fields")


def evaluate_attendance():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("CALL ListLowAttendanceStudents()")
        low_attendance_students = cursor.fetchall()
        if low_attendance_students:
            low_attendance_info = "\n".join([f"{student[0]} has low attendance." for student in low_attendance_students])
            messagebox.showinfo("Low Attendance", low_attendance_info)
        else:
            messagebox.showinfo("Low Attendance", "No students with low attendance found.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        conn.close()


root = Tk()
root.title("Student Management System")
root.geometry("300x250")

frame = Frame(root)
frame.pack(pady=50)

login_button = Button(frame, text="Login", command=open_login_window)
login_button.pack(pady=10)

register_button = Button(frame, text="Register", command=open_register_window)
register_button.pack(pady=10)

root.mainloop()
