import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import csv
from InputForm import InputForm
from video import Video
from datetime import datetime
import threading
from selenium import webdriver
import chromedriver_autoinstaller
from helper import DownloadVideo
from tkinter import filedialog
import os
import subprocess
import json

dataTable = []

class App:
    def __init__(self, root):
        # Đặt tiêu đề cho cửa sổ
        root.title("YDownloader")

        # Tạo một form nhập liệu và đặt vào cửa sổ chính
        self.input_form = InputForm(root, "URL: ", "+ Add", self)
        self.input_form.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.columns = ('File Name', 'Resolution', 'URL', 'Size', 'Time', 'Status', 'Time Left', 'Date', 'MP3', 'STT')

        # Tạo bảng và đặt vào cửa sổ chính
        self.table = ttk.Treeview(root, columns=self.columns, show="headings")

        # Xác định tiêu đề của các cột
        self.table.heading('File Name', text='File Name')
        self.table.heading('URL', text='URL')
        self.table.heading('Size', text='Size')
        self.table.heading('Status', text='Status')
        self.table.heading('Time Left', text='Time Left')
        self.table.heading('Date', text='Date')
        self.table.heading('Time', text='Time')
        self.table.heading('Resolution', text='Resolution')
        self.table.heading('MP3', text='MP3')
        self.table.heading('STT', text='STT')

        # Căn chỉnh các cột trong bảng
        self.table.column('File Name', width=70, anchor='w')
        self.table.column('URL', width=0, anchor='w', stretch=tk.NO)
        self.table.column('Size', width=10, anchor='w')
        self.table.column('Status', width=10, anchor='w')
        self.table.column('Time Left', width=0, anchor='w', stretch=tk.NO)
        self.table.column('Date', width=50, anchor='w')
        self.table.column('Time', width=50, anchor='w')
        self.table.column('Resolution', width=50, anchor='w')
        self.table.column('MP3', width=0, anchor='w', stretch=tk.NO)
        self.table.column('STT', width=0, anchor='w', stretch=tk.NO)

        # Tạo thanh cuộn cho bảng
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        # Tạo sub-menu
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Download", command=self.dlVideo)
        self.menu.add_command(label="Delete", command=self.deleteRow)
        self.menu.add_command(label="Open", command=self.open_folder_and_select_file)

        self.table.bind("<Button-3>", self.popup)
        self.table.bind("<Control-Button-1>", self.popup)

        # Đặt bảng và thanh cuộn lên cửa sổ chính
        self.table.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Thiết lập cấu trúc cột của cửa sổ
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=0)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=1)

        # Tạo thread riêng biệt để chạy Selenium và lặp lại công việc
        self.selenium_thread = threading.Thread(target=self.selenium_task)
        self.selenium_thread.daemon = True
        self.selenium_thread.start()
        
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Thiết lập kích thước tối thiểu cho cửa sổ
        root.wm_minsize(700, 300)

        self.default_value()
        self._center_window(root)
    
    def selenium_task(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--start-maximized")
        opt.add_argument("--headless")

        chromedriver_autoinstaller.install()
        # Khởi tạo driver
        self.driver = webdriver.Chrome(options=opt)
        
        # while True:
        #     # Ngủ một lúc trước khi thực hiện lại công việc
        #     time.sleep(5)

    def on_submit(self, dataRender):
        video = Video(
            dataRender['title'],
            dataRender['url'],
            '',
            0,
            0,
            datetime.today().strftime('%Y-%m-%d'),
            dataRender['video'],
            [],
            dataRender['time'],
            root,
            self.reRenderTable,
            dataRender['y2m'],
            "",
            "",
            ""
        )
        print(video.getSetVideo())
        dataTable.append(video)
        tp = video.getSetVideo() + (len(dataTable) - 1,)
        item = self.table.insert('', 'end', values=tp)
        return

    def reRenderTable(self):
        self.table.delete(*self.table.get_children())
        for idx, vi in enumerate(dataTable):
            tp = vi.getSetVideo() + (idx,)
            print(tp)
            self.table.insert('', 'end', values=tp)
    
    def default_value(self):
        with open("data.csv", 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                rs = json.loads(row[6])
                video = Video(
                    row[0], row[1], row[2], int(row[3]), row[4], row[5], rs, row[7], row[8], root, self.reRenderTable, 
                    row[12], row[13], row[9], row[10]
                )
                dataTable.append(video)
        self.reRenderTable()
        return

    def deleteRow(self):
        selected_row = self.table.focus()
        resInfo = self.table.item(selected_row, "value")[-1]
        dataTable.pop(int(resInfo))
        self.reRenderTable()

    def dlVideo(self):
        selected_row = self.table.focus()
        print(selected_row)
        resInfo = self.table.item(selected_row, "value")[-1]
        _url = dataTable[int(resInfo)].getY2m()
        # _idx = dataTable[int(resInfo)].getIndexResolutionVideo()
        _btnDownload = dataTable[int(resInfo)].getBtnDownload()
        _name = dataTable[int(resInfo)].getName()
        _resolution = dataTable[int(resInfo)].getSigleResolution()
        folder_path = filedialog.askdirectory()
        messagebox.showinfo("Notifycation", "Downloading, please click OK to continue")
        rs = DownloadVideo(_url, self.driver, _btnDownload, _name, _resolution, folder_path)
        if (rs != False):
            messagebox.showinfo("Notifycation", "Download successful")
            dataTable[int(resInfo)].setStatus(1)
            dataTable[int(resInfo)].setLocation(rs)
        else:
            messagebox.showinfo("Notifycation", "Something Wrong, please try downloading again")
            dataTable[int(resInfo)].setStatus(2)
            dataTable[int(resInfo)].setLocation("")
        self.reRenderTable()

    def popup(self, event):
        # Tạo sub-menu cho cột đầu tiên
        row_id = self.table.identify_row(event.y)
        column_id = self.table.identify_column(event.x)
        if row_id and column_id:
            if column_id == "#2":
                resInfo = self.table.item(row_id, "value")[-1]
                print(dataTable[int(resInfo)].getStatus())
                if dataTable[int(resInfo)].getStatus() != "Success":
                    print(self.table.item(row_id, "value"))
                    dataTable[int(resInfo)].getMenuRes().post(event.x_root, event.y_root)
            else:
                resInfo = self.table.item(row_id, "value")[-1]
                print(self.table.item(row_id, "value"))
                self.menu.post(event.x_root, event.y_root)

    def open_folder_and_select_file(self):
        file_path = ""
        selected_row = self.table.focus()
        print(selected_row)
        resInfo = self.table.item(selected_row, "value")[-1]
        file_path = dataTable[int(resInfo)].getLocation()
        if file_path == "":
            messagebox.showinfo("Notifycation", "You haven't downloaded the file")
        else:
            # Lấy đường dẫn đầy đủ đến tập tin
            full_path = os.path.abspath(file_path)

            # Tạo đường dẫn đến thư mục chứa tập tin
            folder_path = os.path.dirname(full_path)

            # Mở thư mục và đưa người dùng đến vị trí của tập tin trong thư mục đó trên hệ thống
            subprocess.run(["open", "-R", full_path], cwd=folder_path)

    def _center_window(self, window):
        # Lấy kích thước của màn hình
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Tính toán vị trí và kích thước cho cửa sổ
        window_width = 500
        window_height = 300
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Thiết lập vị trí và kích thước cho cửa sổ
        window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

    def on_closing(self):
        self.driver.quit()
        with open(f'data.csv', mode='w') as file:
            writer = csv.writer(file)
            for vi in dataTable:
                writer.writerow(vi.extractAttribute().values())
                print(vi.extractAttribute())
        root.destroy()


# Tạo cửa sổ Tkinter
root = tk.Tk()

# Tạo ứng dụng
app = App(root)

# Chạy ứng dụng
root.mainloop()
