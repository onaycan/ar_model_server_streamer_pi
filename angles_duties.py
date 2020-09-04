import RPi.GPIO as GPIO

import time

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)
p.start(2.5)

time.sleep(1)

def SetAngle(angle):
    global p , servoPIN
    duty = angle / 18 + 2.5
    GPIO.output(servoPIN, True)
    p.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servoPIN, False)


#while True:
#    p.ChangeDutyCycle(12.5)  
#    time.sleep(1) 
#    p.ChangeDutyCycle(2.5)  
#    time.sleep(1)  

curangle = 180
SetAngle(curangle)

curangle = 0
SetAngle(curangle)

curangle = 90
SetAngle(curangle)

p.stop()
GPIO.cleanup()
