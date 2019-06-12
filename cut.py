# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 08:15:04 2019

@author: Deer
"""

from tkinter.filedialog import askdirectory
from PIL import Image
import os
import os.path

print('Please input the floder with all raw pictures...')
Dpath = askdirectory()
files = os.listdir(Dpath)
Dresult = Dpath + '/Result'

print('The Code is working, please witing..')
for file in files:
    if '.jpg' in file:
        pic_path = Dpath + '/' + file
        Raw_img = Image.open(pic_path)
        QR_img = Raw_img.crop((100,510,860,940))
        QR_dir = Dresult + '/' + file + 'cut' + '.jpg'
        QR_img.save(QR_dir)
        
print('Finish')       
        
