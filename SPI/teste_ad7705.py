from AD770X import *
import time
import pigpio

def main(args):
    i = 0
    pi = pigpio.pi()
    if not pi.connected:
        exit()

    pi.write(25,0)
    ad7705 = AD770X(device=0)
    ad7705.initChannel(CHN_AIN1)
    time.sleep (slp_time)
    ad7705.initChannel(CHN_AIN2)

    while True :
        print(i)
        time.sleep (slp_time)
        a = ad7705.readADResultRaw(CHN_AIN1)
        time.sleep (slp_time)
        print("Canal 1: " + str(a))
        b = ad7705.readADResultRaw(CHN_AIN2)
        print("Canal 2: " + str(b))

        # Tensão = palava lida*Vdd/2^16
        tensao_a = a*ESCALA
        print("Tensão Canal a: " + str(tensao_a))
        tensao_b = b*5/65535
        print("Tensão Canal b: " + str(tensao_b))

        i=i+1
        if(i>50):
            pi.write(25,1)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
