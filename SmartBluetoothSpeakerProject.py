# 컴정과 'Smart 블루투스' 프로젝트 201344052 B반 원종진

import subprocess
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

FIRST_TRIG = 5
FIRST_ECHO = 6
SECOND_TRIG = 13
SECOND_ECHO = 19
LED_GREEN = 16
LED_YELLOW = 20
LED_RED = 21


TRIG = [FIRST_TRIG, SECOND_TRIG]
ECHO = [FIRST_ECHO, SECOND_ECHO]
distance = [0, 0]
pulse_start = [0, 0]
pulse_end = [0, 0]
pulse_duration = [0, 0]

people_cnt = 0
in_ready = False
out_ready = False

for i in range(len(ECHO)) :
    GPIO.setup(TRIG[i], GPIO.OUT)
    GPIO.setup(ECHO[i], GPIO.IN)

GPIO.setup(LED_GREEN, GPIO.OUT)
#GPIO.setup(LED_YELLOW, GPIO.OUT)
#GPIO.setup(LED_RED, GPIO.OUT)

GPIO.output(LED_GREEN, False)

print("start")

#subprocess.call('mplayer ./mp3/iu.mp3', shell=True)

try:
    while True:
        for i in range(len(ECHO)):
            GPIO.output(TRIG[i],False)
            time.sleep(0.1)
 
            GPIO.output(TRIG[i],True)
            time.sleep(0.00001)
            GPIO.output(TRIG[i],False)
             
            while GPIO.input(ECHO[i])==0:
                pulse_start[i]=time.time()
                
             
            while GPIO.input(ECHO[i])==1:
                pulse_end[i]=time.time()

            pulse_duration[i]=pulse_end[i]-pulse_start[i]
             
            distance[i]=pulse_duration[i]*17150
            distance[i]=round(distance[i],2)
            now = time.localtime()
            if(distance[i]<30) :
                print("REC ! - sensor ",i);
                if( in_ready ==True and i==0 ) :
                    people_cnt = people_cnt + 1 
                    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
                    print("Time : ",s,", Sensor Name : Sensor ",i+1,", Distance : ",distance[i],"cm, People Count : ",people_cnt)
                    out_ready = False
                    in_ready = False
                elif(out_ready==True and i==1 ) :
                    people_cnt = people_cnt - 1
                    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
                    print("Time : ",s,", Sensor Name : Sensor ",i+1,", Distance : ",distance[i],"cm, People Count : ",people_cnt)
                    out_ready = False
                    in_ready = False
                elif(i==1) :
                    in_ready = True
                else :
                    out_ready = True
                
except:    
    GPIO.cleanup()
    print("error")


'''
print("start")
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_YELLOW, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(FIRST_TRIG, GPIO.OUT)
GPIO.setup(FIRST_ECHO, GPIO.IN)
GPIO.setup(SECOND_TRIG, GPIO.OUT)
GPIO.setup(SECOND_ECHO, GPIO.IN)

GPIO.output(LED_GREEN, False)
GPIO.output(LED_YELLOW, False)
GPIO.output(LED_RED, False)

try:
    while True:
        GPIO.output(FIRST_TRIG, False)
        GPIO.output(SECOND_TRIG, False)
        time.sleep(0.5)
        GPIO.output(FIRST_TRIG, True)
        GPIO.output(SECOND_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(FIRST_TRIG, False)
        GPIO.output(SECOND_TRIG, False)
        while GPIO.input(echo) == 0 :
            pulse_start = time.time()
        while GPIO.input(echo) == 1 :
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)
        if(distance<=20):
            pwmRed.ChangeDutyCycle(100-distance*5)
        else:
            pwmRed.ChangeDutyCycle(0)
        print("Distance : ", distance, "cm")

        
except :
    print("Cleanning UP")
    GPIO.cleanup()
        
'''
