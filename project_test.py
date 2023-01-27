from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time
import random

app = Flask(__name__)
  

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
        global name2
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

        # global getal1
        getal1 = random.randint(50, 110)
        # global getal2 
        getal2 = random.randint(50, 110)

        global uitkomst1 

        random_som = random.randint(1,3)
        if random_som == 1:
            som = str(getal1)+" + " + str(getal2)
            uitkomst1 = getal1+getal2
        elif random_som == 2:
            som = str(getal1)+" x " + str(getal2)
            uitkomst1 = getal1*getal2
        else:
            som = str(getal1)+" - " + str(getal2)
            uitkomst1 = getal1-getal2
        
        #----------------------

        return render_template('schot1.html', result=[power, som] )


@app.route("/player2", methods=['GET', 'POST'])
def player2():
    if request.method == 'POST':
        form_data = request.form
        global score_p1
        score_p1 = int(form_data['score1'])
        som_p1 = int(form_data['som1'])

        if som_p1 == uitkomst1:
            score_p1 += 3

        return render_template('player2.html', result=name2)


@app.route("/schot2", methods=['GET','POST'])
def schot2():
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

        #------ Rekensom ------------
            # nog te doen

        #---------------------------
        
        
        return render_template('schot2.html', result=[power] )




if __name__ == "__main__":
    pins=[18, 23, 24, 25]
    pinsReverse = pins[::-1]
    GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
    app.run()
    