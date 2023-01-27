from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Pin configuratie
# pins=[18, 23, 24, 25]
# pinsReverse = pins[::-1] 
# extrapins=[13, 19]  


# Steppermotor initialisatie
# GPIO.setmode(GPIO.BCM)
# for pin in pins:
#     GPIO.setup(pin, GPIO.OUT)       

# for pin in extrapins:
#     GPIO.setup(pin, GPIO.IN)  
    
# def setup():
#     pins=[18, 23, 24, 25]
#     pinsReverse = pins[::-1]
#     GPIO.setmode(GPIO.BCM)
#     for pin in pins:
#         GPIO.setup(pin, GPIO.OUT)       

#     # for pin in extrapins:
#     #     GPIO.setup(pin, GPIO.IN)  

def running(list, speed):
    for i in range(0, len(list)):
        GPIO.output(list[i-2], 0)    
        GPIO.output(list[i-1], 1)
        GPIO.output(list[i], 1)
        time.sleep(speed)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/start", methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        form_data = request.form
        name1 = form_data['speler1']
        name2 = form_data['speler2']
        return render_template('start.html', result=[name1, name2])


@app.route("/schot1", methods=['GET', 'POST'])
def schot1():
    if request.method == 'POST':
        form_data = request.form
        power = int(form_data['power'])
        speed = float(0.01 - (0.000075 * power))
        counter1 = 0
        counter2 = 0

        #----- Voet schiet ----
        while counter1 < 120:   
            running(pinsReverse, speed)       
            counter1 += 1  
                    
        time.sleep(1)
        while counter2 < 120:
            running(pins, speed)    # om de motor terug te draaien
            counter2 += 1
        
        
        #----------------------
        #------ Rekensom ------

        return render_template('schot1.html', result=power )



if __name__ == "__main__":
    pins=[18, 23, 24, 25]
    pinsReverse = pins[::-1]
    GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
    app.run()
    