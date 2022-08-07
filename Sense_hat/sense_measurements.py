import time
from datetime import date, datetime
import csv
import os
from sense_hat import SenseHat

def main(args):
    header = ["horario", "umidade_relativa(percent)", "temperatura_umidade(deg_C)", "temperatura_pressao(deg_C)", "pressao(milliBar)", "compass_norte(deg)", "gyro_roll(deg)", "gyro_pitch(deg)", "gyro_yaw(deg)", "accelerometer_roll(deg)", "accelerometer_pith(deg)", "accelerometer_yaw(deg)"]
    sense = SenseHat()
    data = date.today()
    filename = data.strftime("senseHat_%d_%m_%Y")
    horario = datetime.now().time()
    horario = str(horario)
    
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
    
    dados = [{"horario": horario,"umidade_relativa(percent)": umidade,"temperatura_umidade(deg_C)": temp_h,"temperatura_pressao(deg_C)": temp_p,"pressao(milliBar)": pressao,"compass_norte(deg)": compass,"gyro_roll(deg)": gyro_roll,"gyro_pitch(deg)": gyro_pitch,"gyro_yaw(deg)": gyro_yaw,"accelerometer_roll(deg)": accelerom_roll,"accelerometer_pith(deg)": accelerom_pitch,"accelerometer_yaw(deg)": accelerom_yaw}]
    
    file_loc = "/home/pi/Desktop/projeto_energia/Dados/Sense_Hat/"+filename+".csv"
    
    if (os.path.isfile(file_loc)):
        with open(file_loc, "a") as csv_file:
            arquivo = csv.DictWriter(csv_file, fieldnames=header)
            arquivo.writerows(dados)
    else:
        with open(file_loc, "a") as csv_file:
            arquivo = csv.DictWriter(csv_file, fieldnames=header)
            arquivo.writeheader()
            arquivo.writerows(dados)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))