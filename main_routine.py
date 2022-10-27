# sudo pigpiod
from AD770X import *
import os
import pigpio
from sense_hat import SenseHat
import time

# Inicializacao comum - pigpiod e ADC7705
os.system('sudo pigpiod')
time.sleep(.5)
ad7705 = AD770X(device=0)
pi = pigpio.pi()

# GPIO Provisorio
GPIO_TENSAO = 5
GPIO_CURR_IRR = 22

# GPIO Fixo
GPIO_TENSAO = 5
GPIO_IRR = 26
LER_IRR = False

# GPIO Flutuante
GPIO_TENSAO_P1P2 = 5
GPIO_TENSAO_P3P4 = 6
GPIO_CURR = 22
GPIO_IRR = 26

# Escalas comuns
ACS712_ESCALA =10 #1A/100mV = 10A/V
ACS712_OFFSET = 25 #2.5V para 0A com ganho de 100mV/
 

def main(args):
    # Subprocesso para fazer upload dos dados
    os.popen('python3 /home/pi/Desktop/projeto_fotovoltaica/file_uploader.py')

    # Subprocesso para fazer leitura do SPI Fixo
    # os.popen('python3 /home/pi/Desktop/projeto_fotovoltaica/SPI_fixo.py')

    # Subprocesso para fazer leitura do SPI Flutuante
    #os.popen('python3 /home/pi/Desktop/projeto_fotovoltaica/SPI_flutuante.py')

    # Subprocesso para fazer leitura do SPI Provisório
    os.popen('python3 /home/pi/Desktop/projeto_fotovoltaica/SPI_provisorio.py')

    # Subprocesso para fazer leitura do Sense Hat
    os.popen('python3 /home/pi/Desktop/projeto_fotovoltaica/senseHat_measurements.py')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))