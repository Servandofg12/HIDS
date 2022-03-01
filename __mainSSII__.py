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

