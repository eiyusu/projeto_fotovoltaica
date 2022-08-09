# sudo pigpiod
from AD770X import *
from ischedule import schedule, run_loop
import datetime
import os
import pigpio
from sense_hat import SenseHat
import time
from SPI_provisorio import *
from senseHat_measurements import *

os.system('sudo pigpiod')
time.sleep(1)
pi = pigpio.pi()
GPIO_TENSAO =5
GPIO_CURR_IRR =22
ACS712_ESCALA =10 #1A/100mV = 10A/V
ACS712_OFFSET =2.5 #2.5V para 0A com ganho de 100mV/
first_SPI = True
ad7705 = AD770X(device=0)

#SPI
def read_SPI():
    read_SPI_provisorio()

#Sense Hat
def read_SenseHat():
    read_senseHat_sensors()

def main(args):
    schedule(read_SPI,interval=0.1)
    schedule(read_SenseHat,interval=1)

    run_loop()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))