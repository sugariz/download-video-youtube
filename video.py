import tkinter as tk
import json

class Video:
    def __init__(self, name, url, size, status, timeLeft, date, video, mp3, time, root, reRenderTable, y2m, location, resolution, btnDownload):
        self.root = root
        self.reRenderTable = reRenderTable
        self.name = name
        self.url = url
        self.size = size
        self.status = Status(status)
        self.timeLeft = timeLeft
        self.date = date
        self.video = video
        self.mp3 = mp3
        self.time = time
        self.resolution = resolution
        self.btnDownload = btnDownload
        self.menuRes = None
        self.setDefaultValue()
        self.menuResolution()
        self.y2m = y2m
        self.location = location
    def setLocation(self, newLocation): self.location = newLocation
    def getLocation(self): return self.location
    def getBtnDownload(self): return self.btnDownload
    def getY2m(self): return self.y2m
    def getStringVideo(self): return json.dumps(self.video)
    def setDefaultValue(self):
        if self.resolution == '':
            self.resolution = self.video[0]['resolution']
        if self.size == '':
            self.size = self.video[0]['fileSize']
        if self.btnDownload == '':
            self.btnDownload = self.video[0]['download']
    def setValue(self, position):
        self.resolution = self.video[position]["resolution"]
        self.size = self.video[position]["fileSize"]
        self.btnDownload = self.video[position]["download"]
        self.reRenderTable()
    def getMenuRes(self): return self.menuRes
    def menuResolution(self):
        self.menuRes = tk.Menu(self.root, tearoff=False)
        for idx, v in enumerate(self.video):
            if v["resolution"] != None:
                self.menuRes.add_command(label=v["resolution"], 
                                         command=lambda idx=idx: self.setValue(idx))
    def getName(self): return self.name
    def getUrl(self): return self.url
    def getSize(self): return self.size
    def getStatus(self): return self.status.getStatus()
    def getTimeLeft(self): return self.timeLeft
    def getDate(self): return self.date
    def setName(self, name): self.name = name
    def setUrl(self, url): self.url = url
    def setSize(self, size): self.size = size
    def setStatus(self, status): self.status.setStatus(status)
    def setTimeLeft(self, timeLeft): self.timeLeft = timeLeft
    def setTimeDate(self, date): self.date = date
    def getVideo(self): return self.video
    def getSigleResolution(self): return self.resolution
    def getResolution(self):
        resolution = []
        for row in self.video:
            resolution.append(row['resolution'])
        return resolution
    def getFileSize(self, resolution):
        for row in self.video:
            if resolution == row['resolution']: return row['fileSize']
    def getButtonDownload(self, resolution):
        for row in self.video:
            if resolution == row['resolution']: return row['download']
    def getSetVideo(self):
        return (
            self.name,
            self.resolution,
            self.url,
            self.size,
            self.time,
            self.status.getStatus(),
            self.timeLeft,
            self.date,
            self.mp3,
        )
    def extractAttribute(self):
        return {
            "name": self.name,
            "url": self.url,
            "size": self.size,
            "status": self.status.getValue(),
            "timeLeft": self.timeLeft,
            "date": self.date,
            "video": self.getStringVideo(),
            "mp3": [],
            "time": self.time,
            "resolution": self.resolution,
            "btnDownload": self.btnDownload,
            "menuRes": None,
            "y2m": self.y2m,
            "location": self.location
        }
    def getIndexResolutionVideo(self):
        for idx, vi in enumerate(self.video):
            if vi['resolution'] == self.resolution:
                return idx

class Status:
    def __init__(self, status) -> None:
        self.status = status
        # 0 -> Chưa tải
        # 1 -> Đã tải
        # 2 -> Đang tải
        # -1 -> Lỗi
    def getStatus(self):
        if self.status == 0: return "Ready"
        if self.status == 1: return "Success"
        if self.status == 0: return "Failure"
    def getValue(self): return self.status

    def setStatus(self, newStatus): self.status = newStatus
