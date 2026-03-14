from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from downloader.downloader import download_video, download_audio
from downloader.validator import url_validator
from fastapi.templating import Jinja2Templates
from os import listdir, remove

app = FastAPI()

templates = Jinja2Templates(directory="templates")


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
    files = listdir()
    file =  [file for file in files if file.endswith(".mp4")]

    if url_validator(link_url):

        if len(file) > 0:
            mark_for_deletion(file)
            cleanup()
            
        download_video(link_url)
        return JSONResponse({'received_data': 'Video preparado'})
    
    else:
        return JSONResponse({"received_data": "Ingrese una url valida"})

@app.post("/api/data/audio")
async def received_aud_data(request: Request):
    link = await request.json()
    link_url = link["name_aud"]

    files = listdir()
    file =  [file for file in files if file.endswith(".opus") or file.endswith(".ogx")]

    if url_validator(link_url):
        if len(file) > 0:
            mark_for_deletion(file)
            cleanup()

        download_audio(link_url)
        return JSONResponse({'received_data': 'Audio preparado'})
    
    else:
        return JSONResponse({'received_data': 'Ingrese una url valida'})

@app.get("/download/video")
async def download_vid():
    files = listdir()
    file =  [file for file in files if file.endswith(".mp4")]
    if len(file) > 0:
        print(file)
        mark_for_deletion(file)
        # try:
        return FileResponse(file[0], filename=file[0])
    
    else:
        return "error"

@app.get("/download/audio")
async def download_audio_yt():
    files = listdir()
    file =  [file for file in files if file.endswith(".opus") or file.endswith("ogx")]
    if len(file) > 0:
        print(file)
        cleanup()
        mark_for_deletion(file)
        return FileResponse(file[0], filename=file[0])
    else:
        return None