from pytube import YouTube
from urllib.parse import urlparse, parse_qs
from pytube import Playlist
import re
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

def is_valid_youtube_link(link):
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
            else:
                return 0
        else:
            return 0

        # Kiểm tra tính hợp lệ của ID video bằng cách tải thông tin của video
        # YouTube('https://www.youtube.com/watch?v=' + video_id).streams.first().download()
        return 1
    except:
        return 0

def downloadVideo(url, path, resolution):
    try:
        yt = YouTube(url)
        video = yt.streams.get_by_resolution(resolution)
        # video.download(path)
        print(video.filesize)
        return True
    except Exception as e:
        print(e)
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            print(video.filesize_mb)
            return True
        except Exception as ee:
            print(ee)
        return False

def getSize(url, resolution=""):
    try:
        yt = YouTube(url)
        if resolution == "":
            video = yt.streams.get_highest_resolution()
            return video.filesize_mb
        print("[DEBUG]", resolution, "dont run this line")
        video = yt.streams.get_by_resolution(resolution)
        return video.filesize_mb
    except Exception as e:
        print(e)
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            return video.filesize_mb
        except Exception as ee:
            print(ee)
        return 0

def getAllResolution(url):
    resolutions = []
    try:
        yt = YouTube(url)
        for i in yt.streams: 
            resolutions.append(str(i.resolution))
        resolutions = list(set(resolutions))
        print(resolutions)
        return resolutions
    except Exception as e:
        print(e)
        print(resolutions)
        return resolutions
    
# def getAllNameFromPlaylist(url):
#     name = []
#     try:

#         for video in play_list.videos:
#             name = video.title
#             print(name)
#     except Exception as e:
#         print(e)

def getAllVideoFromPlaylist(url):
    try:
        playlist = Playlist(url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        # names = playlist.videos
        urls = playlist.video_urls
        # rs = []
        # for video, url in zip(urls, urls):
        #     rs.append({
        #         # "title": video.title,
        #         "url": url
        #     })
        return urls
    except Exception as e:
        print(e)
        return False

# videos = getAllVideoFromPlaylist("https://www.youtube.com/playlist?list=PL6gx4Cwl9DGCkg2uj3PxUWhMDuTw3VKjM")
# print(videos)
# getAllResolution("https://www.youtube.com/watch?v=pMQ2b8Y0Qrw&list=RDpMQ2b8Y0Qrw&start_radio=1")
# downloadVideo('https://www.youtube.com/watch?v=pMQ2b8Y0Qrw&list=RDpMQ2b8Y0Qrw&start_radio=1', '.', '144p')