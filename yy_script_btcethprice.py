#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------
try:
    import sys
    import time
    import logging
    import requests
    import zz_wrapper_arduinoMF_v1 as serialarduino
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
def banner(text,speed=150,repeat=1):
    for z in range(0,repeat):
        for i in range(0, len(text)+8):
            banner_text = '    '+text+'    '
            banner_init = i
            banner_end = i+4
            serialarduino.SendComSerial(arduino,"wr:"+banner_text[banner_init:banner_end])
            serialarduino.SendComSerial(arduino,"wait:"+str(speed))

#----------------------------------------------------------------------------------------------------
def btcprice():
    response = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
    data = response.json()
    return(data["data"]["amount"])
def ethprice():
    response = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
    data = response.json()
    return(data["data"]["amount"])
#----------------------------------------------------------------------------------------------------
def close():
    serialarduino.SendComSerial(arduino,"cl:0") 
    serialarduino.CloseComSerial(arduino)
    logging.info('#--- Script ending ---#')

#----------------------------------------------------------------------------------------------------
""" main """
if __name__ == '__main__':

    try:
        while True:
            price = btcprice()
            text = "BTC price: USD "
            serialarduino.SendComSerial(arduino,"sp:5:1")
            serialarduino.SendComSerial(arduino,"sp:6:0")
            banner(text)
            serialarduino.SendComSerial(arduino,"bd:15:1")
            serialarduino.SendComSerial(arduino,"wr:"+price[0:2]+"."+price[2:4])
            time.sleep(2)
            serialarduino.SendComSerial(arduino,"bd:15:0")

            price = ethprice()
            text = "ETH price: USD "
            serialarduino.SendComSerial(arduino,"sp:5:0")
            serialarduino.SendComSerial(arduino,"sp:6:1")
            banner(text)
            serialarduino.SendComSerial(arduino,"bd:15:1")
            serialarduino.SendComSerial(arduino,"wr:"+price[0:1]+"."+price[1:4])
            time.sleep(2)
            serialarduino.SendComSerial(arduino,"bd:15:0")
    except KeyboardInterrupt:
        print("\nBTC price banner interrupted")
        pass

    close()
#----------------------------------------------------------------------------------------------------
