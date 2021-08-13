# arduino

1st - download this library to your Arduino IDE (the multifunction library provided by IDE installer isnt good)
https://github.com/hpsaturn/MultiFuncShield-Library

2nd [optional] - replace the MultiFuncShield.cpp by my modified_MultiFuncShield.cpp that provides more letters to 7 segment display

3rd - Install these libraries on your Arduino IDE:
TimerOne
Wire
OneWire
DallasTemperature

4th - Flash the zz_serial_arduino_1.ino, a wrapper for MultiFuncShield to accept serial commands.
Now your Arduino listens on serial port fo multifunction shield commands. Send [help] to see acepted commands

5th - Use or import zz_serial_arduino_v1.py, the python script to write commands on serial port to interact with the wrapper.

yy_script_btcethprice.py
yy_script_boardtest.py

These 2 scripts use zz_serial_arduino_v1.py to interact with Arduino Multifucntion shield by serial.
