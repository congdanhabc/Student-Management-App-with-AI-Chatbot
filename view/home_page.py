from controller.student import StudentController
from controller.importExcel import import_excel
from view.profile_page import ProfilePage
from view.chatbot_view import ChatbotView
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import date, datetime
from PIL import ImageTk, Image

class HomePage:
    def __init__(self, content_frame, theme_colors, is_dark_theme):
        self.student_controller = StudentController()
        self.content_frame = content_frame
        self.theme_colors = theme_colors
        self.is_dark_theme = is_dark_theme

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        colors = self.theme_colors["dark" if self.is_dark_theme else "light"]
        self.home_frame = tk.Frame(self.content_frame, name="home_frame", bg=colors["bg"])
        self.home_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.show_home_page()
        self.update_search_results()
    
    def show_home_page(self):
        # Tạo khung top bar trong khung nội dung
        top_bar = tk.Frame(self.home_frame, bg="#2c2c2c", height=50)
        top_bar.pack(side="top", fill="x")

        # Thêm tiêu đề vào top bar
        tk.Label(top_bar, text="Quản lý sinh viên", bg="#2c2c2c", fg="white", font=("Arial", 14)).pack(side="left", padx=10)

        # Tạo khung cho các chức năng
        self.function_frame = tk.Frame(self.home_frame, name="function_frame", bg="#1c1c1c")
        self.function_frame.pack(pady=20)

        chatbot_icon = Image.open("assets/chatbot1.png")  # Thay đổi đường dẫn icon
        chatbot_icon = chatbot_icon.resize((50, 50), Image.LANCZOS)
        self.chatbot_icon = ImageTk.PhotoImage(chatbot_icon)
        
        chatbot_button = tk.Button(top_bar, image=self.chatbot_icon, 
                                command=self.open_chatbot, 
                                bg="#2c2c2c", bd=0)
        chatbot_button.pack(side="right", padx=10)

        # Chức năng tìm kiếm
        tk.Label(self.function_frame, text="Tìm kiếm sinh viên", bg="#1c1c1c", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        self.search_entry = tk.Entry(self.function_frame, width=50)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.function_frame, text="Tìm kiếm", bg="#2c2c2c", fg="white", font=("Arial", 12), command=lambda: self.update_search_results()).grid(row=0, column=2, padx=10, pady=5)

        # Thêm các nút phụ dưới thanh tìm kiếm
        tk.Button(self.function_frame, text="Nhập Excel", bg="#2c2c2c", fg="white", font=("Arial", 12), width=15, command=lambda: self.import_excel()).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(self.function_frame, text="Chi tiết", bg="#2c2c2c", fg="white", font=("Arial", 12), width=15, command=lambda: self.view_profile()).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.function_frame, text="Xóa", bg="#2c2c2c", fg="white", font=("Arial", 12), width=15, command=lambda: self.delete_student()).grid(row=1, column=2, padx=10, pady=5)
        tk.Button(self.function_frame, name="add_student", text="Thêm sinh viên", bg="#2c2c2c", fg="white", font=("Arial", 12), width=15, command=lambda: self.add_student_dialog()).grid(row=1, column=3, padx=10, pady=5)

        # Khu vực hiển thị kết quả với Treeview
        result_frame = tk.Frame(self.home_frame, bg="#1c1c1c")
        result_frame.pack(fill="both", expand=True)

        # Tạo Treeview để hiển thị kết quả
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("STT", "MaSinhVien", "TenSinhVien", "GioiTinh", "NgaySinh")
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.result_tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, False))

        self.result_tree.heading("STT", text="STT")
        self.result_tree.heading("MaSinhVien", text="Mã sinh viên")
        self.result_tree.heading("TenSinhVien", text="Tên sinh viên")
        self.result_tree.heading("GioiTinh", text="Giới tính")
        self.result_tree.heading("NgaySinh", text="Ngày sinh")

        # Đặt chiều rộng cột và tô màu nền khác nhau
        self.result_tree.column("STT", width=50, anchor="center")
        self.result_tree.column("MaSinhVien", width=100, anchor="center")
        self.result_tree.column("TenSinhVien", width=150, anchor="center")
        self.result_tree.column("GioiTinh", width=60, anchor="center")
        self.result_tree.column("NgaySinh", width=70, anchor="center")

        self.result_tree.tag_configure('evenrow', background='white')
        self.result_tree.tag_configure('oddrow', background='#e6e6e6')

        self.result_tree.pack(fill="both", expand=True, padx=10, pady=10)


    def open_chatbot(self):
        # Tạo chatbot view với root là cửa sổ chính
        root = self.content_frame.winfo_toplevel()
        ChatbotView(root)

    def update_search_results(self):
        # Xóa nội dung cũ
        for row in self.result_tree.get_children():
            self.result_tree.delete(row)

        # Lấy kết quả tìm kiếm
        name = self.search_entry.get()
        results = self.student_controller.search_student_by_name(name)

        # Chèn kết quả mới vào
        for index, result in enumerate(results):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            values = (result["STT"], result["MaSinhVien"], result["HoTen"], result["GioiTinh"], result["NgaySinh"])
            self.result_tree.insert("", "end", values=values, tags=tag)

    def view_profile(self):
        selected_item = self.result_tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sinh viên!")
            return
        item = self.result_tree.item(selected_item)
        values = item["values"]
        ma_sinh_vien = values[1]
        ProfilePage(self.content_frame, ma_sinh_vien)

    def delete_student(self):
        selected_item = self.result_tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sinh viên!")
            return
        item = self.result_tree.item(selected_item)
        values = item["values"]
        ma_sinh_vien = values[1]
        if self.student_controller.delete_student(ma_sinh_vien):
            tk.messagebox.showinfo("Thành công", "Xóa sinh viên thành công")
        for row in self.result_tree.get_children():
            self.result_tree.delete(row)

    def add_student_dialog(self):
        # Tạo một cửa sổ hộp thoại mới
        dialog = tk.Toplevel(self.content_frame, name="add_student_dialog")
        dialog.title("Thêm Sinh Viên")
        dialog.geometry("+450+200")
    
        # Nhãn và ô nhập mã sinh viên 
        tk.Label(dialog, text="Mã Sinh Viên:").grid(row=0, column=0, padx=10, pady=5) 
        self.student_id_entry = tk.Entry(dialog, name="id") 
        self.student_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Nhãn và ô nhập họ tên
        tk.Label(dialog, text="Họ Tên:").grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(dialog, name="name")
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Nhãn và ô chọn giới tính
        tk.Label(dialog, text="Giới Tính:").grid(row=2, column=0, padx=10, pady=5)
        self.gender_entry = tk.StringVar(dialog ,value="Nam")  # Giá trị mặc định
        gender_options = ["Nam", "Nữ"]
        gender_menu = ttk.OptionMenu(dialog, self.gender_entry, self.gender_entry.get(), *gender_options)
        gender_menu.grid(row=2, column=1, padx=10, pady=5)
        
        # Nhãn và ô nhập ngày sinh
        tk.Label(dialog, text="Ngày Sinh (dd/mm/yyyy):").grid(row=3, column=0, padx=10, pady=5)
        self.birthDay_entry = tk.Entry(dialog, name="birth")
        #DateEntry(dialog, name="birth", date_pattern="dd/MM/yyyy", mindate=date(1900, 1, 1), year=date.today().year, month=date.today().month, day=date.today().day)
        self.birthDay_entry.grid(row=3, column=1, padx=10, pady=5)
        # self.birthDay_entry.bind("<FocusOut>", lambda e: self.validate_date(self.birthDay_entry.get()))

        tk.Button(dialog, name="save", text="Lưu", width=10, command=lambda: self.add_student()).grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(dialog, name="gender_change", width=0, height=0, command=lambda: self.gender_entry.set("Nữ"), relief='flat', borderwidth=0).grid(row=5, column=0, columnspan=2, pady=10)


    def validate_date(self, default):
        try:
            datetime.strptime(self.birthDay_entry.get(), "%d/%m/%Y")
            return True
        except ValueError:
            self.birthDay_entry.set_date(default)

    def add_student(self):
        ma_sinh_vien = self.student_id_entry.get().strip()
        name = self.name_entry.get().strip() 
        gender = self.gender_entry.get() 
        birth_date = self.birthDay_entry.get() # Kiểm tra xem có ô nào bị bỏ trống 
        if not name or not gender or not birth_date: 
            tk.messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin vào tất cả các ô!")
        if self.student_controller.add_student(ma_sinh_vien, name, gender, birth_date):
            tk.messagebox.showinfo("Thành công", "Thêm sinh viên thành công")
        else:
            tk.messagebox.showwarning("Cảnh báo", "Thêm sinh viên không thành công")
        

    def import_excel(self):
        excel_path = filedialog.askopenfilename()
        if excel_path:
            try:
                import_excel(excel_path)
                tk.messagebox.showinfo("Thành công", "Dữ liệu Excel đã được nhập thành công")
                self.update_search_results()
            except Exception as e:
                print(e)
                tk.messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi nhập dữ liệu từ Excel:\n{e}")

    def sort_column(self, col, reverse):
        data = [(self.convert_to_number(self.result_tree.set(k, col)), k) for k in self.result_tree.get_children('')]
        data.sort(reverse=reverse, key=lambda x: x[0])

        for index, (val, k) in enumerate(data):
            self.result_tree.move(k, '', index)

        self.result_tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def convert_to_number(self, value):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value