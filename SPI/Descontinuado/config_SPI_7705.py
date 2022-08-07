# sudo pigpiod
import pigpio
import time

pi = pigpio.pi()
if not pi.connected:
   exit(0)

pi.write(8, 1)

adc = pi.spi_open(0, 50000, 0)

pi.spi_write(adc, b'\x20')
pi.spi_write(adc, b'\x0C')
pi.spi_write(adc, b'\x10')
pi.spi_write(adc, b'\x40')
pi.spi_write(adc, b'\x38')
pi.spi_close(adc)
pi.stop()