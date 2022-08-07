from AD770X import *
import time
import pigpio
from datetime import date, datetime
import csv
import os

def main(args):

    pi = pigpio.pi()
    data = date.today()
    filename = data.strftime("SPI_prov_dadosAltaFrequencia_%d_%m_%Y")
    horario = datetime.now().time()
    horario = str(horario)

    #Definição de pinos
    GPIO_TENSAO = 5
    GPIO_CURR_IRR = 22
    ACS712_ESCALA = 10 #1A/100mV = 10A/V
    ACS712_OFFSET = 2.5 #2.5V para 0A com ganho de 100mV/A

    #Desligar CS todas placas
    pi.write(GPIO_TENSAO, 1)
    pi.write(GPIO_CURR_IRR, 1)

    ad7705 = AD770X(device=0)

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
    time.sleep(slp_time)

    #Canal de corrente ---definir ganho
    #Ativar o CS
    pi.write(GPIO_CURR_IRR, 0)
    ad7705.initChannel(CHN_AIN1)
    time.sleep(slp_time)
    corrente_v = ad7705.readADResultRaw(CHN_AIN1)*ESCALA
    corrente = (corrente_v-ACS712_OFFSET)*ACS712_ESCALA
    corrente = str(corrente)
    time.sleep(slp_time)

    #Canal do piranômetro ---definir ganho e escala de acordo com a curva do sensor para definir radiação
    ad7705.initChannel(CHN_AIN2)
    time.sleep(slp_time)
    radiacao = ad7705.readADResultRaw(CHN_AIN2)*ESCALA
    radiacao = str(radiacao)
    #Desativar o CS
    pi.write(GPIO_CURR_IRR, 1)

    header = ["horario", "tensao_p1(V)", "tensao_p2(V)", "corrente(A)", "radiacao(W/m2)"]

    dados = [
    {"horario": horario, "tensao_p1(V)": tensao_p1, "tensao_p2(V)": tensao_p2, "corrente(A)": corrente, "radiacao(W/m2)": radiacao}
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
