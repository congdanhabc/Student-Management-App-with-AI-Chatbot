from view.home_page import HomePage
from view.manager_page import ManagerPage
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

class Dashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quản lý sinh viên")
        self.root.geometry("1200x760+150+20")
        # Khởi tạo theme
        self.is_dark_theme = True
        self.theme_colors = {
            "dark": {
                "bg": "#1c1c1c",
                "fg": "white",
                "button_bg": "#2c2c2c",
                "top_bar_bg": "#2c2c2c",
                "sidebar_bg": "#2c2c2c"
            },
            "light": {
                "bg": "white",
                "fg": "black", 
                "button_bg": "#e0e0e0",
                "top_bar_bg": "#f0f0f0",
                "sidebar_bg": "#f0f0f0"
            }
        }

        # Khởi tạo biến để theo dõi trang hiện tại
        self.current_page = None
        self.chatbot_window = None
        
        # Áp dụng theme ban đầu
        self.apply_theme()

        # Tạo khung sidebar
        self.create_sidebar()

        # Tạo khung nội dung chính
        self.content_frame = tk.Frame(self.root, name="content_frame", bg=self.get_current_theme()["bg"])
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Tạo settings frame
        self.create_settings()

        self.home_page()
        self.root.mainloop()

    def create_sidebar(self):
        colors = self.get_current_theme()
        self.sidebar = tk.Frame(self.root, name="side_bar", bg=colors["sidebar_bg"], width=200)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(
            self.sidebar, 
            text="Quản lý sinh viên", 
            bg=colors["sidebar_bg"], 
            fg=colors["fg"], 
            font=("Arial", 16)
        ).pack(pady=20)

        nav_items = {"Trang chủ": ["home", self.home_page], "Quản lý học vụ": ["manager", self.manager_page]}
        for item, value in nav_items.items():
            tk.Button(
                self.sidebar, 
                name=value[0],
                text=item, 
                bg=colors["button_bg"], 
                fg=colors["fg"], 
                font=("Arial", 12), 
                width=30, 
                height=2, 
                command=value[1]
            ).pack(fill="x", pady=5)


    def create_settings(self):
        colors = self.get_current_theme()
        settings_frame = tk.Frame(self.sidebar, bg=colors["sidebar_bg"])
        settings_frame.pack(side="bottom", pady=20)

        # Tải và chuẩn bị icon settings
        settings_icon = Image.open("assets/settings.png")
        settings_icon = settings_icon.resize((30, 30), Image.LANCZOS)
        self.settings_icon = ImageTk.PhotoImage(settings_icon)

        self.settings_button = tk.Button(
            settings_frame,
            image=self.settings_icon,
            bg=colors["sidebar_bg"],
            bd=0,
            command=self.show_settings_menu
        )
        self.settings_button.pack(side="left", padx=10)

        # # Tải và chuẩn bị icon micro
        # micro_icon = Image.open("assets/mic.png")
        # micro_icon = micro_icon.resize((30, 30), Image.LANCZOS)
        # self.micro_icon = ImageTk.PhotoImage(micro_icon)

        # self.micro_button = tk.Button(
        #     settings_frame,
        #     image=self.micro_icon,
        #     bg=colors["sidebar_bg"],
        #     bd=0,
        #     command=self.open_voice_recognition
        # )
        # self.micro_button.pack(side="left", padx=10)

    def show_settings_menu(self):
        settings_menu = tk.Menu(self.root, tearoff=0)
        current_theme = "Sáng" if self.is_dark_theme else "Tối"
        settings_menu.add_command(
            label=f"Đổi sang theme {current_theme}",
            command=self.toggle_theme
        )
        
        # Hiển thị menu tại vị trí chuột
        settings_menu.post(
            self.settings_button.winfo_rootx(),
            self.settings_button.winfo_rooty()
        )

    def get_current_theme(self):
        return self.theme_colors["dark" if self.is_dark_theme else "light"]

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
        # Cập nhật lại giao diện
        self.refresh_interface()

    def apply_theme(self):
        colors = self.get_current_theme()
        self.root.configure(bg=colors["bg"])

    def refresh_interface(self):
        # Xóa và tạo lại toàn bộ giao diện
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tạo lại sidebar và nội dung chính
        self.create_sidebar()
        self.content_frame = tk.Frame(self.root, bg=self.get_current_theme()["bg"])
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Tạo lại settings
        self.create_settings()

        # Hiển thị lại trang chính hoặc giao diện hiện tại
        self.home_page()

    # def open_chatbot(self):
    #     # Đóng cửa sổ chatbot cũ nếu có
    #     if self.chatbot_window:
    #         self.chatbot_window.destroy()

    #     # Tạo cửa sổ mới cho chatbot
    #     self.chatbot_window = tk.Toplevel(self.root)
    #     self.chatbot_window.title("Nhận diện giọng nói")
    #     self.chatbot_window.geometry("400x300+500+300")
    #     self.chatbot_window.configure(bg=self.get_current_theme()["bg"])
        
    #     # Thêm label hướng dẫn
    #     tk.Label(
    #         self.chatbot_window,
    #         text="Nói 'trợ giúp' để xem danh sách lệnh",
    #         bg=self.get_current_theme()["bg"],
    #         fg=self.get_current_theme()["fg"],
    #         font=("Arial", 12)
    #     ).pack(pady=10)
        
    #     # Label hiển thị kết quả
    #     self.result_label = tk.Label(
    #         self.chatbot_window,
    #         text="Kết quả nhận diện sẽ hiển thị tại đây",
    #         bg=self.get_current_theme()["bg"],
    #         fg=self.get_current_theme()["fg"],
    #         font=("Arial", 12),
    #         wraplength=350
    #     )
    #     self.result_label.pack(pady=20)

    #     tk.Label(
    #         self.chatbot_window,
    #         text="Đang lắng nghe... Hãy nói để thực hiện hành động!",
    #         bg=self.get_current_theme()["bg"],
    #         fg=self.get_current_theme()["fg"],
    #         font=("Arial", 12),
    #         wraplength=380
    #     ).pack(expand=True, padx=20)

    #     # Nút điều khiển
    #     button_frame = tk.Frame(
    #         self.chatbot_window,
    #         bg=self.get_current_theme()["bg"]
    #     )
    #     button_frame.pack(pady=20)

    #     tk.Button(
    #         button_frame,
    #         text="Bắt đầu",
    #         bg="lightblue",
    #         fg="black",
    #         command=self.start_recognition
    #     ).pack(side="left", padx=10)

    #     tk.Button(
    #         button_frame,
    #         text="Đóng",
    #         bg="lightcoral",
    #         fg="black",
    #         command=self.chatbot_window.destroy
    #     ).pack(side="left", padx=10)

    # def start_recognition(self):
    #     """Hàm khởi động nhận diện giọng nói."""
    #     recognize_speech(self, self.update_result)

    # def update_result(self, text):
    #     """Cập nhật kết quả nhận diện lên giao diện."""
    #     if hasattr(self, 'result_label'):
    #         self.result_label.config(text=f"Kết quả: {text}")

    def export_data(self, file_type="excel"):
        """Xuất dữ liệu ra file."""
        if self.current_page:
            # Gọi phương thức xuất dữ liệu của trang hiện tại
            if hasattr(self.current_page, 'export_data'):
                self.current_page.export_data(file_type)
            else:
                messagebox.showwarning("Thông báo", "Chức năng xuất file chưa được hỗ trợ ở trang này")
        else:
            messagebox.showwarning("Thông báo", "Vui lòng chọn trang cần xuất dữ liệu")

    def refresh_data(self):
        """Làm mới dữ liệu trang hiện tại."""
        if self.current_page:
            if hasattr(self.current_page, 'refresh_data'):
                self.current_page.refresh_data()
            else:
                messagebox.showwarning("Thông báo", "Không thể làm mới dữ liệu ở trang này")
        else:
            messagebox.showwarning("Thông báo", "Không có trang nào được chọn")

    def home_page(self):
        """Chuyển đến trang chủ."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_page = HomePage(self.content_frame, self.theme_colors, self.is_dark_theme)

    def handle_command(self, command):
        """Xử lý lệnh nhận diện được."""
        if "điểm danh" in command.lower():
            tk.messagebox.showinfo("Hành động", "Thực hiện điểm danh!")
        elif "đóng" in command.lower():
            self.root.destroy()
        else:
            tk.messagebox.showwarning("Lệnh không hợp lệ", "Không hiểu lệnh. Vui lòng thử lại.")

    def manager_page(self):
        """Chuyển đến trang quản lý."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_page = ManagerPage(self.content_frame)
