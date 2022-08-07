# sudo pigpiod
import pigpio

pi = pigpio.pi()
if not pi.connected:
   exit(0)

adc = pi.spi_open(0, 50000, 0)
data = pi.spi_read(adc, 2)
print(data)

pi.spi_close(adc)
pi.stop()