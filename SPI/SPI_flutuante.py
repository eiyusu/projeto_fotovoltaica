from AD770X import *
import time
import pigpio
from datetime import date, datetime
import csv
import os

def main(args):

    pi = pigpio.pi()
    data = date.today()
    filename = data.strftime("SPI_flut_dadosAltaFrequencia_%d_%m_%Y")
    horario = datetime.now().time()
    horario = str(horario)

    #Definição de pinos
    GPIO_TENSAO_P1P2 = 5
    GPIO_TENSAO_P3P4 = 6
    GPIO_CURR = 22
    GPIO_IRR = 26
    ACS712_ESCALA = 10 #1A/100mV = 10A/V
    ACS712_OFFSET = 2.5 #2.5V para 0A com ganho de 100mV/A

    #Desligar CS de todas placas
    pi.write(GPIO_TENSAO_P1P2, 1)
    pi.write(GPIO_TENSAO_P3P4, 1)
    pi.write(GPIO_CURR, 1)
    pi.write(GPIO_IRR, 1)


    ad7705 = AD770X(device=0)

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

    header = ["horario", "tensao_p1(V)", "tensao_p2(V)", "tensao_p3(V)", "tensao_p4(V)", "corrente_p1p2(A)", "corrente_p3p4(A)", "irradiacao(W/m2)"]

    dados = [
    {"horario": horario, "tensao_p1(V)": tensao_p1, "tensao_p2(V)": tensao_p2, "tensao_p3(V)": tensao_p3, "tensao_p4(V)": tensao_p4, "corrente_p1p2(A)": corrente_p1p2, "corrente_p3p4(A)": corrente_p3p4, "irradiacao(W/m2)": irradiacao}
    ]

    file_loc = "/home/pi/Desktop/projeto_energia/Dados/SPI/"+filename+".csv"

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
