# 컴정과 'Smart 블루투스' 프로젝트 201344052 B반 원종진

import subprocess
import os
import time
import random
import RPi.GPIO as GPIO



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

F_STATE = [ 'search', 'ready', 'wait' ]
song = ['cs.mp3', 'hd.mp3', 'mr.mp3'],['am.mp3', 'bi.mp3', 'iu.mp3', 'ho.mp3'],['mg.mp3','nn.mp3','nm.mp3','pi.mp3']

FIRST_TRIG = 5
FIRST_ECHO = 6
SECOND_TRIG = 13
SECOND_ECHO = 19
BUZZ = 15
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

global volume
global people_cnt
global ready_cnt
global wait_cnt
global ready_success
global player
global mp3open

volume = 80
people_cnt=0
ready_cnt =0
wait_cnt=0
ready_success=False
mp3open=False

for i in range(len(ECHO)) :
    GPIO.setup(TRIG[i], GPIO.OUT)
    GPIO.setup(ECHO[i], GPIO.IN)

GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_YELLOW, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(BUZZ, GPIO.OUT)
GPIO.setup(SWITCH_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_CHANGE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def btnChange(channel) :
    global mp3open
    global player
    musicName = ""
    os.system("killall -9 mplayer")
    mp3open=True
    musicName = random.choice(random.choice(song))
    player = subprocess.Popen(["mplayer","./mp3/"+musicName], stdin=subprocess.PIPE)
    print("Change Button Presssed! : "+musicName)

def btnUp(channel) :
    global volume
    if(volume<100) :
        volume = volume +2
        os.system("amixer cset numid=1 "+str(volume)+"% | amixer cset numid=3 "+str(volume)+"%")
    print("Change Volume to "+str(volume)+"%")


def btnDown(channel) :
    global volume
    if(volume>0) :
        volume = volume - 2
        os.system("amixer cset numid=1 "+str(volume)+"% | amixer cset numid=3 "+str(volume)+"%")
    print("Change Volume to "+str(volume)+"%")

GPIO.add_event_detect(SWITCH_CHANGE, GPIO.FALLING, callback=btnChange, bouncetime=300)
GPIO.add_event_detect(SWITCH_UP, GPIO.FALLING, callback=btnUp, bouncetime=300)
GPIO.add_event_detect(SWITCH_DOWN, GPIO.FALLING, callback=btnDown, bouncetime=300)

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

def checkTime():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s


def changePeople(sensor_n):
    global people_cnt
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
    global people_cnt
    if(people_cnt<=0):
        changeMusic()
        GPIO.output(LED_GREEN, False)
        GPIO.output(LED_YELLOW, False)
        GPIO.output(LED_RED, False)
    elif(people_cnt<3) :
        changeMusic()
        GPIO.output(LED_GREEN, True)
        GPIO.output(LED_YELLOW, False)
        GPIO.output(LED_RED, False)
    elif(people_cnt<5) :
        changeMusic()
        GPIO.output(LED_GREEN, False)
        GPIO.output(LED_YELLOW, True)
        GPIO.output(LED_RED, False)
    elif(people_cnt==5):
        changeMusic()
        GPIO.output(LED_GREEN, False)
        GPIO.output(LED_YELLOW, False)
        GPIO.output(LED_RED, True)

def changeMusic():
    global player
    global people_cnt
    global mp3open
    musicName = ""
    #player=subprocess.Popen(["mplayer", "-slave","./mp3/iu.mp3"], bufsize=-1 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)   
    if(mp3open==True) :
        os.system("killall -9 mplayer")
        mp3open=False

    if(people_cnt==1) :
        musicName = random.choice(song[0])
        player=subprocess.Popen(["mplayer","./mp3/"+musicName], stdin=subprocess.PIPE)
        mp3open=True
        
    elif(people_cnt==2) :
        musicName = random.choice(song[1])
        player=subprocess.Popen(["mplayer","./mp3/"+musicName], stdin=subprocess.PIPE)
        mp3open=True

    elif(people_cnt==3) :
        musicName = random.choice(song[1])
        player=subprocess.Popen(["mplayer","./mp3/"+musicName], stdin=subprocess.PIPE)
        mp3open=True

    elif(people_cnt==4) :
        musicName = random.choice(song[1])
        player=subprocess.Popen(["mplayer","./mp3/"+musicName], stdin=subprocess.PIPE)
        mp3open=True

    elif(people_cnt==5) :
        musicName = random.choice(song[2])
        player=subprocess.Popen(["mplayer","./mp3/"+musicName], stdin=subprocess.PIPE)
        mp3open=True
    
    #player=subprocess.call(["mplayer","./mp3/iu.mp3"] )
    #pygame.mixer.music.load("mp3/iu.mp3")
    #pygame.mixer.music.play()
    #print("change Music ->"+musicName)
 

def printLog(sensor_n):
    global people_cnt
    if(sensor_n==0):
        print("Time : ",checkTime(),":: 1 Person OUT, Now People Count : ",people_cnt)
    else:
        print("Time : ",checkTime(),":: 1 Person IN, Now People Count : ",people_cnt) 
        


def search():
    #print(F_STATE[0])
    GPIO.output(BUZZ,1)
    time.sleep(0.25)
    GPIO.output(BUZZ,0)
    try:
        while True:
            for i in range(len(ECHO)):
                GPIO.output(TRIG[i],False)
                time.sleep(0.12)
     
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

                #print(distance[i], ", ",i)
                
                if(distance[i]<55) :
                    #print("REC ! - 1st sensor ",i);
                    return i
                    
    except Exception as e:
        GPIO.cleanup()
        print("Searching Error : ", e)


def ready(sensor_number):
    global ready_cnt
    global ready_success
    #print(F_STATE[1])
    GPIO.output(BUZZ,1)
    time.sleep(0.05)
    GPIO.output(BUZZ,0)
    time.sleep(0.03)
    GPIO.output(BUZZ,1)
    time.sleep(0.05)
    GPIO.output(BUZZ,0)
    try:
        while (ready_cnt < 42):
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

            #print(distance[sensor_number], ", ",sensor_number, ", ",ready_cnt)

            if(distance[sensor_number]<55) :
                #print("REC ! - 2nd sensor ",sensor_number);
                changePeople(sensor_number)
                ready_success = True
                return
                
            ready_cnt = ready_cnt + 1
            
    except Exception as e:    
        GPIO.cleanup()
        print("Readying Error : ", e)


def wait(sensor_number):
    global wait_cnt
    #print(F_STATE[2])
    GPIO.output(BUZZ,1)
    time.sleep(0.05)
    GPIO.output(BUZZ,0)
    time.sleep(0.03)
    GPIO.output(BUZZ,1)
    time.sleep(0.05)
    GPIO.output(BUZZ,0)
    time.sleep(0.03)
    GPIO.output(BUZZ,1)
    time.sleep(0.05)
    GPIO.output(BUZZ,0)
    try:
        while (wait_cnt < 21) :
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

            #print(distance[sensor_number], ", ",sensor_number, ", ",wait_cnt)

            if(distance[sensor_number]<55) :
                #print("Waitting for Out or In, This Person");
                wait_cnt = 0
                
            wait_cnt = wait_cnt + 1
            
    except Exception as e:
        GPIO.cleanup()
        print("Waitting Error : ", e)


def resetOption():
    global ready_success
    global ready_cnt
    global wait_cnt
    ready_success = False
    ready_cnt = 0
    wait_cnt = 0

print("--- === Smart Bluetooth Speaker Detection Start === ---")
start()
