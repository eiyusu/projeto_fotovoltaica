import os
import time
import datetime
import shutil
from main_routine import *
import urllib.request
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def connected(host='https://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
    
def upload_files():
    data = datetime.date.today()
    horario = datetime.datetime.now()
    
    if int(horario.strftime('%H')) >=0 and int(horario.strftime('%H')) < 6:
        day_part='1'
    elif int(horario.strftime('%H')) >=6 and int(horario.strftime('%H')) < 12:
        day_part='2'
    elif int(horario.strftime('%H')) >=12 and int(horario.strftime('%H')) < 18:
        day_part='3'
    elif int(horario.strftime('%H')) >=18:
        day_part='4'
        
    if connected():
        os.chdir('/home/pi/Desktop/projeto_fotovoltaica')
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth) 
        if day_part == '1':
            data = datetime.date.today() - datetime.timedelta(days=1)
            dir_name = data.strftime("dados_%Y_%m_%d_4")
            if os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2"):
                gfile = drive.CreateFile({'title': dir_name})
                gfile.SetContentFile("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                gfile.Upload()
                print(dir_name+' uploaded')
                os.remove("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                print(dir_name+'.tar.bz2 deleted')
        elif day_part == '2':
            dir_name = data.strftime("dados_%Y_%m_%d_1")
            if os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2"):
                gfile = drive.CreateFile({'title': dir_name})
                gfile.SetContentFile("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                gfile.Upload()
                print(dir_name+' uploaded')
                os.remove("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                print(dir_name+'.tar.bz2 deleted')
        elif day_part == '3':
            dir_name = data.strftime("dados_%Y_%m_%d_2")
            if os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2"):
                gfile = drive.CreateFile({'title': dir_name})
                gfile.SetContentFile("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                gfile.Upload()
                print(dir_name+' uploaded')
                os.remove("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                print(dir_name+'.tar.bz2 deleted')
        elif day_part == '4':
            dir_name = data.strftime("dados_%Y_%m_%d_3")
            if os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2"):
                gfile = drive.CreateFile({'title': dir_name})
                gfile.SetContentFile("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                gfile.Upload()
                print(dir_name+' uploaded')
                os.remove("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                print(dir_name+'.tar.bz2 deleted')
                
                