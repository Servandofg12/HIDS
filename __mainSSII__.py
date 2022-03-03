#coding: utf-8
'''
Created on 22 feb 2022

@author: Servando
'''
#ficheros binarios, de imágenes y directorios
#de los sistemas informáticos críticos y las aplicaciones de la organización y dar cuenta
#mensualmente
import hashlib
import os
import time
import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import logging
import tkinter as tk
import threading
import sys
from threading import Thread
from tkinter.scrolledtext import ScrolledText
from win10toast import ToastNotifier
import smtplib
from pathlib import Path

# GLOBALS
configDict = dict()
filesAndHashes = dict()
newFilesAndHashes = dict()
badIntegrity = list()
graphDate = list()
cantidadDeArchivos = [0, 1000]
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
interval = 0
running = bool()
toaster = ToastNotifier()


def importConfig():
    """ Params: NONE """
    """ Return: NONE """
    """ Crea un archivo de configuracion si no lo hay con las opciones de la plantilla de 'configs'
    y en caso de que ya exista (que sera siempre menos la primera vez que se ejecute el script)
    carga la configuracion de dicho archivo y la importa al diccionario del script llamado 'configDict',
    mediante este diccionario vamos a poder manejar dichas opciones indicadas en el archivo de configuracion"""
    
    path = "config.config"
    if (os.path.exists(path)):
        try:
            with open(path, "r") as config:
                for line in config:
                    if "#" not in line:
                        confSplitted = line.split("=")
                        configDict[confSplitted[0].strip(
                        )] = confSplitted[1].strip()

            logging.info("La configuracion se ha importado correctamente!")

        except:
            logging.error("Error al importar la configuracion")
    else:
        configs = ["\nSelected Hash mode=\n",
                   "Directories to protect=\n", "Verify interval=\n", "email=\n", "smtpPass=\n", "toEmail=\n"]
        try:
            with open("config.config", "w") as file:
                file.write(
                    "# Agregar los directorios a proteger, separados por una coma\n# Intervalo de tiempo entre examenes en minutos\n# Guardar la configuracion antes de iniciar el examen \n# Los Hash que soportan son: sha3_256, sha3_384, sha3_512 o md5")
                for config in configs:
                    file.write(config)
            logging.info("Archivo de configuracion creado satisfactoriamente!")

        except:
            logging.error(
                "Error al crear el archivo de configuracion, problema con los permisos?")
        importConfig()
        
        
def folderHash(pathName):
    """ Params: ruta """
    """ Return: devuelve un diccionario formato por la ruta y el hash: key=ruta, value=hash """
    """ Se le pasa una ruta y viaja por todos los archivos y las subrutas de dicha ruta y calcula los hashes
    de cada uno de los archivos encontrados """
    fileAndHash = dict()
    for root, dirs, files in os.walk(pathName):
        for file in files:
            with open(os.path.join(root, file), "rb") as fileRaw:
                if(configDict["Selected Hash mode"].lower() == "sha3_256"):
                    fileAndHash[os.path.join(root, file).replace("\\", "/")] = hashlib.sha3_256(
                        fileRaw.read()).hexdigest()
                elif(configDict["Selected Hash mode"].lower() == "sha3_384"):
                    fileAndHash[os.path.join(root, file).replace("\\", "/")] = hashlib.sha3_384(
                        fileRaw.read()).hexdigest()
                elif(configDict["Selected Hash mode"].lower() == "sha3_512"):
                    fileAndHash[os.path.join(root, file).replace("\\", "/")] = hashlib.sha3_512(
                        fileRaw.read()).hexdigest()
                elif(configDict["Selected Hash mode"].lower() == "md5"):
                    fileAndHash[os.path.join(root, file).replace("\\", "/")] = hashlib.md5(
                        fileRaw.read()).hexdigest()
    return fileAndHash


def exportarHashesADocumento(diccionarioDeHashes):
    begin_time = datetime.datetime.now()
    path = "hashes.hash"
    try:
        with open(path, "w") as writer:
            for key, value in diccionarioDeHashes.items():
                writer.write(key + "=" + value + "\n")
        logging.info("Se han guardado los hashes en el archivo hashes.hash correctamente!")

    except:
        logging.error("Error al exportar los hashes al archivo hashes.hash.")
    
    end = datetime.datetime.now() - begin_time
    strr = "Hashes exportados correctamente en: " + str(end)
    logging.info(strr)
    
    
    
def compareHashes():
    """ Params: NONE """
    """ Return: NONE """
    """ Compara los dos diccionarios, uno contiene los hashes cargados del archivo hashes.hash y el otro contiene los hashes recien calculados,
    tras dicha comparacion los resultados saldran por consola """
    numberOfFilesOK = int()
    numberOfFilesNoOk = int()
    listOfNoMatches = list()
    for key, value in filesAndHashes.items():
        if newFilesAndHashes[key] == value:
            numberOfFilesOK += 1
        else:
            numberOfFilesNoOk += 1
            cadena = "DIR: " + str(key) + "Los hashes no coinciden!"
            listOfNoMatches.append(cadena)
    badIntegrity.append(numberOfFilesNoOk)
    #graphDate.append(datetime.datetime.now().strftime("%M"))
    str1 = "Numero de archivos OK: " + str(numberOfFilesOK)
    str2 = "Numero de archivos MODIFICADOS: " + str(numberOfFilesNoOk)
    logging.info(str1)
    logging.info(str2)
    if(listOfNoMatches):
        str3 = "Archivos con integridad comprometida: "
        noMatchesToPrint = list()
        for entry in listOfNoMatches:
            noMatchesToPrint.append("           "+entry)
        logging.warning(str3 + "\n" + '\n'.join(noMatchesToPrint))
        toaster.show_toast(
            "HIDS", "Hay un problema integridad. Revisar LOG.", duration=interval, threaded=True)
    else:
        toaster.show_toast(
            "HIDS", "Examen finalizado. Se mantiene la integridad.", duration=interval, threaded=True)


    
    
def runHandle():
    t = Thread(target=run)
    global running
    running = True
    t.start()
    
    
def run():
    """ Params: NONE """
    """ Return: NONE """
    """  """
    if running == True:
        begin_time = datetime.datetime.now()
        pathName = configDict["Directories to protect"]
        global newFilesAndHashes
        newFilesAndHashes = folderHash(pathName)
        compareHashes()
        interval = configDict["Verify interval"]
        threading.Timer(float(interval), run).start()
        end = datetime.datetime.now() - begin_time
        strr = "Comprobacion realizada con exito en: " + str(end)
        logging.info(strr)
    


def iniciar():
    
    filename = "log.log"
    logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S', filename=filename, level=logging.INFO)
    importConfig()
    #Una vez importada la configuración debemos calcular los hashes de los docs:
    pathName = configDict["Directories to protect"]
    global filesAndHashes
    filesAndHashes = folderHash(pathName)
    #print(filesAndHashes)
    exportarHashesADocumento(filesAndHashes)
    runHandle()
    run()
    #gui()


if __name__ == "__main__":
    iniciar()
    #print(os.path.abspath('.').split(os.path.sep)[0]+os.path.sep+"top_secret\log.log")
