#coding: utf-8
'''
Created on 22 feb 2022

@author: Servando
'''
#ficheros binarios, de imágenes y directorios
#de los sistemas informáticos críticos y las aplicaciones de la organización y dar cuenta
#mensualmente
import hashlib
from msilib.schema import Directory
import os
import datetime
import logging
import tkinter as tk
import threading
from threading import Thread
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
from pick import pick
import webbrowser
import re

    
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
now = datetime.datetime.now().strftime("%Y-%m-\d %H:%M:%S")
interval = 0
running = bool()
window = tk.Tk()
logBox = ScrolledText(window, width=80, height=20)
contadorDeDias = 0
contadorDeMes = 0
numberFilesOkMensual = 0
numberFilesModifiedMensual = 0


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


def importarConfiguracion():
     
    path = "config.config"
    if (os.path.exists(path)):
        try:
            with open(path, "r") as config:
                for line in config:
                    if "#" not in line:
                        confSplitted = line.split("=")
                        configDict[confSplitted[0].strip(
                        )] = confSplitted[1].strip()

            logging.info("La configuración ha sido importada con éxito")

        except:
            logging.error("Se ha producido un error al importar la configuracion")
    else:
        configs = ["\nSelected Hash mode=\n",
                   "Directories to protect=\n", "Verify interval=\n"]
        try:
            with open("config.config", "w") as file:
                file.write(
                    "# Agregar los directorios a proteger, separados por una coma\n# Intervalo de tiempo entre examenes en segundos\n# Guardar la configuracion antes de iniciar el examen \n# Los Hash que soportan son: sha3_256, sha3_384, sha3_512 o md5\n# Las rutas de los archivos deben empezaro por 'C:\\' ")
                for config in configs:
                    file.write(config)
            logging.info("El archivo de configuración ha sido generado con éxito")

        except:
            logging.error(
                "Se ha porudcido un error al crear el archivo de configuracion")
        menu()
        
def configurarSistema():
    path = "config.config"
    if (os.path.exists(path)):
        webbrowser.open_new("config.config")
    else:
        configs = ["\nSelected Hash mode=\n",
                   "Directories to protect=\n", "Verify interval=\n"]
        try:
            with open("config.config", "w") as file:
                file.write(
                    "# Agregar los directorios a proteger, separados por una coma\n# Intervalo de tiempo entre examenes en minutos\n# Guardar la configuracion antes de iniciar el examen \n# Los Hash que soportan son: sha3_256, sha3_384, sha3_512 o md5\n# Para el directorio a proteger debe empezar con 'C:\\'")
                for config in configs:
                    file.write(config)
            logging.info("El archivo de configuración ha sido generado con éxito")
            webbrowser.open_new("config.config")
        except:
            logging.error(
                "Se ha porudcido un error al crear el archivo de configuracion")
        
        
def hashearCarpeta(pathName):
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
        logging.info("Los hashes han sido guardados con éxito")

    except:
        logging.error("Se ha producido un error al exportar los hashes")
    
    end = datetime.datetime.now() - begin_time
    strr = "Hashes exportados correctamente en: " + str(end)
    logging.info(strr)
    
    
def comparaHashes():
    global contadorDeDias
    contadorDeDias += 1
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
    global numberFilesOkMensual
    global numberFilesModifiedMensual
    numberFilesOkMensual += numberOfFilesOK
    numberFilesModifiedMensual += numberOfFilesNoOk
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
    if(contadorDeDias==31):
        global contadorDeMes
        contadorDeMes += 1
        porcentaje = (numberFilesModifiedMensual/(numberFilesModifiedMensual+numberFilesOkMensual))*100
        path = "reporteMensual"+str(contadorDeMes)+".txt"
        with open(path, "w") as reporte:
            reporte.write("\nNumero de ficheros sin modificar en el mes: " +str(numberFilesOkMensual))
            reporte.write("\nNumero de ficheros modificados en el mes: " +str(numberFilesModifiedMensual))
            reporte.write("\nPorcentaje de integridad comprometida en el mes: " +str(porcentaje))
        logging.info("Se ha generado un reporte mensual nuevo!")


def interfazTkinterHandle():
    t = Thread(target=interfazTkinter)
    t.start()
    
def runHandle():
    t = Thread(target=run)
    global running
    running = True
    t.start()
    interfazTkinter()
    
    
