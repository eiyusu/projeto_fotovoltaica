import os
import time
import datetime
import shutil
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
                os.remove("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
        elif day_part == '2':
            dir_name = data.strftime("dados_%Y_%m_%d_1")
            if os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2"):
                gfile = drive.CreateFile({'title': dir_name})
                gfile.SetContentFile("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                gfile.Upload()
                os.remove("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
        elif day_part == '3':
            dir_name = data.strftime("dados_%Y_%m_%d_2")
            if os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2"):
                gfile = drive.CreateFile({'title': dir_name})
                gfile.SetContentFile("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                gfile.Upload()
                os.remove("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
        elif day_part == '4':
            dir_name = data.strftime("dados_%Y_%m_%d_3")
            if os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2"):
                gfile = drive.CreateFile({'title': dir_name})
                gfile.SetContentFile("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                gfile.Upload()
                os.remove("/home/pi/Desktop/projeto_fotovoltaica/saved_data/"+dir_name+".tar.bz2")
                
                
def file_handler():
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
            command = 'cd /home/pi/Desktop/projeto_fotovoltaica/;tar cvjf saved_data/' + dir_name +'.tar.bz2 '+ dir_name
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
            command = 'cd /home/pi/Desktop/projeto_fotovoltaica/;tar cvjf saved_data/' + dir_name +'.tar.bz2 '+ dir_name
            os.system(command)
            shutil.rmtree("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name, ignore_errors = True)
                
def main(args):
    while True:
        time.sleep(3000)
        #Comprime os arquivos
        file_handler()
        
        #Liga internet
        os.system('cd /etc/ppp/peers/;sudo ifconfig wlan0 down;sudo pon rnet')
        time.sleep(600)
        
        #Joga arquivos no drive
        upload_files()
        
        #Desliga internet
        os.system('cd /etc/ppp/peers/;sudo poff rnet;sudo ifconfig wlan0 up')

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
                
                