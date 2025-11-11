import speech_recognition as sr

def transcribe_audio_free_google():
    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                print("Đang nghe...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                text = r.recognize_google(audio, language="vi-VN") # Thay đổi ngôn ngữ nếu cần
                print("Text:", text)
        except sr.WaitTimeoutError:
            print("Hết thời gian chờ.")
        except sr.UnknownValueError:
            print("Không nhận diện được giọng nói.")
        except sr.RequestError as e:
            print(f"Lỗi từ Google Web Speech API: {e}")