def run():
    if running:
        begin_time = datetime.datetime.now()
        pathName = configDict["Directories to protect"]
        global newFilesAndHashes
        newFilesAndHashes = hashearCarpeta(pathName)
        comparaHashes()
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
<<<<<<< HEAD
                            datefmt='\d/%m/%Y %H:%M:%S', filename=filename, level=logging.INFO)
    importConfig()
=======
                            datefmt='%d/%m/%Y %H:%M:%S', filename=filename, level=logging.INFO)
    importarConfiguracion()
>>>>>>> siadan
    crearHashes()
    
def crearHashes():
    pathName = configDict["Directories to protect"]
    global filesAndHashes
    filesAndHashes = hashearCarpeta(pathName)
    exportarHashesADocumento(filesAndHashes)
    
def detenerExamen():
    global running
    running = False
    run()
    
    
def leeLog():
    text = str()
    if (os.path.exists('log.log')):
        with open(os.path.join('log.log')) as reader:
            text = reader.read()
    else:
        f = open(os.path.join('log.log'), "x")
    return text


def logBoxContainer():
    logBox.delete("1.0", tk.END)
    text = leeLog()
    logBox.insert(tk.INSERT, text)
    logBox.insert(tk.END, "")
    
def interfazTkinter():
    window.resizable(0, 0)
    window.geometry("512x512")
    labelLog = tk.Label(window, text="Fichero de LOG")
    labelLog.pack()
    window.title("HIDS")
    logBox.pack()
    window.mainloop()
        
        
def menu():
    title = logo
    options = ['Configurar sistema HIDS', 'Importar configuracion', 'Empezar Examen',
                'Detener Examen', 'Ver Logs', 'Cerrar']
    option, index = pick(options, title, indicator='=>', default_index=0)
    
    if option == 'Configurar sistema HIDS':
        configurarSistema()        
    elif option == 'Importar configuracion':
        importarConfigYHashes()
        generarFicheros()
    elif option == 'Empezar Examen':
        importarConfigYHashes()
        runHandle()
    elif option == 'Detener Examen':
        detenerExamen()
    elif option == 'Ver Logs':
        path = "log.log"
        if (os.path.exists(path)):
            webbrowser.open_new("log.log")
    elif option == 'Cerrar':
        os.system(quit())
    
    menu()

<<<<<<< HEAD
def guardar(fichero):
    log_start = "^\w+:\d\d\/\d\d\/\d\d\d\d \d\d:\d\d:\d\d: "
    ok_check_text = "Comprobacion realizada con exito en: "
    ok_files_text = "Numero de archivos OK: "
    changed_check_text = "Archivos con integridad comprometida: "
    changed_files_text = "Numero de archivos MODIFICADOS: "
    dir = "DIR: "


    with open(fichero, "r") as log:
        #ok_files = re.findall(log_start + ok_files_text + "\d+$", log)
        #ok_files = re.findall(pattern="^\w+:\d+\/\d+\/\d+ \d+:\d+:\d+: Numero de archivos OK: \d$", string=log)
        #print(ok_files)
        #changed_files = re.findall(log_start + changed_files_text + "\d$")
        #changed_check = re.findall(log_start + changed_check_text)
        lista_ok = []
        lista_failed = []
        lista_dir = []
        for linea in log:
            if ok_files_text in linea or changed_files_text in linea:
                split = linea.split(":")
                tipo_log = split[0]
                fecha = split[1].split(" ")[0]
                horas = split[1].split(" ")[1]
                minutos = split[2]
                segundos = split[3]
                mensaje = split[4][1:]
                numero = int(split[5][1:-1])
                if ok_files_text in linea:
                    lista_ok.append(numero)
                    
                else:
                    lista_failed.append(numero)
            elif changed_files_text in linea:
                pass
            elif dir in linea:
                split = linea.split(dir)
                lista_dir.append(split[1])

        print(lista_ok)
        print(lista_failed)

            


'''def iniciar():
    
    filename = "log.log"
    logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s',
                        datefmt='\d/%m/%Y %H:%M:%S', filename=filename, level=logging.INFO)
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
    guardar("log.log")
    #menu()
    #iniciar()
    #print(os.path.abspath('.').split(os.path.sep)[0]+os.path.sep+"top_secret\log.log")
=======

if __name__ == "__main__":
    menu()
>>>>>>> siadan
