#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------
try:
    import sys
    import logging
    import time
    import serial #pyserial
except:
    print(sys.exc_info())

#----------------------------------------------------------------------------------------------------
DEVICE='/dev/ttyUSB0'
BAUD_RATE='115200'
TIMEOUT='1'
PARITY='N'
STOPBITS='1'
BYTESIZE='8'

logger = logging.getLogger(__name__)

#----------------------------------------------------------------------------------------------------
def InitComSerial():
    # Starting Serial Connection
    arduino = serial.Serial(DEVICE,
    int(BAUD_RATE),
    timeout=int(TIMEOUT),
    bytesize=int(BYTESIZE),
    stopbits=int(STOPBITS),
    parity=PARITY)
    time.sleep(1.8) # Wait to communicate to Serial after it's established
    return arduino

#----------------------------------------------------------------------------------------------------
def StatusComSerial(arduino):
    # rtscts=BOOL, xonxoff=BOOL, e dsrdtr=BOOL
    logger.info('Port Status: %s ' % (arduino.isOpen()))
    logger.info('Connected Device: %s ' % (arduino.name))
    logger.info('Configuration Dump: %s ' % (arduino))

#----------------------------------------------------------------------------------------------------
def SendComSerial(arduino,user_inp=''):
    arduino.write(bytes(user_inp+'\n', 'utf-8'))
    serialmsg = arduino.readline()
    serial_return=("#" + arduino.name + ": " + serialmsg.decode().rstrip())
    logger.info(serial_return)
    return serial_return

#----------------------------------------------------------------------------------------------------
def ReadComSerial(arduino):
    arduino.reset_input_buffer()
    arduino.reset_output_buffer()
    try:
        while True:
            serialmsg = arduino.readline()
            if serialmsg:
                serial_return=("#" + arduino.name + ": " + serialmsg.decode().rstrip())
                logger.info(serial_return)
                return serial_return
    except KeyboardInterrupt:
        print("\nReadComSerial interrupted")
        pass

#----------------------------------------------------------------------------------------------------
def CloseComSerial(arduino):
    # Closing Serial Connection
    arduino.close()

#----------------------------------------------------------------------------------------------------
""" main """
if __name__ == '__main__':

    logging.basicConfig(
    format='%(asctime)s %(levelname)-2s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

    arduino = InitComSerial()
    StatusComSerial(arduino)
    print ('[exit] to leave, [listen] ro read serial')

    Flag = True
    while Flag:
        try:
            print('!Enter command:', end =" ")
            user_inp = input()
            if user_inp == 'exit':
                Flag = False
            elif user_inp == 'listen' or user_inp == 'read':
                print("ReadComSerial started. CTRL+C to interrupt")
                ReadComSerial(arduino)
            else:
                SendComSerial(arduino,user_inp)
        except:
            print('\nInput interrupted') 
    CloseComSerial(arduino)
#----------------------------------------------------------------------------------------------------
