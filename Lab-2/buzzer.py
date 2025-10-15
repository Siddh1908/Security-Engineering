from gpiozero import Buzzer
from time import sleep

bz =  None   # replace None with the correct pin number
bz.off() 

def success():
    """3 short beeps."""
    # TODO: on/off pattern


def fail():
    """1 long beep."""
    # TODO: on/off pattern


def cleanup():
    bz.off()
    bz.close()