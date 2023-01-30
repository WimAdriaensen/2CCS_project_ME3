from flask import Flask, render_template, request, session
import RPi.GPIO as GPIO
import time
import random

app = Flask(__name__)

app.secret_key = ',@k(beV1vt,8M)-Bze8OyWiC`DNR~d}-_vW4#Fpp5hytg9lvvmOXXfY>o/~k#t'

name1 = ""
name2= ""
score_p1=0
score_p2=0
score2 = 0
score1 = 0
uitkomst2 = 0

def running(list, speed):
    for i in range(0, len(list)):
        GPIO.output(list[i-2], 0)    
        GPIO.output(list[i-1], 1)
        GPIO.output(list[i], 1)
        time.sleep(speed)


@app.route("/")
def hello():
    return render_template('index.html', data=[{'difficulty':'easy'}, {'difficulty':'medium'}, {'difficulty':'hard'}] )


@app.route("/start", methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        form_data = request.form
        global name1
        name1 = form_data['speler1']
        global name2
        name2 = form_data['speler2']
        global difficulty
        difficulty = form_data['diff_select']

        session['result'] = [name1, name2]

        return render_template('start.html')


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

        if difficulty == "easy":
            getal1 = random.randint(10, 50)
            getal2 = random.randint(10, 50)
            getal3 = random.randint(1, 10)
            getal4 = random.randint(1, 10)
            if getal2 > getal1:
                grootste_getal = getal2
                getal2 = getal1
                getal1 = grootste_getal
        elif difficulty == "medium":
            getal1 = random.randint(50, 100)
            getal2 = random.randint(50, 100)
            getal3 = random.randint(10, 20)
            getal4 = random.randint(10, 20)
        else:
            getal1 = random.randint(70, 110)
            getal2 = random.randint(70, 110)
            getal3 = random.randint(5, 20)


        global uitkomst1 
        
        random_som = random.randint(1,3)

        if random_som == 1:
            if difficulty == "hard":
                som = str(getal1)+" + " + str(getal2) + " x " + str(getal3)
                uitkomst1 = getal1+getal2*getal3

            else:
                som = str(getal1)+" + " + str(getal2)
                uitkomst1 = getal1+getal2
        elif random_som == 2:
            if difficulty == "hard":
                som = str(getal3)+" x " + str(getal2) + " - " + str(getal1)
                uitkomst1 = getal3*getal2-getal1
                
            else:
                som = str(getal1)+" - " + str(getal2)
                uitkomst1 = getal1-getal2
        else:
            if difficulty == "hard":
                som = str(getal1)+" - " + str(getal2) + " x " + str(getal3)
                tussen_uitkomst = getal1-getal2*getal3
                uitkomst1 = round(tussen_uitkomst, 2)

            else:
                som = str(getal3)+" x " + str(getal4)
                uitkomst1 = getal3*getal4
        
        #----------------------

        return render_template('schot1.html', result=[power, som] )


@app.route("/player2", methods=['GET', 'POST'])
def player2():
    if request.method == 'POST':
        form_data = request.form
        global score_p1

        if score_p1 is None:
            score_p1 = int(form_data['score1'])
        else:
            score_p1+=int(form_data['score1'])

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
        if difficulty == "easy":
            getal1 = random.randint(10, 50)
            getal2 = random.randint(10, 50)
            getal3 = random.randint(1, 10)
            getal4 = random.randint(1, 10)
            if getal2 > getal1:
                grootste_getal = getal2
                getal2 = getal1
                getal1 = grootste_getal
        elif difficulty == "medium":
            getal1 = random.randint(50, 100)
            getal2 = random.randint(50, 100)
            getal3 = random.randint(10, 20)
            getal4 = random.randint(10, 20)
        else:
            getal1 = random.randint(70, 110)
            getal2 = random.randint(70, 110)
            getal3 = random.randint(5, 20)


        global uitkomst2
        
        random_som = random.randint(1,3)

        if random_som == 1:
            if difficulty == "hard":
                som = str(getal1)+" + " + str(getal2) + " x " + str(getal3)
                uitkomst2 = getal1+getal2*getal3

            else:
                som = str(getal1)+" + " + str(getal2)
                uitkomst2 = getal1+getal2
        elif random_som == 2:
            if difficulty == "hard":
                som = str(getal3)+" x " + str(getal2) + " - " + str(getal1)
                uitkomst2 = getal3*getal2-getal1
                
            else:
                som = str(getal1)+" - " + str(getal2)
                uitkomst2 = getal1-getal2
        else:
            if difficulty == "hard":
                som = str(getal1)+" - " + str(getal2) + " x " + str(getal3)
                tussen_uitkomst = getal1-getal2*getal3
                uitkomst2 = round(tussen_uitkomst, 2)

            else:
                som = str(getal3)+" x " + str(getal4)
                uitkomst2 = getal3*getal4
                
        
        
        return render_template('schot2.html', result=[power, som] )


@app.route("/end", methods=['GET', 'POST'])
def end():
    if request.method == 'POST':
        form_data = request.form
        global score_p2
        # score_p2 += int(form_data['score2'])
        som_p2 = int(form_data['som2'])

        if score_p2 is None:
            score_p2 = int(form_data['score2'])
        else:
            score_p2+=int(form_data['score2'])

        if som_p2 == uitkomst2:
            score_p2 += 3

        result = [name1, name2, score_p1, score_p2]
        session['result'] = result

    return render_template('end.html')

@app.route("/reset", methods=['GET', 'POST'])
def reset():
    result = session.get('result', [None, None])
    session.pop('result', None)
    session['result'] = result
    return render_template('start.html')

if __name__ == "__main__":
    pins=[18, 23, 24, 25]
    pinsReverse = pins[::-1]
    GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
    app.run(debug=True)
