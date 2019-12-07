# -*- coding: latin-1 -*-

import os
import time
import re
import shutil
import subprocess
import sys
import configparser


def removeEmptyFolders(path):
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                removeEmptyFolders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and not any(path in s for s in rutas):
        print("[" + time.ctime() + "] Removing empty folder:" + path)
        os.rmdir(path)


def borrarDirsVacios():
    for path in rutas:
        removeEmptyFolders(path)


def comprobarRuta(directorio):
    if not os.path.exists(directorio):
        os.makedirs(directorio)


# INICIO MAIN
if __name__ == '__main__':

    # print "["+ time.ctime() + "] renombrar.py started"
    config = configparser.ConfigParser()
    config.readfp(open('conf_rename.ini'))

    rutaOriginal = config.get('DIRS', 'downloadBase')+config.get('DIRS', 'rutaOriginal')
    rutaPeliculas = config.get('DIRS', 'downloadBase')+config.get('DIRS', 'rutaPeliculas')

    # TODO: recorrer todas las rutas que se carguen, no declararlas "a pelo"
    rutas = [rutaOriginal, rutaPeliculas]
    extensiones = ["avi", "mp4", "mkv", "vob", "mpg", "iso"]

    comprobarRuta(rutaOriginal)
    comprobarRuta(rutaPeliculas)

    # nos desplazamos a la ruta de descargas
    os.chdir(rutaOriginal)

    # exploramos recursivamente
    for root, dirs, files in os.walk(rutaOriginal):
        # print (os.path.join(root,fichero).strip(path))
        print(("[" + time.ctime() + "] Ficheros leidos = "+str(len(files))))
        for fichero in files:
            # Comprobamos que sea un fichero grande
            if (os.path.getsize(os.path.join(root, fichero)))/(1024*1024.0) > 60:
                # si es un fichero de las extensiones definidas previamente
                if any(fichero[-3:].lower() in s for s in extensiones):
                    # print ("FICHERO VIDEO LEIDO: " + fichero)
                    # comprobamos si es una serie (SXXEXX o XXxXX)
                    if re.search(r"([sS])(\d+)([eE]|EP|ep)(\d+)", fichero) != None or re.search(r"(\d+)x(\d+)", fichero) != None:
                        print("[" + time.ctime() + "] Serie detectada y dejada para tvnamer= "+fichero)
                    # si es una pelicula
                    else:
                        shutil.move(os.path.join(root, fichero),
                                    os.path.join(rutaPeliculas, fichero))
                        print("[" + time.ctime() + "] Pelicula Movida= "+os.path.join(root, fichero))
                else:
                    # fichero no video grande
                    print("[" + time.ctime() + "] Archivo grande no video . Dejado en carpeta =" +
                          re.escape(os.path.join(root, fichero)))
            else:
                # fichero pequeño comprobar srt
                if (os.path.splitext(fichero)[1] == '.srt'):
                    shutil.move(os.path.join(root, fichero), os.path.join(rutaPeliculas, fichero))
                    print("[" + time.ctime() + "] Archivo de subs original. Movido =" +
                          os.path.join(root, fichero))
                else:
                    subprocess.check_call(
                        'rm ' + re.escape(os.path.join(root, fichero)), shell=True)
                    print("[" + time.ctime() + "] Archivo DESCARTADO y borrado= " + re.escape(fichero))
    # print("Terminado el bucle de ficheros")
    borrarDirsVacios()  # ojo esta llamada depende de la variable global rutas
    sys.exit()
