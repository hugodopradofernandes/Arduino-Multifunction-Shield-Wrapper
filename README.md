
# Arduino Multifunction Shield Wrapper

![Arduino Multifunction Shield](https://github.com/hugodopradofernandes/arduino/blob/main/ArduinoMultifunctionShield.jpg)

**1st** - Download this library to your Arduino IDE lib folder (the multifunction library provided by IDE installer isnt good) https://github.com/hpsaturn/MultiFuncShield-Library

**2st** - Install these libraries on your Arduino IDE:

*TimerOne*\
*Wire*\
*OneWire*\
*DallasTemperature*

**3rd** - Flash the zz_serial_arduino_1.ino, a wrapper for MultiFuncShield to accept serial commands.
**Now your Arduino listens on serial port for multifunction shield commands.** 

Send [help] to Arduino to list acepted commands and parameters

    [Commands: delay, write, blink, clear, led, blinkled, beep, readpot, setpin, readanalog, gettemp]
    Also a serial output is sent displaying button press/longpress/release

**4th** - Use directly or import **zz_serial_arduino_v1.py**, the python script to write commands on serial port to interact with the wrapper installed on Arduino

Some examples of scripts using zz_serial_arduino_v1.py
*yy_script_btcethprice.py
yy_script_boardtest.py*

These 2 scripts use zz_serial_arduino_v1.py to interact with Arduino Multifunction shield by serial port
Video Example: https://www.reddit.com/r/arduino/comments/p3efrt/crypto_price_update_realtime/

---------------------------------------------------------

