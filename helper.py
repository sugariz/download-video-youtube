from urllib.parse import urlparse, parse_qs
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import requests
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

def isValidYoutubeLink(link):
    """
    Kiểm tra tính hợp lệ của liên kết YouTube.
    Trả về True nếu liên kết hợp lệ, ngược lại trả về False.
    """
    try:
        # Lấy ID video từ liên kết
        query = urlparse(link)
        if query.hostname == 'youtu.be':  # Nếu link là dạng short link
            video_id = query.path[1:]
            if len(video_id) == 0: return 0
        elif query.hostname in ('www.youtube.com', 'youtube.com'):  # Nếu link là dạng full link
            if query.path == '/watch':  # Nếu link là trang xem video
                video_id = parse_qs(query.query)['v'][0]
                return 1
            elif query.path[:7] == '/embed/':  # Nếu link là dạng embedded
                video_id = query.path.split('/')[2]
                return 2
            elif query.path == "/playlist":
                video_id = ""
                return 3
            elif query.path[:8] == '/shorts/':  # Nếu link là trang shorts
                return 4
            else:
                return 0
        else:
            return 0

        return 11
    except:
        return 0


def getInfoVideo(url, driver, type, onSubmit):
    urlDownload = ""
    if (type == 1): urlDownload = url.replace("youtube.com", "youtubezz.com")
    if (type == 11): urlDownload = url.replace("youtu.be", "y2meta.com/vi/youtube")
    if (type == 4): urlDownload = url.replace("youtube.com/shorts", "y2meta.com/vi/youtube")
    if (type == 9): urlDownload = url
    if urlDownload == "": return
    try:
        driver.get(urlDownload)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "moretab")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result = {
            "title": None,
            "time": None,
            "url": url,
            "y2m": urlDownload,
            "video": [],
            "mp3": [],
        }
        infoArea = soup.find('tbody', {'id': 'moretab'})
        captionArea = soup.find('div', {'class': 'caption text-left'})
        if infoArea == None or captionArea == None: return result
        rowInfo = infoArea.find_all('tr')
        captionBold = captionArea.find('b')
        captionParaph = captionArea.find('p')
        if len(rowInfo) == 0 or captionBold == None or captionParaph == None: return result
        result["title"] = captionBold.text.strip()
        result["time"] = captionParaph.text.replace("Thời lượng:  ", "").strip()
        result["time"] = captionParaph.text.replace("Duration:  ", "").strip()
        dataVideo = []
        index = 1
        for info in rowInfo:
            cellInfo = info.find_all('td')
            if (len(cellInfo) == 3):
                realInfo = {
                    "resolution": None,
                    "fileSize": None,
                    "download": None,
                }
                resolution = cellInfo[0].text
                fileSize = cellInfo[1].text
                buttonDownload = '//*[@id="moretab"]/tr[{}]/td[3]/button'.format(index)
                if (resolution != None):
                    realInfo["resolution"] = " ".join(cellInfo[0].text.split())
                if (fileSize != None):
                    realInfo["fileSize"] = " ".join(cellInfo[1].text.split())
                if (buttonDownload != None):
                    realInfo["download"] = buttonDownload
                dataVideo.append(realInfo)
            index += 1
        result["video"] = dataVideo
        if (onSubmit != None): onSubmit(result)
        return result
    except TimeoutException as q:
        print(q)
        return False

def getListFromPlaylist(url, driver):
    rs = []
    urlDownload = url.replace("youtube.com", "youtubezz.com")
    driver.get(urlDownload)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "search-result")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    infoThumnails = soup.find_all('div', {'class': 'thumbnail'})
    for thumnail in infoThumnails:
        rs.append(thumnail.a['href'])

    return rs

def DLN(url, driver, button):
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "moretab")))
    result = ""
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, button))
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-download-link')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        dlArea = soup.find('a', {'class': 'btn-download-link'})
        result = dlArea['href']
        return result
    except TimeoutException as q:
        print(q)
        return None

def DownloadVideo(url, driver, button, title, resolution, path=None):
    # infoVideo = getInfoVideo(url, driver, 9, None)
    rs = DLN(url, driver,button)
    file_name = re.sub(r'[^\w\-\.]', '_', title)
    if rs == None: return False
    finalPath = ""
    if path == "" or path == None:
        finalPath = file_name + "({})".format(resolution) + ".mp4"
    else:
        finalPath = path + "/" + file_name + "({})".format(resolution) + ".mp4"
    saveFile(rs, finalPath)
    return finalPath

def saveFile(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
