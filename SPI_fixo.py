# sudo pigpiod
from AD770X import *
import csv
import os
import pigpio
import time
import datetime
from main_routine_provisorio import *

def read_SPI_fixo_sensors():

    data = datetime.date.today()
    horario = datetime.datetime.now()
    horario=str(horario)

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
    tensao_p1 = str(tensao_p1)
    time.sleep(slp_time)

    ad7705.initChannel(CHN_AIN2)
    time.sleep(slp_time)
    tensao_p2 = ad7705.readADResultRaw(CHN_AIN2)*ESCALA
    tensao_p2 = str(tensao_p2)
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
        irradiacao = str(irradiacao)
        #Desativar o CS
        pi.write(GPIO_IRR, 1)
    else:
        irradiacao = "null"
        
    filename = data.strftime("SPI_fixo_%Y_%m_%d")

    header = ["horario", "tensao_p1(V)", "tensao_p2(V)", "irradiacao(W/m2)"]

    dados = [
    {"horario": horario, "tensao_p1(V)": tensao_p1, "tensao_p2(V)": tensao_p2, "irradiacao(W/m2)": irradiacao}
    ]

    file_loc = "/home/pi/Desktop/projeto_fotovoltaica/Dados/SPI/"+filename+".csv"

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
    print(horario+': SPI Fixo data saved')

