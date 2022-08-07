#spidev
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)
to_send = [0x1c]

while (True):
    a=spi.xfer2(to_send)
    print(a)
