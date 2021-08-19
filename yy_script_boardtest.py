#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------
try:
    import sys
    import time
    import logging
    import requests
    import zz_serial_arduino_v1 as serialarduino
except:
    print(sys.exc_info())

#----------------------------------------------------------------------------------------------------
logging.basicConfig(
filename='log.out',
format='%(asctime)s %(levelname)-2s %(message)s',
level=logging.INFO,
datefmt='%Y-%m-%d %H:%M:%S')

logging.info('#--- Script starting ---#')
arduino = serialarduino.InitComSerial()
#serialarduino.StatusComSerial(arduino)
serialarduino.SendComSerial(arduino,"cl:0") 

#----------------------------------------------------------------------------------------------------
def leds_proto_pin():
    for i in range(1, 5):
        if (i % 2 != 0):
            blue = serialarduino.SendComSerial(arduino,"wr:blue") 
            print(blue)
            serialarduino.SendComSerial(arduino,"sp:5:1")
            serialarduino.SendComSerial(arduino,"sp:6:0")
            serialarduino.SendComSerial(arduino,"beep:10:1:1:1:1")
            serialarduino.SendComSerial(arduino,"wait:500")
        else:
            yellow = serialarduino.SendComSerial(arduino,"wr:yell")
            print(yellow)
            serialarduino.SendComSerial(arduino,"sp:6:1")
            serialarduino.SendComSerial(arduino,"sp:5:0")
            serialarduino.SendComSerial(arduino,"beep:3:3:3:1:1")
            serialarduino.SendComSerial(arduino,"wait:500")
    serialarduino.SendComSerial(arduino,"cl:0") 
#----------------------------------------------------------------------------------------------------
def button_press():
    print("Press some arduino shield button")
    serialarduino.SendComSerial(arduino,"wr:push")
    button = serialarduino.ReadComSerial(arduino).split('_')[1]
    serialarduino.SendComSerial(arduino,"wr:btn."+button)
    print("Button "+button+" pressed")
    serialarduino.SendComSerial(arduino,"led:"+button+":1")
    serialarduino.SendComSerial(arduino,"beep:10:3:"+button+":1:1")
    serialarduino.SendComSerial(arduino,"wait:5000")
    serialarduino.SendComSerial(arduino,"cl:3")

#----------------------------------------------------------------------------------------------------
def banner(text,speed=150,repeat=1):
    for z in range(0,repeat):
        for i in range(0, len(text)+8):
            banner_text = '    '+text+'    '
            banner_init = i
            banner_end = i+4
            serialarduino.SendComSerial(arduino,"wr:"+banner_text[banner_init:banner_end])
            serialarduino.SendComSerial(arduino,"wait:"+str(speed))

#----------------------------------------------------------------------------------------------------
def pot():
    print("Read pot started. CTRL+C to interrupt")
    try:
        previous_value = 0
        while True:
            time.sleep(0.1)
            serialmsg = serialarduino.SendComSerial(arduino,"rp")
            try:
                if (int(float(serialmsg.split('_')[1])) % 2 != 0):
                    serialarduino.SendComSerial(arduino,"sp:6:1")
                    serialarduino.SendComSerial(arduino,"sp:5:0")
                else:
                    serialarduino.SendComSerial(arduino,"sp:6:0")
                    serialarduino.SendComSerial(arduino,"sp:5:1")
                serialarduino.SendComSerial(arduino,"wr:"+serialmsg.split('_')[1])
                if (abs(previous_value - int(float(serialmsg.split('_')[1])))) > 5 and (abs(previous_value - int(float(serialmsg.split('_')[1])))) < 10:
                    serialarduino.SendComSerial(arduino,"led:1:1")
                elif (abs(previous_value - int(float(serialmsg.split('_')[1])))) > 10:
                    serialarduino.SendComSerial(arduino,"led:3:1")
                else:
                    serialarduino.SendComSerial(arduino,"led:15:0")
                previous_value = int(float(serialmsg.split('_')[1]))
            except IndexError:
                pass
            
    except KeyboardInterrupt:
        print("\nRead pot interrupted")
        pass

