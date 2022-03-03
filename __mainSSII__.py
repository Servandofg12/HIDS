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
import keyboard
from pick import pick





#def run():
    #readLogFile()
    #filename = os.path.abspath('.').split(os.path.sep)[
    #    0]+os.path.sep+"top_secret\log.log"
    #logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s',
    #                    datefmt='%m/%d/%Y %H:%M:%S', filename=filename, level=logging.INFO)
    #importConfig()
    #gui()
    
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

#print(logo)
def vacio():
    pass

def menu():
    title = logo
    options = ['Inicializar', 'Crear Hashes', 'Empezar Examen', 'Detener Examen', 'Ver Logs']
    option, index = pick(options, title, indicator='=>', default_index=1)
    if option == 'Inicializar':
        vacio()
    elif option == 'Crear Hashes':
        vacio()
    elif option == 'Empezar Examen':
        vacio()
    elif option == 'Detener Examen':
        vacio()
    elif option == 'Ver Logs':
        vacio()

# This is the main boilerplate of the program, where the functions are called.
if __name__ == "__main__":
    menu()
    