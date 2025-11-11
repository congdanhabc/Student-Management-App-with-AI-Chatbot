🎓 Ứng Dụng Quản Lý Sinh Viên với Chatbot AI

Đây là một dự án ứng dụng Desktop được xây dựng bằng Python và Tkinter, cung cấp một giải pháp toàn diện để quản lý thông tin sinh viên. Điểm nhấn đặc biệt của dự án là Chatbot "Nghĩa", một trợ lý ảo được xây dựng bằng Google Gemini API, có khả năng hiểu ngôn ngữ tự nhiên để thực thi các tác vụ quản lý phức tạp, giúp tự động hóa và đơn giản hóa công việc.

✨ Các Tính Năng Chính

Ứng dụng cung cấp hai phương thức tương tác chính: thao tác thủ công qua giao diện và ra lệnh qua chatbot.

a) Thao Tác Thủ Công

Giao diện đồ họa (GUI) thân thiện, cho phép thực hiện đầy đủ các tác vụ quản lý:


    👤 Quản lý sinh viên (CRUD): Thêm, xem, sửa, xóa thông tin sinh viên một cách trực quan.

    📊 Nhập từ Excel: Nhanh chóng thêm hàng loạt sinh viên vào hệ thống từ một file Excel có sẵn.

    📧 Lọc & Xuất Dữ Liệu: Dễ dàng trích xuất danh sách sinh viên chưa có thông tin email.

    ✉️ Gửi Email Báo Cáo: Tự động soạn và gửi email đính kèm file Excel tổng hợp thông tin chuyên cần đến người quản lý.

    ⚠️ Gửi Email Cảnh Báo Hàng Loạt: Tự động gửi email cảnh cáo học vụ đến những sinh viên có số buổi vắng vượt quá quy định.

b) Tương Tác Với Chatbot "Nghĩa"

Thay vì thao tác thủ công, bạn có thể "trò chuyện" hoặc "ra lệnh" cho trợ lý ảo Nghĩa. Chatbot được huấn luyện để phân tích yêu cầu của bạn và thực hiện một trong các chức năng sau:

    1. Thêm sinh viên
       
    2. Xem thông tin sinh viên

    3. Liệt kê sinh viên thiếu email

    4. Gửi báo cáo tổng hợp

    5. Gửi email cảnh báo hàng loạt

    6. Trò chuyện thông thường

🛠️ Công Nghệ Sử Dụng

    Ngôn ngữ: Python

    Giao diện (GUI): Tkinter

    Mô hình ngôn ngữ (LLM): Google Gemini API

    Lưu trữ & Truy vấn Vector: Qdrant

    Quản lý bộ nhớ Chatbot: Mem0

    Thao tác với Excel: Openpyxl, Pandas

    Gửi Email: smtplib

⚙️ Hướng Dẫn Cài Đặt và Sử Dụng
Yêu Cầu

    Python 3.10+ (Khuyến khích 3.12)

    Git

Các Bước Cài Đặt

1. Tải dự án về máy:
code Bash


    git clone https://github.com/congdanhabc/Student-Management-App-with-AI-Chatbot.git

    cd Student-Management-App-with-AI-Chatbot

2. Tạo và kích hoạt môi trường ảo:
code Bash

    
    # Lệnh cho Windows

    python -m venv .venv
    .\.venv\Scripts\activate

  

3. Cài đặt các thư viện cần thiết:
Sử dụng file requirements.txt đã được cung cấp để cài đặt tất cả các gói phụ thuộc.
code Bash

    
    pip install -r requirements.txt

  

4. Cấu hình các biến môi trường:
Dự án cần các thông tin nhạy cảm để hoạt động.

    Trong thư mục gốc, sao chép file example.env và đổi tên bản sao thành .env.

    Mở file .env và điền đầy đủ các thông tin của bạn vào các trường còn trống:

        SENDER_EMAIL: Email bạn sẽ dùng để gửi báo cáo/cảnh báo.

        SENDER_APP_PASSWORD: Mật khẩu ứng dụng (16 ký tự) của email trên. Lấy tại quản lý tài khoản Google.

        MANAGER_EMAIL: Email của người quản lý sẽ nhận báo cáo.

        GEMINI_API_KEY: API Key để sử dụng Gemini. Lấy tại Google AI Studio.

5. Chạy Ứng Dụng:
Sau khi hoàn tất cài đặt, thực thi file Python chính (ví dụ main.py):
code Bash

    
    python main.py
