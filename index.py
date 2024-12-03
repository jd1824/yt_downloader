from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from downloader.downloader import download_video, download_audio
#from downloader.filtro import eliminar_video
from fastapi.templating import Jinja2Templates
from os import listdir, remove
# import asyncio
# import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore 
import socket
#from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

def mark_for_deletion(filename):
    # Simula una marca para eliminación (en un sistema real, podrías usar una base de datos)
    with open(".delete_list", "a") as f:
        if len(filename) > 0:
            f.write(filename[0] + "\n")

def cleanup():
    with open(".delete_list", "r") as f:
        files_to_delete = f.readlines()
    with open(".delete_list", "w") as f:
        f.truncate(0)  # Vaciar el archivo de marcas
    for file in files_to_delete:
        file = file.strip()
        try:
            remove(file)
        except OSError as e:
            print(f"Error al eliminar el archivo {file}: {e}")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/data/video")
async def received_vid_data(request: Request):
    link = await request.json()
    link_url = link["name"]
    download_video(link_url)
    client_host = request.client.host
    return JSONResponse({'received_data': 'Video preparado', "ip": client_host})

@app.post("/api/data/audio")
async def received_aud_data(request: Request):
    link = await request.json()
    link_url = link["name_aud"]
    download_audio(link_url)
    try:
        return JSONResponse({'received_data': 'Audio preparado'})
    except BaseException:
        return JSONResponse({"received_data": "Ingrese la url"})

@app.get("/redirect/video")
def redirect_video():
    return RedirectResponse(url=f"http://{ip}/download/video", status_code=302)

@app.get("/redirect/audio")
def redirect_audio():
    return RedirectResponse(url=f"http://{ip}/download/audio", status_code=302)

@app.get("/download/video")
async def download_vid():
    #id2 = id.replace(r"https%3A//www.youtube.com/watch%3Fv%3D", "")
    files = listdir()
    file =  [file for file in files if file.endswith(".mp4")]
    if len(file) > 0:
        print(file)
        mark_for_deletion(file)
        # try:
        return FileResponse(file[0], filename=file[0])
    
    else:
        return "Archivo inexistente"
    # finally:
    #     await asyncio.sleep(0)
    #     remove(file[0])

@app.get("/download/audio")
async def download_audio_yt():
    #id2 = id.replace(r"https%3A//www.youtube.com/watch%3Fv%3D", "")
    files = listdir()
    file =  [file for file in files if file.endswith(".mp3")]
    if len(file) > 0:
        print(file)
        mark_for_deletion(file)
        return FileResponse(file[0], filename=file[0])
    else:
        return RedirectResponse("fhttp://{ip}/")
    
@app.on_event("startup")
async def start_scheduler():
    scheduler = AsyncIOScheduler(jobstores={'default': MemoryJobStore()})
    scheduler.add_job(cleanup, 'interval', seconds=30)
    scheduler.start()
