import yt_dlp
from downloader.convert import convert
from os import listdir

def download_video(link):
    ydl_opts = {
        'format': 'bestvideo + bestaudio/best',
        'outtmlp': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("descarga completa")
        archivos = listdir()
        filtro = [archivo for archivo in archivos if archivo.endswith("mp4")]
        return filtro[0]


    except Exception as e:
        print("hubo problemas {e}")

def download_audio(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmlp': '%(title)s.%(ext)s',
        'merge_output_format': 'mp3'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            #print(ydl.params)
            info = ydl.extract_info(link, download=False)
            title = info.get("title", None)
        
        convert()

        print("descarga completa")

    except yt_dlp.DownloadError as e:
        print("hubo problemas {e}")


if __name__ == "__main__":
    link = str(input("Pon la url del video: ")).strip()
    download_video(link=link)