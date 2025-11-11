import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from controller.chatbot import Chatbot
import speech_recognition as sr

def transcribe_audio():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Đang nghe...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            text = r.recognize_google(audio, language="vi-VN") # Thay đổi ngôn ngữ nếu cần
            return text
    except sr.WaitTimeoutError:
        print("Hết thời gian chờ.")
    except sr.UnknownValueError:
        print("Không nhận diện được giọng nói.")
    except sr.RequestError as e:
        print(f"Lỗi từ Google Web Speech API: {e}")


class ChatbotView:
    def __init__(self, root):
        self.root = root
        self.chatbot = Chatbot(self.root)
        self.user_id = "customer_bot"
        
        self.chatbot_window = tk.Toplevel(root)
        self.chatbot_window.title("AI Chatbot")
        self.chatbot_window.geometry("500x600")
        
        # Khung hiển thị tin nhắn
        self.chat_display = tk.Text(self.chatbot_window, state='disabled', wrap=tk.WORD, font=("Arial", 12))
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Khung nhập tin nhắn
        input_frame = tk.Frame(self.chatbot_window)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Ô nhập tin nhắn
        self.message_entry = tk.Entry(input_frame, width=40)
        self.message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,10))
        
        # Nút micro
        # mic_icon = Image.open("assets/mic.png")
        # mic_icon = mic_icon.resize((25, 25), Image.LANCZOS)
        # self.mic_icon = ImageTk.PhotoImage(mic_icon)
        # 
        # mic_button = tk.Button(input_frame, image=self.mic_icon, 
        #                        command=self.start_speech_recognition, 
        #                        bd=0)
        # mic_button.pack(side=tk.RIGHT)
        
        # Nút gửi
        send_button = tk.Button(input_frame, text="Gửi", command=self.send_message)
        send_button.pack(side=tk.RIGHT, padx=5)

        self.update_chat_display("Chatbot: Chào bạn, đây là AI chatbot! Bạn cần tôi giúp gì ?")
    
    def send_message(self):
        message = self.message_entry.get()
        self.update_chat_display("\nNgười dùng: " + message)
        # Handle the query and print the response
        response = self.chatbot.handle_customer_query(self.user_id, message)
        self.message_entry.delete(0, tk.END)
        self.update_chat_display("\nChatbot: " + response)
    
    def start_speech_recognition(self):
        text = None
        while text is None:
            text = transcribe_audio()
        self.message_entry.insert(tk.END, " " + text)
    
    def update_chat_display(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)