#----------------------------------------------------------------------------------------------------
def analog():
    print("Read analog started. CTRL+C to interrupt")
    try:
        previous_value = 0
        while True:
            time.sleep(0.1)
            serialmsg = serialarduino.SendComSerial(arduino,"ra")
            try:
                if (int(float(serialmsg.split('_')[1])) % 2 != 0):
                    serialarduino.SendComSerial(arduino,"sp:6:1")
                    serialarduino.SendComSerial(arduino,"sp:5:0")
                else:
                    serialarduino.SendComSerial(arduino,"sp:6:0")
                    serialarduino.SendComSerial(arduino,"sp:5:1")
                serialarduino.SendComSerial(arduino,"wr:"+serialmsg.split('_')[1])
                if (abs(previous_value - int(float(serialmsg.split('_')[1])))) > 5 and (abs(previous_value - int(float(serialmsg.split('_')[1])))) < 250:
                    serialarduino.SendComSerial(arduino,"led:1:1")
                elif (abs(previous_value - int(float(serialmsg.split('_')[1])))) > 250:
                    serialarduino.SendComSerial(arduino,"led:3:1")
                else:
                    serialarduino.SendComSerial(arduino,"led:15:0")
                previous_value = int(float(serialmsg.split('_')[1]))
            except IndexError:
                pass

    except KeyboardInterrupt:
        print("\nRead analog interrupted")
        pass

#----------------------------------------------------------------------------------------------------
def temp():
    print("Read temp started. CTRL+C to interrupt")
    try:
        previous_value = 0.0
        while True:
            time.sleep(0.1)
            serialmsg = serialarduino.SendComSerial(arduino,"gt")
            try:
                if (int(float(serialmsg.split('_')[1])) % 2 != 0):
                    serialarduino.SendComSerial(arduino,"sp:6:1")
                    serialarduino.SendComSerial(arduino,"sp:5:0")
                else:
                    serialarduino.SendComSerial(arduino,"sp:6:0")
                    serialarduino.SendComSerial(arduino,"sp:5:1")
                serialarduino.SendComSerial(arduino,"wr:"+serialmsg.split('_')[1])
                if (abs(previous_value - int(float(serialmsg.split('_')[1])))) > .5 and (abs(previous_value - int(float(serialmsg.split('_')[1])))) < 1:
                    serialarduino.SendComSerial(arduino,"led:1:1")
                elif (abs(previous_value - int(float(serialmsg.split('_')[1])))) > 1:
                    serialarduino.SendComSerial(arduino,"led:3:1")
                else:
                    serialarduino.SendComSerial(arduino,"led:15:0")
                previous_value = int(float(serialmsg.split('_')[1]))
            except IndexError:
                pass
            
    except KeyboardInterrupt:
        print("\nRead temp interrupted")
        pass

#----------------------------------------------------------------------------------------------------
def count_7segment(first=0,second=9999,wait=0,beep=0):
    if first > second:
        start = second
        end = first + 1
        reverse = True
        count = 0
    else:
        start = first
        end = second + 1
        reverse = False
    for z in range(start,end):
        if reverse == True:
            count += 1
            i = end - count
        else: i = z
        if i < 10: serialarduino.SendComSerial(arduino,"wr:   "+str(i))
        if i < 100 and i >= 10: serialarduino.SendComSerial(arduino,"wr:  "+str(i))
        if i < 1000 and i >= 100: serialarduino.SendComSerial(arduino,"wr: "+str(i))
        if i >= 1000: serialarduino.SendComSerial(arduino,"wr:"+str(i))
        if beep > 0 and i % beep == 0: serialarduino.SendComSerial(arduino,"beep:10:1:1:1:1")
        serialarduino.SendComSerial(arduino,"wait:"+str(wait))

#----------------------------------------------------------------------------------------------------
def close():
    serialarduino.SendComSerial(arduino,"cl:0") 
    serialarduino.CloseComSerial(arduino)
    logging.info('#--- Script ending ---#')

#----------------------------------------------------------------------------------------------------
""" main """
if __name__ == '__main__':

# -- board test --
#    leds_proto_pin()

#    button_press()

#    text="'The quick brown fox jumps over the lazy dog ?!'"
#    banner(text,150,2)

    pot()
    analog()
    temp()

#    count_7segment(50,12,100,10)
#    count_7segment(131,144,100,10)

    close()
#----------------------------------------------------------------------------------------------------