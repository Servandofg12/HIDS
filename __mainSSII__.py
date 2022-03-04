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
from pick import pick
import webbrowser
import pathlib

    
logo = """
   █████   █████ █████ ██████████    █████████ 
░░███   ░░███ ░░███ ░░███░░░░███  ███░░░░░███
 ░███    ░███  ░███  ░███   ░░███░███    ░░░ 
 ░███████████  ░███  ░███    ░███░░█████████ 
 ░███░░░░░███  ░███  ░███    ░███ ░░░░░░░░███
 ░███    ░███  ░███  ░███    ███  ███    ░███
 █████   █████ █████ ██████████  ░░█████████ 
░░░░░   ░░░░░ ░░░░░ ░░░░░░░░░░    ░░░░░░░░░  
                                             
                                   in Python                   
                       """

    
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
window = tk.Tk()
logBox = ScrolledText(window, width=80, height=20)
toaster = ToastNotifier()


def generarFicheros():
    generarFicherosBin()
    generarFicherosTxt()

def generarFicherosBin():
    global configDict 
    path = Path(configDict["Directories to protect"])
    try:
        Path(configDict["Directories to protect"]+"\FicherosBIN").mkdir(parents=True)
    except:
        pass
    count = 0
    for i in range(1, 101):
        nameFile = "EjemploBin " + str(i) +".bin"
        path = Path((configDict["Directories to protect"]+"\FicherosBIN") + os.path.sep + nameFile)
        try:
            with open(path, "w") as file:
                file.write("Esto es un ejemplo de fichero bin (" + str(i) + ").")
        except:
            logging.info("Se ha producido un error a la hora de crear ficheros. :(")
        count += 1
    logging.info("Creados " + str(count) + " ficheros BIN correctamente.")

def generarFicherosTxt():
    global configDict 
    path = Path(configDict["Directories to protect"])
    try:
        Path(configDict["Directories to protect"]+"\FicherosTXT").mkdir(parents=True)
    except:
        pass
    count = 0
    for i in range(1, 101):
        nameFile = "EjemploTxt " + str(i) +".txt"
        path = Path((configDict["Directories to protect"]+"\FicherosTXT") + os.path.sep + nameFile)
        try:
            with open(path, "w") as file:
                file.write("Esto es un ejemplo de fichero txt (" + str(i) + ").")
        except:
            logging.info("Se ha producido un error a la hora de crear ficheros. :(")
        count += 1
    logging.info("Creados " + str(count) + " ficheros TXT correctamente.")


def importConfig():
     
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
        menu()
        
        
def folderHash(pathName):
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


    

def guiHandle():
    t = Thread(target=gui)
    t.start()
    
def runHandle():
    t = Thread(target=run)
    global running
    running = True
    t.start()
    gui()
    
    
def run():
    if running:
        begin_time = datetime.datetime.now()
        pathName = configDict["Directories to protect"]
        global newFilesAndHashes
        newFilesAndHashes = folderHash(pathName)
        compareHashes()
        logBox.config(state=tk.NORMAL)
        logBoxContainer()  # AQUI EL LOG BOX
        logBox.config(state=tk.DISABLED)
        interval = configDict["Verify interval"]
        threading.Timer(float(interval), run).start()
        end = datetime.datetime.now() - begin_time
        strr = "Comprobacion realizada con exito en: " + str(end)
        logging.info(strr)
    else:
        logging.critical("EXAMEN INTERRUMPIDO")
        

def importarConfigYHashes():        
    filename = "log.log"
    logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S', filename=filename, level=logging.INFO)
    importConfig()
    crearHashes()
    
def crearHashes():
    pathName = configDict["Directories to protect"]
    global filesAndHashes
    filesAndHashes = folderHash(pathName)
    exportarHashesADocumento(filesAndHashes)
    
def detenerExamen():
    toaster.show_toast(
        "HIDS", "Servicio interrumpido. El sistema NO esta examinando los directorios.", threaded=True)
    global running
    running = False
    run()
    
    
def readLogFile():
    text = str()
    if (os.path.exists('log.log')):
        with open(os.path.join('log.log')) as reader:
            text = reader.read()
    else:
        f = open(os.path.join('log.log'), "x")
    return text


def logBoxContainer():
    logBox.delete("1.0", tk.END)
    text = readLogFile()
    logBox.insert(tk.INSERT, text)
    logBox.insert(tk.END, "")
    
def gui():
    window.resizable(0, 0)
    window.geometry("512x512")
    labelLog = tk.Label(window, text="Fichero de LOG")
    labelLog.pack()
    window.title("HIDS")
    logBox.pack()
    window.mainloop()
        
        
def menu():
    title = logo
    options = ['Importar configuracion', 'Empezar Examen', 'Detener Examen', 'Ver Logs', 'Cerrar']
    option, index = pick(options, title, indicator='=>', default_index=0)
    
    if option == 'Importar configuracion':
        importarConfigYHashes()
        generarFicheros()
    elif option == 'Empezar Examen':
        importarConfigYHashes()
        runHandle()
    elif option == 'Detener Examen':
        detenerExamen()
    elif option == 'Ver Logs':
        webbrowser.open_new("log.log")
    elif option == 'Cerrar':
        os.system(quit())
    
    menu()

'''def iniciar():
    
    filename = "log.log"
    logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S', filename=filename, level=logging.INFO)
    importConfig()
    #Una vez importada la configuración debemos calcular los hashes de los docs:
    global configDict
    pathName = configDict["Directories to protect"]
    global filesAndHashes
    filesAndHashes = folderHash(pathName)
    #print(filesAndHashes)
    exportarHashesADocumento(filesAndHashes)
    runHandle()
    run()
    #gui()'''


if __name__ == "__main__":
    #print(os.path.exists("C:\\Users\Servando\Desktop\Carpeta de Ejemplo"))
    '''path = "C:\\Users\Servando\Desktop\Carpeta de Ejemplo\Ejemplo 2"
    with open(path, "w") as file:
                file.write("Esto es un ejemplo de fichero")'''
    menu()
    #iniciar()
    #print(os.path.abspath('.').split(os.path.sep)[0]+os.path.sep+"top_secret\log.log")
