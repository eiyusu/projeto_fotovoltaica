# sudo pigpiod
from AD770X import *
from ischedule import schedule, run_loop
import os
import pigpio
from sense_hat import SenseHat
import time
#from SPI_flutuante import *
from SPI_fixo import *
#from SPI_provisorio import *
from senseHat_measurements import *
from dayPart_handler import *
from file_uploader import *

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
ACS712_OFFSET =2.5 #2.5V para 0A com ganho de 100mV/

#SPI Provisorio
def read_SPI_provisorio():
    read_SPI_provisorio_sensors()
    
#SPI Fixo
def read_SPI_fixo():
    read_SPI_fixo_sensors()
    
#SPI Flutuante
def read_SPI_flutuante():
    read_SPI_flutuante_sensors()

#Sense Hat
def read_SenseHat():
    read_senseHat_sensors()
    
def check_dayPart():
    file_handler()
    
def upload_file():
    upload_files()

def main(args):

# Flutuante
#    schedule(read_SPI_flutuante,interval=0.1)
#    schedule(read_SenseHat,interval=1)

# Fixo
    schedule(read_SPI_fixo,interval=0.1)

# Provisório
#    schedule(read_SPI_provisorio,interval=0.1)
#    schedule(read_SenseHat,interval=1)
    
# Rotina para verificar e comprimir arquivos
    schedule(check_dayPart,interval=7200)

# Rotina para verificar e fazer upload de arquivos
    schedule(upload_file(),interval=7200)
        
    run_loop()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))