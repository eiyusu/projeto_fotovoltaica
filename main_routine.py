# sudo pigpiod
from AD770X import *
from ischedule import schedule, run_loop
import os
import pigpio
from sense_hat import SenseHat
import time

# Inicializacao comum - pigpiod e ADC7705
os.system('sudo pigpiod')
time.sleep(1)
ad7705 = AD770X(device=0)
time.sleep(1)
pi = pigpio.pi()
time.sleep(1)

# Escalas comuns
ACS712_ESCALA =10 #1A/100mV = 10A/V
ACS712_OFFSET =2.5 #2.5V para 0A com ganho de 100mV/

# Configuracao
abrir_menu = True # Se trocada, deve manualmente configurar o comando
# 1 - Flutuante, 2 - Fixo, 3 - Provisório
# comando = 3
# Se comando = 2, deve dizer para ler ou não a irradiancia
# LER_IRR = False

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

def main(args):
    
    if abrir_menu:
        print('1 - Flutuante\n 2 - Fixo\n 3 - Provisório')
        comando = input('\nSelecione o sistema: ')
        
    if comando == 1:
        from SPI_flutuante import *
        from senseHat_measurements import *
        
        # GPIO Flutuante
        GPIO_TENSAO_P1P2 = 5
        GPIO_TENSAO_P3P4 = 6
        GPIO_CURR = 22
        GPIO_IRR = 26
        
        schedule(read_SPI_flutuante,interval=0.1)
        schedule(read_SenseHat,interval=1)
        
    elif comando == 2:
        from SPI_fixo import *
        
        # GPIO Fixo
        GPIO_TENSAO = 5
        GPIO_IRR = 26
        
        irr_read = input('\nLer irradiação? (s/n)')
        if irr_read == 's':
            LER_IRR = True
        else:
            LER_IRR = False
        schedule(read_SPI_fixo,interval=0.1)
        
    elif commando == 3:
        from SPI_provisorio import *
        from senseHat_measurements import *
        
        # GPIO Provisorio
        GPIO_TENSAO = 5
        GPIO_CURR_IRR = 22
        
        schedule(read_SPI_provisorio,interval=0.1)
        schedule(read_SenseHat,interval=1)
        
    run_loop()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))