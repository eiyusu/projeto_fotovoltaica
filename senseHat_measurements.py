from sense_hat import SenseHat
import csv
import os
import time
import datetime
from main_routine import *

def read_senseHat_sensors():
    sense = SenseHat()
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
    
    umidade = sense.humidity
    temp_h = sense.temperature
    pressao = sense.pressure
    temp_p = sense.get_temperature_from_pressure()
    temp_h = sense.get_temperature_from_humidity()
    sense.set_imu_config(True, False, False) #Compass,Gyro,Acc
    compass = sense.compass
    sense.set_imu_config(False, True, False)
    gyro = sense.gyro
    gyro_roll = gyro['roll']
    gyro_pitch = gyro['pitch']
    gyro_yaw = gyro['yaw']
    sense.set_imu_config(False, False, True)
    accelerom = sense.accelerometer
    accelerom_roll = accelerom['roll']
    accelerom_pitch = accelerom['pitch']
    accelerom_yaw = accelerom['yaw']
    
    dir_name = data.strftime("dados_%Y_%m_%d_")+day_part
    if not os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name):
        os.mkdir('/home/pi/Desktop/projeto_fotovoltaica/'+dir_name)
    header_sense = ["horario", "umidade_relativa(percent)", "temperatura_umidade(deg_C)", "temperatura_pressao(deg_C)", "pressao(milliBar)", "compass_norte(deg)", "gyro_roll(deg)", "gyro_pitch(deg)", "gyro_yaw(deg)", "accelerometer_roll(deg)", "accelerometer_pith(deg)", "accelerometer_yaw(deg)"]
    dados_sense = [{"horario": horario,"umidade_relativa(percent)": umidade,"temperatura_umidade(deg_C)": temp_h,"temperatura_pressao(deg_C)": temp_p,"pressao(milliBar)": pressao,"compass_norte(deg)": compass,"gyro_roll(deg)": gyro_roll,"gyro_pitch(deg)": gyro_pitch,"gyro_yaw(deg)": gyro_yaw,"accelerometer_roll(deg)": accelerom_roll,"accelerometer_pith(deg)": accelerom_pitch,"accelerometer_yaw(deg)": accelerom_yaw}]
    filename_sense = data.strftime("senseHat_%Y_%m_%d")
    file_loc_sense = "/home/pi/Desktop/projeto_fotovoltaica/"+dir_name+"/"+filename_sense+".csv"
    
    if (os.path.isfile(file_loc_sense)):
        with open(file_loc_sense, "a") as csv_file_sense:
            arquivo = csv.DictWriter(csv_file_sense, fieldnames=header_sense)
            arquivo.writerows(dados_sense)
    else:
        with open(file_loc_sense, "a") as csv_file_sense:
            arquivo = csv.DictWriter(csv_file_sense, fieldnames=header_sense)
            arquivo.writeheader()
            arquivo.writerows(dados_sense)
    csv_file_sense.close()
    
    print(str(horario)+': Sense Hat data saved')