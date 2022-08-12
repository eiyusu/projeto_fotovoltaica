# sudo pigpiod
from AD770X import *
import csv
import os
import pigpio
import time
import datetime
from main_routine import *

def read_SPI_fixo_sensors():

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

    #Desligar CS todas placas
    pi.write(GPIO_TENSAO,1)
    pi.write(GPIO_IRR,1)

    #Canais de tensão --- definir taxa de ganho dos divisores
    #Ativar o CS
    pi.write(GPIO_TENSAO, 0)
    time.sleep(slp_time)

    ad7705.initChannel(CHN_AIN1)
    time.sleep(slp_time)
    tensao_p1 = ad7705.readADResultRaw(CHN_AIN1)*ESCALA
    time.sleep(slp_time)

    ad7705.initChannel(CHN_AIN2)
    time.sleep(slp_time)
    tensao_p2 = ad7705.readADResultRaw(CHN_AIN2)*ESCALA
    #Desativar o CS
    pi.write(GPIO_TENSAO, 1)

    # Advanio (não será mais pelo AD620/ADC7705)
    if(LER_IRR):
        #Canal do piranômetro ---definir ganho e escala de acordo com a curva do sensor para definir irradiacao
        #Ativar o CS
        time.sleep(slp_time)
        pi.write(GPIO_IRR, 0)
        ad7705.initChannel(CHN_AIN1)
        time.sleep(slp_time)
        irradiacao = ad7705.readADResultRaw(CHN_AIN1)*ESCALA
        #Desativar o CS
        pi.write(GPIO_IRR, 1)
    else:
        irradiacao = "null"
        
    dir_name = data.strftime("dados_%Y_%m_%d_")+day_part
    if not os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name):   
        os.mkdir('/home/pi/Desktop/projeto_fotovoltaica/'+dir_name)
    filename = data.strftime("SPI_fixo_%Y_%m_%d_")+day_part

    header = ["horario", "tensao_p1(V)", "tensao_p2(V)", "irradiacao(W/m2)"]

    dados = [
    {"horario": horario, "tensao_p1(V)": tensao_p1, "tensao_p2(V)": tensao_p2, "irradiacao(W/m2)": irradiacao}
    ]

    file_loc = "/home/pi/Desktop/projeto_fotovoltaica/"+dir_name+"/"+filename+".csv"

    if (os.path.isfile(file_loc)):
        with open(file_loc, "a") as csv_file:
            arquivo = csv.DictWriter(csv_file, fieldnames=header)
            arquivo.writerows(dados)
    else:
        with open(file_loc, "a") as csv_file:
            arquivo = csv.DictWriter(csv_file, fieldnames=header)
            arquivo.writeheader()
            arquivo.writerows(dados)
    csv_file.close()
    print(str(horario)+': SPI Fixo data saved')

