import time
from timeloop import Timeloop
from datetime import timedelta
import os

tl = Timeloop()

#@tl.job(interval=timedelta(seconds=.1))
#def read_SPI():
#    os.system('sudo python /home/pi/Desktop/projeto_fotovoltaica/SPI/SPI_provisorio.py')
    
@tl.job(interval=timedelta(seconds=.1))
def read_SenseHat():
    os.system('sudo python /home/pi/Desktop/projeto_fotovoltaica/Sense_hat/sense_measurements.py')

def main(args):
    tl.start(block=True)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))