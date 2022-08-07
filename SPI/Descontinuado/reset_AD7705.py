# sudo pigpiod
import pigpio

pi = pigpio.pi()
if not pi.connected:
   exit(0)
   
#Reset da placa   
pi.write(2, 0)
pi.write(2, 1)
pi.write(2, 0)
pi.write(25, 1)

pi.stop()