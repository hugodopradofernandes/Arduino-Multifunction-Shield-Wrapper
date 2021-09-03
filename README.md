
# Arduino Multifunction Shield Wrapper

<img src="https://github.com/hugodopradofernandes/Arduino-Multifunction-Shield-Wrapper/blob/main/ArduinoMultifunctionShield.jpg" width="800">

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


**4th** - Use directly or import **zz_wrapper_arduinoMF_v1.py**, the python script to write commands on serial port to interact with the wrapper installed on Arduino

Some examples of scripts importing zz_wrapper_arduinoMF_v1.py
*yy_script_btcethprice.py
yy_script_boardtest.py*

These 2 scripts import zz_wrapper_arduinoMF_v1.py to interact with Arduino Multifunction shield by serial port
Video Example: https://www.reddit.com/r/arduino/comments/p3efrt/crypto_price_update_realtime/


**5th** - From flask directory, run ff_wrapper_arduinoMF.py to open a web interface to interact with Arduino Multifunction shield

<img src="https://raw.githubusercontent.com/hugodopradofernandes/Arduino-Multifunction-Shield-Wrapper/main/images/flask_1.png" width="400">
<img src="https://raw.githubusercontent.com/hugodopradofernandes/Arduino-Multifunction-Shield-Wrapper/main/images/flask_2.png" width="400">

