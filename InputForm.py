import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from helper import isValidYoutubeLink, getInfoVideo, getListFromPlaylist
import threading
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

class InputForm(ttk.Frame):
    def __init__(self, master, label_text, button_text, app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Lưu trữ đối tượng lớp App
        self.app = app
        
        # Tạo một biến StringVar để lưu trữ dữ liệu nhập vào
        self.input_var = tk.StringVar()

        # Tạo một nhãn để mô tả ô nhập liệu
        self.input_label = ttk.Label(self, text=label_text)

        # Tạo ô nhập liệu và liên kết với biến StringVar
        self.input_entry = ttk.Entry(self, textvariable=self.input_var)

        # Tạo nút và liên kết với hàm xử lý sự kiện
        self.button = ttk.Button(self, text=button_text, command=self._on_button_click)

        # Đặt các thành phần lên giao diện theo thứ tự bằng hàm grid()
        self.input_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.input_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.button.grid(row=0, column=2, padx=5, pady=5)

        # Thiết lập cấu trúc cột của frame
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)

    def _on_button_click(self):
        # Lấy dữ liệu từ ô nhập liệu
        input_text = self.input_var.get()
        rs = isValidYoutubeLink(input_text.strip())
        if rs == 0:
            return messagebox.showinfo("Notification", "Invalid URL, please enter in YouTube format")
        if rs == 1 or rs == 11:
            messagebox.showinfo("Notification", "[W] Adding, please wait for a moment")
            resGetInfo = getInfoVideo(input_text.strip(), self.app.driver, rs, self.app.on_submit)
            if resGetInfo == False:
                messagebox.showinfo("Notification", "Something went wrong, please try again")
            else:
                messagebox.showinfo("Notification", "Added successfully")
            # download_thread = threading.Thread(target=getInfoVideo, args=(input_text.strip(), rs, self.app.on_submit))
            # download_thread.start()
        if rs == 2:
            messagebox.showinfo("Notification", "[E] Adding, please wait for a moment")
        if rs == 3:
            messagebox.showinfo("Notification", "[P] Adding, please wait for a moment")
            playlist = getListFromPlaylist(input_text.strip(), self.app.driver)
            print(playlist)
            for vi in playlist:
                getInfoVideo("https://www.y2meta.com{}".format(vi), self.app.driver, 9, self.app.on_submit)
            messagebox.showinfo("Notification", "Added successfully")
        if rs == 4:
            messagebox.showinfo("Notification", "[S] Adding, please wait for a moment")
            resGetInfo = getInfoVideo(input_text.strip(), self.app.driver, rs, self.app.on_submit)
            if resGetInfo == False:
                messagebox.showinfo("Notification", "Something went wrong, please try again")
            else:
                messagebox.showinfo("Notification", "Added successfully")
