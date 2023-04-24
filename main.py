from tkinter import *
from tkinter.font import Font
from tkinter import ttk
import os
from handleYoutube import *
from tkinter import filedialog

def handleDownload():
    url = entryUrl.get()
    rs = is_valid_youtube_link(url)
    if rs == 3:
        videos = getAllVideoFromPlaylist(url)
        for video in videos:
            my_data.append([video])
            my_list.append([
                Label(frameTable, textvariable=my_data[len(my_data-1)][0], anchor="w", bg='#F9FAFC', fg="#121212", height="2",width=width[cell],padx=0,pady=0,bd=0,font=("Arial", 14, "normal"))
            ])
                
        rerender()
    if rs == 1:
        size = getSize(url)
        my_list.append([url, size])
        rerender()
    print(my_list)
    print("[LOG] valid link:", rs)

def handleChooseLocation(index):
    filename = filedialog.askdirectory()
    print(filename, index)

def rerender():
    for row in range(0, len(my_list)):
        for cell in range(0, len(my_list[0])):
            my_list[row][cell].grid(row=row + 1, column=cell, padx=0, pady=0)
 
font_path = "./Darker_Grotesque/DarkerGrotesque-Bold.ttf"
abs_font_path = os.path.abspath(font_path)
 

root = Tk()
root.configure(bg='#F9FAFC')
root.geometry("900x500")

frameInput = Frame(root)
frameInput.configure(width=900, height=100)

labelUrl = Label(frameInput, padx=0, pady=0, text="URL: ", anchor="w", bg='#F9FAFC', fg="#121212", font=("Arial", 14, "bold"))
entryUrl = Entry(frameInput, font=('Arial',14,'normal'), bg='#F9FAFC', fg="#121212", bd=0, width=30)
buttonUrl = Button(frameInput, text='Download', bg='#F9FAFC', fg="#121212", bd=0, command=handleDownload)
labelUrl.grid(row=0, column=0)
entryUrl.grid(row=0, column=1)
buttonUrl.grid(row=0, column=2)

frameTable = Frame(root)
frameTable.configure(width=800, height=400, bg='#F9FAFC')

width = [30, 10, 10, 15, 20, 10]

headerName = Label(frameTable, padx=0, pady=0, width="30", height="2", text="Url", anchor="w", bg='#F9FAFC', fg="#121212", font=("Arial", 14, "bold"))
headerSize = Label(frameTable, padx=0, pady=0, text="Size", width="10", height="2", bg='#F9FAFC', fg="#121212", font=("Arial", 14, "bold"))
headerStatus = Label(frameTable, padx=0, pady=0, text="Status", width="10", height="2", bg='#F9FAFC', fg="#121212", font=("Arial", 14, "bold"))
headerTimeLeft = Label(frameTable, padx=0, pady=0, text="Time Left", width="15", height="2", bg='#F9FAFC', fg="#121212", font=("Arial", 14, "bold"))
headerTime = Label(frameTable, padx=0, pady=0, text="Location", height="2", width="20", bg='#F9FAFC', fg="#121212", font=("Arial", 14, "bold"))
headerFile = Label(frameTable, padx=0, pady=0, text="Action", height="2", bg='#F9FAFC', fg="#121212", font=("Arial", 14, "bold"))

headerName.grid(row=0, column=0)
headerSize.grid(row=0, column=1)
headerStatus.grid(row=0, column=2)
headerTimeLeft.grid(row=0, column=3)
headerTime.grid(row=0, column=4)
headerFile.grid(row=0, column=5)

# resolutions = getAllResolution("https://www.youtube.com/watch?v=pMQ2b8Y0Qrw&list=RDpMQ2b8Y0Qrw&start_radio=1")
# videos = getAllVideoFromPlaylist("https://www.youtube.com/playlist?list=PL6gx4Cwl9DGCkg2uj3PxUWhMDuTw3VKjM")

my_list = [
    ["https://www.youtube.com/watch?v=pMQ2b8Y0Qrw&list=RDpMQ2b8Y0Qrw&start_radio=1",
     "26.405",
     "Done",
     "",
     "/user/test",
     ""
    ],
    ["https://www.youtube.com/watch?v=pMQ2b8Y0Qrw&list=RDpMQ2b8Y0Qrw&start_radio=1",
     "10.702",
     "",
     "",
     "/user/test",
     ""
    ],
    ["https://www.youtube.com/watch?v=pMQ2b8Y0Qrw&list=RDpMQ2b8Y0Qrw&start_radio=1",
     "2.5",
     "Done",
     "",
     "/user/test",
     ""
    ],
    ["https://www.youtube.com/watch?v=pMQ2b8Y0Qrw&list=RDpMQ2b8Y0Qrw&start_radio=1",
     "8.2",
     "",
     "",
     "/user/test",
     ""
    ],
    ["https://www.youtube.com/watch?v=pMQ2b8Y0Qrw&list=RDpMQ2b8Y0Qrw&start_radio=1",
     "9.5782",
     "Done",
     "",
     "/user/test",
     ""
    ]
]
my_data = []

# for video in videos:
#     my_list.append([video, '', '', '', '', ''])

for row in range(0, len(my_list)):
    for cell in range(0, len(my_list[0])):
        print(cell)
        if cell == 5:
            buttonCell = Button(frameTable, text='Choose...', bg='#F9FAFC', fg="#121212", bd=0)
            buttonCell.grid(row=row + 1, column=cell, padx=0, pady=0)
        else:
            labelCell = Label(frameTable, 
                text=my_list[row][cell], 
                anchor="w", 
                bg='#F9FAFC', 
                fg="#121212", 
                height="2",
                width=width[cell],
                padx=0,
                pady=0,
                bd=0,
                font=("Arial", 14, "normal"))
            labelCell.grid(row=row + 1, column=cell, padx=0, pady=0)
            # separator = ttk.Separator(orient="horizontal")
            # separator.place(in_=labelCell, x=0, rely=1.0, height=1, relwidth=1.0)

frameTable.grid_columnconfigure(0)
frameTable.grid_rowconfigure(0)
frameInput.grid(row=0, column=0)
frameTable.grid(row=1, column=0)
# t = Table(root)
root.mainloop()