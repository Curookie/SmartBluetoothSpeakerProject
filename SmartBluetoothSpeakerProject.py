# 컴정과 'Smart 블루투스' 프로젝트 201344052 B반 원종진

import subprocess
import threading
import time
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

F_STATE = [ 'search', 'ready', 'wait' ]

FIRST_TRIG = 5
FIRST_ECHO = 6
SECOND_TRIG = 13
SECOND_ECHO = 19
LED_GREEN = 16
LED_YELLOW = 20
LED_RED = 21
SWITCH_UP = 17
SWITCH_DOWN = 27
SWITCH_CHANGE = 22


TRIG = [FIRST_TRIG, SECOND_TRIG]
ECHO = [FIRST_ECHO, SECOND_ECHO]
distance = [0, 0]
pulse_start = [0, 0]
pulse_end = [0, 0]
pulse_duration = [0, 0]

people_cnt = 0
ready_cnt = 0
wait_cnt = 0
ready_success = False

for i in range(len(ECHO)) :
    GPIO.setup(TRIG[i], GPIO.OUT)
    GPIO.setup(ECHO[i], GPIO.IN)

GPIO.setup(LED_GREEN, GPIO.OUT)
#GPIO.setup(LED_YELLOW, GPIO.OUT)
#GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(SWITCH_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_CHANGE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(SWITCH_CHANGE, GPIO.FALLING, callback=changeMusic)


def start():
    changeLED()
    while True:
        i = search()
        
        if(i==0):
            ready(1)
        else:
            ready(0)

        if(ready_success):
            if(i==0):
                wait(1)
            else:
                wait(0)

        resetOption()

    
def resetOption():
    ready_success = False
    ready_cnt = 0
    wait_cnt = 0
            

def checkTime():
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s


def changePeople(sensor_n):
    if(sensor_n==1):
        people_cnt = people_cnt + 1
    elif(people_cnt<=0):
        people_cnt = 0
        print("People_Count_Error:-n error")
    else:
        people_cnt = people_cnt - 1
    changeLED()    
    printLog(sensor_n)


def changeLED():
    if(people_cnt==0):
        GPIO.output(LED_GREEN, False)
        GPIO.output(LED_YELLOW, False)
        GPIO.output(LED_RED, False)
    elif(people_cnt<3) :
        GPIO.output(LED_GREEN, True)
        GPIO.output(LED_YELLOW, False)
        GPIO.output(LED_RED, False)
    elif(people_cnt<5) :
        GPIO.output(LED_GREEN, False)
        GPIO.output(LED_YELLOW, True)
        GPIO.output(LED_RED, False)
    else:
        GPIO.output(LED_GREEN, False)
        GPIO.output(LED_YELLOW, False)
        GPIO.output(LED_RED, True)

def changeMusic():
    print("change Music")
 

def printLog(sensor_n):
    if(sensor_n==0):
        print("Time : ",checkTime(),":: 1 Person OUT, Now People Count : ",people_cnt)
    else:
        print("Time : ",checkTime(),":: 1 Person IN, Now People Count : ",people_cnt) 
        



def search():
    try:
        while True:
            for i in range(len(ECHO)):
                GPIO.output(TRIG[i],False)
                time.sleep(0.25)
     
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
                
                if(distance[i]<60) :
                    print("REC ! - 1st sensor ",i);
                    return i
                    
    except:    
        GPIO.cleanup()
        print("Searching Error")



def ready(sensor_number):
    try:
        while (ready_cnt < 100):
            GPIO.output(TRIG[sensor_number],False)
            time.sleep(0.1)
     
            GPIO.output(TRIG[sensor_number],True)
            time.sleep(0.00001)
            GPIO.output(TRIG[sensor_number],False)
                 
            while GPIO.input(ECHO[sensor_number])==0:
                pulse_start[sensor_number]=time.time()
                    
                 
            while GPIO.input(ECHO[sensor_number])==1:
                pulse_end[sensor_number]=time.time()

            pulse_duration[sensor_number]=pulse_end[sensor_number]-pulse_start[sensor_number]
                 
            distance[sensor_number]=pulse_duration[sensor_number]*17150
            distance[sensor_number]=round(distance[sensor_number],2)
            now = time.localtime()

            if(distance[sensor_number]<60) :
                print("REC ! - 2nd sensor ",sensor_number);
                changePeople(sensor_number)
                ready_success = True
                return
                
            ready_cnt = ready_cnt + 1
            
    except:    
        GPIO.cleanup()
        print("Readying Error")


def wait(sensor_number):
    try:
        while (ready_cnt < 30):
            GPIO.output(TRIG[sensor_number],False)
            time.sleep(0.1)
     
            GPIO.output(TRIG[sensor_number],True)
            time.sleep(0.00001)
            GPIO.output(TRIG[sensor_number],False)
                 
            while GPIO.input(ECHO[sensor_number])==0:
                pulse_start[sensor_number]=time.time()
                    
                 
            while GPIO.input(ECHO[sensor_number])==1:
                pulse_end[sensor_number]=time.time()

            pulse_duration[sensor_number]=pulse_end[sensor_number]-pulse_start[sensor_number]
                 
            distance[sensor_number]=pulse_duration[sensor_number]*17150
            distance[sensor_number]=round(distance[sensor_number],2)
            now = time.localtime()

            if(distance[sensor_number]<60) :
                print("Waitting for Out or In, This Person");
                wait_cnt = 0
                
            wait_cnt = wait_cnt + 1
            
    except:    
        GPIO.cleanup()
        print("Waitting Error")


print("--- === Smart Bluetooth Speaker Detection Start === ---")

th1 = Thread(target=start)


#subprocess.call('mplayer ./mp3/iu.mp3', shell=True)



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

'''

in_ready = False
out_ready = False

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
