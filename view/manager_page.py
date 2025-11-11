from controller.schedule import ScheduleController
from controller.send_mail import AbsenteeManager

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class ManagerPage:
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.schedule_controller = ScheduleController()
        self.absent_list = self.schedule_controller.get_absent_list()
        self.email_manager = AbsenteeManager()


        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.home_frame = tk.Frame(self.content_frame, name="home_frame", bg="#1c1c1c")
        self.home_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.show_manager_page()

    def show_manager_page(self):
        # Tạo khung top bar trong khung nội dung
        top_bar = tk.Frame(self.home_frame, bg="#2c2c2c", height=50)
        top_bar.pack(side="top", fill="x")

        # Thêm tiêu đề vào top bar
        tk.Label(top_bar, text="Quản lý học vụ", bg="#2c2c2c", fg="white", font=("Arial", 14)).pack(side="left", padx=10)

        # Tạo khung cho các chức năng
        self.function_frame = tk.Frame(self.home_frame, name="function_frame", bg="#1c1c1c")
        self.function_frame.pack(pady=20)

        # Thêm các nút gửi mail       
        tk.Button(self.function_frame, name="show_no_email", text="DS Sinh Viên chưa có Mail", bg="#2c2c2c", fg="white", font=("Arial", 12), width=20, command=lambda: self.show_students_missing_gmail()).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(self.function_frame, name="send_excel", text="Gửi excel tổng hợp", bg="#2c2c2c", fg="white", font=("Arial", 12), width=20, command=lambda: self.send_excel()).grid(row=1, column=2, padx=10, pady=5)
        tk.Button(self.function_frame, name="send_email", text="Gửi Email Hàng Loạt", bg="#2c2c2c", fg="white", font=("Arial", 12), width=20, command=lambda: self.send_bulk_emails()).grid(row=1, column=4, padx=10, pady=5)
        # Khu vực hiển thị kết quả với Treeview
        result_frame = tk.Frame(self.home_frame, bg="#1c1c1c")
        result_frame.pack(fill="both", expand=True)

        # Tạo Treeview để hiển thị kết quả
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("MaSinhVien", "TenSinhVien", "TenMonHoc", "SoBuoi", "ThoiLuong")
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show="headings", style="Treeview")

        self.result_tree.heading("MaSinhVien", text="Mã sinh viên")
        self.result_tree.heading("TenSinhVien", text="Tên sinh viên")
        self.result_tree.heading("TenMonHoc", text="Tên môn học")
        self.result_tree.heading("SoBuoi", text="Số buổi vắng")
        self.result_tree.heading("ThoiLuong", text="Thời lượng vắng")

        # Đặt chiều rộng cột và tô màu nền khác nhau
        self.result_tree.column("MaSinhVien", width=100, anchor="center")
        self.result_tree.column("TenSinhVien", width=150, anchor="center")
        self.result_tree.column("TenMonHoc", width=150, anchor="center")
        self.result_tree.column("SoBuoi", width=60, anchor="center")
        self.result_tree.column("ThoiLuong", width=70, anchor="center")

        self.result_tree.tag_configure('evenrow', background='white')
        self.result_tree.tag_configure('oddrow', background='#e6e6e6')

        self.result_tree.pack(fill="both", expand=True, padx=10, pady=10) 
        self.result_tree.bind("<Double-1>", lambda event: self.send_email_for_selected_student())

        for index, absent in enumerate(self.absent_list):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            values = (absent["MaSinhVien"], absent["TenSinhVien"], absent["TenMonHoc"], absent["SoBuoi"], absent["ThoiLuong"])
            self.result_tree.insert("", "end", values=values, tags=tag)       
        
    def show_students_missing_gmail(self):
        missing_gmail_list = self.email_manager.get_students_missing_gmail(self.absent_list)
        
        if not missing_gmail_list:
            tk.messagebox.showinfo("Thông báo", "Tất cả sinh viên đã có Gmail hợp lệ.")
            return

        dialog = tk.Toplevel(self.content_frame)
        dialog.title("Danh sách sinh viên thiếu Gmail")
        dialog.geometry("500x400")

        tk.Label(dialog, text="Danh sách sinh viên thiếu Gmail:", font=("Arial", 12)).pack(padx=10, pady=10)

        tree = ttk.Treeview(dialog, columns=("MaSinhVien", "TenSinhVien", "EmailSinhVien", "EmailPhuHuynh"), show="headings")
        tree.heading("MaSinhVien", text="Mã SV")
        tree.heading("TenSinhVien", text="Tên SV")
        tree.heading("EmailSinhVien", text="Email SV")
        tree.heading("EmailPhuHuynh", text="Email Phụ Huynh")

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for student in missing_gmail_list:
            tree.insert("", tk.END, values=(
                student["MaSinhVien"],
                student["TenSinhVien"],
                student["EmailSinhVien"],
                student["EmailPhuHuynh"]
            ))

        tk.Button(dialog, text="Đóng", command=dialog.destroy).pack(pady=10)

    def send_excel(self):
        try:
            self.email_manager.send_excel_report(self.absent_list)
            tk.messagebox.showinfo("Thành công", "Gửi file Excel thành công")
        except Exception as e:
            print(e)
            tk.messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi gửi file Excel:\n{e}")

    def send_bulk_emails(self):
        try:
            # Gọi phương thức gửi email hàng loạt
            success_count, failure_count, error_list = self.email_manager.send_bulk_emails(self.absent_list)

            # Hiển thị kết quả gửi email
            message = f"Đã gửi thành công {success_count} email.\nKhông gửi được {failure_count} email."
            if error_list:
                message += "\n\nDanh sách lỗi:\n" + "\n".join(error_list)

            tk.messagebox.showinfo("Kết quả gửi email", message)
        except Exception as e:
            print(e)
            tk.messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi gửi email hàng loạt:\n{e}")

    def send_email_for_selected_student(self):
        selected_item = self.result_tree.focus()  # Lấy item được chọn
        if not selected_item:
            tk.messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sinh viên để gửi email.")
            return

        student_values = self.result_tree.item(selected_item, "values")  # Lấy thông tin từ Treeview
        student_info = {
            "MaSinhVien": student_values[0],
            "TenSinhVien": student_values[1],
            "TenMonHoc": student_values[2],
            "SoBuoi": student_values[3],
            "ThoiLuong": student_values[4],
            "EmailSinhVien": self.get_student_email(student_values[0])  # Lấy email sinh viên từ hàm hỗ trợ
        }

        if not student_info["EmailSinhVien"]:
            tk.messagebox.showwarning("Cảnh báo", f"Không tìm thấy email của sinh viên {student_info['TenSinhVien']}.")
            return

        # Gửi email thông qua AbsenteeManager
        success, message = self.email_manager.send_email_for_student(student_info)
        if success:
            tk.messagebox.showinfo("Thành công", message)
        else:
            tk.messagebox.showerror("Lỗi", message)

    # Hàm hỗ trợ lấy email sinh viên (giả sử từ cơ sở dữ liệu hoặc danh sách có sẵn)
    def get_student_email(self, student_id):
        for student in self.absent_list:
            if student["MaSinhVien"] == student_id:
                return student.get("EmailSinhVien")
        return None
