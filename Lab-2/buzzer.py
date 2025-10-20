from gpiozero import Buzzer
from time import sleep

bz =  Buzzer(27)   # replace None with the correct pin number
bz.off() 

def success():
    """3 short beeps."""
   
    for i in range(3):
        bz.on()
        sleep(0.1)
        bz.off()
        sleep(0.1)

def fail():
    """1 long beep."""
    
    bz.on()
    sleep(2.0)
    bz.off()


def cleanup():
    bz.off()
    bz.close()
