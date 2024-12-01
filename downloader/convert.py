import ffmpeg
from os import listdir, remove

def convert():
    archivos = listdir()
    filtro = [archivo for archivo in archivos if archivo.endswith(".webm")]

    (
        ffmpeg
        .input(filtro[0])
        .output(filtro[0].replace(".webm", ".mp3"))
        .run()
    )

    remove(filtro[0])