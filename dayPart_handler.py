import os
import time
import datetime
import shutil
from main_routine import *

def handle_file():
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

    if day_part == '1':
        data = datetime.date.today() - datetime.timedelta(days=1)
        dir_name = data.strftime("dados_%Y_%m_%d_4")
        if os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name):
            ccommand = 'cd /home/pi/Desktop/projeto_fotovoltaica/;tar cvjf saved_data/' + dir_name +'.tar.bz2 '+ dir_name
            os.system(command)
            shutil.rmtree("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name, ignore_errors = True)
    elif day_part == '2':
        dir_name = data.strftime("dados_%Y_%m_%d_1")
        if os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name):
            command = 'cd /home/pi/Desktop/projeto_fotovoltaica/;tar cvjf saved_data/' + dir_name +'.tar.bz2 '+ dir_name
            os.system(command)
            shutil.rmtree("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name, ignore_errors = True)
    elif day_part == '3':
        dir_name = data.strftime("dados_%Y_%m_%d_2")
        if os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name):
            command = 'cd /home/pi/Desktop/projeto_fotovoltaica/;tar cvjf saved_data/' + dir_name +'.tar.bz2 '+ dir_name
            os.system(command)
            shutil.rmtree("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name, ignore_errors = True)
    elif day_part == '4':
        dir_name = data.strftime("dados_%Y_%m_%d_3")
        if os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name):
            ccommand = 'cd /home/pi/Desktop/projeto_fotovoltaica/;tar cvjf saved_data/' + dir_name +'.tar.bz2 '+ dir_name
            os.system(command)
            shutil.rmtree("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name, ignore_errors = True)
