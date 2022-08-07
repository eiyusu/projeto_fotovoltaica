import serial   
import os, time
 
# Habilita comunicação serial na porta ttyS0
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)


#Teste de comunicação pela porta enviando um comando AT seguido de um "Enter"
port.write(b'AT\r\n')
rcv = port.read(10)
print ('\n'+bytes.decode(rcv))
