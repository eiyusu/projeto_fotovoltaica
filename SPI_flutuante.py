# sudo pigpiod
from AD770X import *
import csv
import os
import pigpio
import time
import datetime
from main_routine import *

def read_SPI_flutuante_sensors():

    data = datetime.date.today()
    horario = datetime.datetime.now()
    horario=str(horario)

    #Desligar CS de todas placas
    pi.write(GPIO_TENSAO_P1P2,1)
    pi.write(GPIO_TENSAO_P3P4, 1)
    pi.write(GPIO_CURR, 1)
    pi.write(GPIO_IRR, 1)

    #Canais de tensão da associação P1 P2 --- definir taxa de ganho dos divisores
    #Ativar o CS
    pi.write(GPIO_TENSAO_P1P2, 0)
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
    pi.write(GPIO_TENSAO_P1P2, 1)
    time.sleep(slp_time)

    #Canais de tensão da associação P3 P4 --- definir taxa de ganho dos divisores
    #Ativar o CS
    pi.write(GPIO_TENSAO_P3P4, 0)
    time.sleep(slp_time)

    ad7705.initChannel(CHN_AIN1)
    time.sleep(slp_time)
    tensao_p3 = ad7705.readADResultRaw(CHN_AIN1)*ESCALA
    tensao_p3 = str(tensao_p3)
    time.sleep(slp_time)

    ad7705.initChannel(CHN_AIN2)
    time.sleep(slp_time)
    tensao_p4 = ad7705.readADResultRaw(CHN_AIN2)*ESCALA
    tensao_p4 = str(tensao_p4)
    #Desativar o CS
    pi.write(GPIO_TENSAO_P3P4, 1)
    time.sleep(slp_time)

    #Canal de correntes das associações ---definir ganho
    #Ativar o CS
    pi.write(GPIO_CURR, 0)
    ad7705.initChannel(CHN_AIN1)
    time.sleep(slp_time)
    corrente_p1p2_v = ad7705.readADResultRaw(CHN_AIN1)*ESCALA
    corrente_p1p2 = (corrente_p1p2_v-ACS712_OFFSET)*ACS712_ESCALA
    corrente_p1p2 = str(corrente_p1p2)
    time.sleep(slp_time)

    ad7705.initChannel(CHN_AIN2)
    time.sleep(slp_time)
    corrente_p3p4_v = ad7705.readADResultRaw(CHN_AIN2)*ESCALA
    corrente_p3p4 = (corrente_p3p4_v-ACS712_OFFSET)*ACS712_ESCALA
    corrente_p3p4 = str(corrente_p3p4)
    #Desativar o CS
    pi.write(GPIO_CURR, 1)
    time.sleep(slp_time)

    #Canal do piranômetro ---definir ganho e escala de acordo com a curva do sensor para definir irradiacao
    #Ativar o CS
    pi.write(GPIO_IRR, 0)
    ad7705.initChannel(CHN_AIN2)
    time.sleep(slp_time)
    irradiacao = ad7705.readADResultRaw(CHN_AIN1)*ESCALA
    irradiacao = str(irradiacao)
    #Desativar o CS
    pi.write(GPIO_IRR, 1)

    
    filename = data.strftime("SPI_flut_%Y_%m_%d")
    
    header = ["horario", "tensao_p1(V)", "tensao_p2(V)", "tensao_p3(V)", "tensao_p4(V)", "corrente_p1p2(A)", "corrente_p3p4(A)", "irradiacao(W/m2)"]

    dados = [
    {"horario": horario, "tensao_p1(V)": tensao_p1, "tensao_p2(V)": tensao_p2, "tensao_p3(V)": tensao_p3, "tensao_p4(V)": tensao_p4, "corrente_p1p2(A)": corrente_p1p2, "corrente_p3p4(A)": corrente_p3p4, "irradiacao(W/m2)": irradiacao}
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
    print(horario+': SPI Flutuante data saved')


