'''
Created on 24 feb 2022

@author: Servando
'''
import os
import logging

if __name__ == '__main__':
    filename = os.path.abspath('.').split(os.path.sep)[
        0]+os.path.sep+"top_secret\log.log"
    logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S', filename=filename, level=logging.INFO)
    print(filename)