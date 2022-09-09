# sudo pigpiod
from AD770X import *
import csv
import os
import pigpio
import time
import datetime
from main_routine import *

G_P25_P1 = (4.6/47.5)
G_P25_P2 = (4.62/47.1)
G_P25_P3 = (4.62/47.5)
G_P25_P4 = (3.28/69.4)
G_AD620_P1 = 1.481
G_AD620_P3 = 1.481
G_AD620_IRR = 1.5
OFF_AD620_P1 = 0
OFF_AD620_P3 = 0
OFF_AD620_IRR = 0

def read_SPI_flutuante_sensors():

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
    tensao_p1 = ((ad7705.readADResultRaw(CHN_AIN1)*ESCALA)-OFF_AD620_P1)*(1/G_AD620_P1)*(1/G_P25_P1)
    time.sleep(slp_time)

    ad7705.initChannel(CHN_AIN2)
    time.sleep(slp_time)
    tensao_p2 = ad7705.readADResultRaw(CHN_AIN2)*ESCALA*(1/G_P25_P2)
    #Desativar o CS
    pi.write(GPIO_TENSAO_P1P2, 1)
    time.sleep(slp_time)

    #Canais de tensão da associação P3 P4 --- definir taxa de ganho dos divisores
    #Ativar o CS
    pi.write(GPIO_TENSAO_P3P4, 0)
    time.sleep(slp_time)

    ad7705.initChannel(CHN_AIN1)
    time.sleep(slp_time)
    tensao_p3 = ((ad7705.readADResultRaw(CHN_AIN1)*ESCALA)-OFF_AD620_P3)*(1/G_AD620_P3)*(1/G_P25_P3)
    time.sleep(slp_time)

    ad7705.initChannel(CHN_AIN2)
    time.sleep(slp_time)
    tensao_p4 = ad7705.readADResultRaw(CHN_AIN2)*ESCALA*(1/G_P25_P4)
    #Desativar o CS
    pi.write(GPIO_TENSAO_P3P4, 1)
    time.sleep(slp_time)

    #Canal de correntes das associações ---definir ganho
    #Ativar o CS
    pi.write(GPIO_CURR, 0)
    ad7705.initChannel(CHN_AIN1)
    time.sleep(slp_time)
    corrente_p1p2_v = ad7705.readADResultRaw(CHN_AIN1)*ESCALA
    corrente_p1p2 = (corrente_p1p2_v*ACS712_ESCALA)-ACS712_OFFSET
    time.sleep(slp_time)

    ad7705.initChannel(CHN_AIN2)
    time.sleep(slp_time)
    corrente_p3p4_v = ad7705.readADResultRaw(CHN_AIN2)*ESCALA
    corrente_p3p4 = (corrente_p3p4_v*ACS712_ESCALA)-ACS712_OFFSET
    #Desativar o CS
    pi.write(GPIO_CURR, 1)
    time.sleep(slp_time)

    #Canal do piranômetro ---definir ganho e escala de acordo com a curva do sensor para definir irradiacao
    #Ativar o CS
    pi.write(GPIO_IRR, 0)
    ad7705.initChannel(CHN_AIN2)
    time.sleep(slp_time)
    irradiacao = (((ad7705.readADResultRaw(CHN_AIN1)*ESCALA)*(1/G_AD620_IRR))-OFF_AD620_IRR)*10
    #Desativar o CS
    pi.write(GPIO_IRR, 1)
    
    dir_name = data.strftime("dados_%Y_%m_%d_")+day_part
    if not os.path.exists("/home/pi/Desktop/projeto_fotovoltaica/"+dir_name):
        os.mkdir('/home/pi/Desktop/projeto_fotovoltaica/'+dir_name)
    filename = data.strftime("SPI_flut_%Y_%m_%d_")+day_part
    
    header = ["horario", "tensao_p1(V)", "tensao_p2(V)", "tensao_p3(V)", "tensao_p4(V)", "corrente_p1p2(A)", "corrente_p3p4(A)", "irradiacao(W/m2)"]

    dados = [
    {"horario": horario, "tensao_p1(V)": tensao_p1, "tensao_p2(V)": tensao_p2, "tensao_p3(V)": tensao_p3, "tensao_p4(V)": tensao_p4, "corrente_p1p2(A)": corrente_p1p2, "corrente_p3p4(A)": corrente_p3p4, "irradiacao(W/m2)": irradiacao}
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
    print(str(horario)+': SPI Flutuante data saved')


