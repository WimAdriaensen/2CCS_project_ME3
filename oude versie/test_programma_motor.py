import RPi.GPIO as GPIO
import time
import json
from flask import Flask, request

app = Flask(__name__)
# to use raspberry PI GPIO numbers
GPIO.setmode(GPIO.BCM)

#verzameling van de pins
pins=[18, 23, 24, 25]
pinsReverse = pins[::-1] 
extrapins=[13, 19]  

def running(list):
    for i in range(0, len(list)):
        GPIO.output(list[i-2], 0)    
        GPIO.output(list[i-1], 1)
        GPIO.output(list[i], 1)
        time.sleep(0.0025)
        
# main program     

counter1 = 0
counter2 = 0

for pin in pins:
        GPIO.setup(pin, GPIO.OUT)       

for pin in extrapins:
        GPIO.setup(pin, GPIO.IN)   

try:
    while True:
        while GPIO.input(13) == False:
            running(pins)

        if GPIO.input(19) == False:

            tijd_voor = time.time()

            while counter1 < 512:   # Def running() heeft een sleep time van 0.0025 voor elke pin in pins
                running(pinsReverse)       # 4 pins is totale tijd van 0.008s voor elke oproeping van def running()
                counter1 += 1       # dus voor deze loop bv. 5s te laten lopen tellen we tot (5/0.008 =) 625.
                                    # tellen tot 265 is voldoende om de motor 180deg te draaien
            tijd_na = time.time()

            tijd_tot = tijd_na - tijd_voor
            print(tijd_tot)
            # time.sleep(1)
            # while counter2 < 120:
            #     running(pins)    # om de motor terug te draaien
            #     counter2 += 1

            

            time.sleep(1)
            counter1 = 0
            counter2 = 0

        
except KeyboardInterrupt:
    print("Program done")
    # cleanup at the end of the program
    GPIO.cleanup()
