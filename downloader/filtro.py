from os import listdir, remove

def eliminar_video():
    archivos = listdir()
    filtro = [archivo for archivo in archivos if archivo.endswith(".mp4")]

    remove(filtro[0])


def eliminar_audio():
    archivos = listdir()
    filtro = [archivo for archivo in archivos if archivo.endswith(".mp3")]

    remove(filtro[0])