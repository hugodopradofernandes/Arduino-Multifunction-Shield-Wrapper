#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------
try:
    import sys
    import time
    import datetime
    import logging
    sys.path.insert(0, '..')
    import zz_wrapper_arduinoMF_v1 as serialarduino
    import subprocess
    from flask import (Flask, request, jsonify, render_template, send_from_directory)
except:
    print(sys.exc_info())

#----------------------------------------------------------------------------------------------------
arduino = serialarduino.InitComSerial()

log_filename='ll_wrapper_arduinoMF.log'
logging.basicConfig(
filename=log_filename, filemode='w',
format='%(asctime)s %(levelname)-2s %(message)s',
level=logging.INFO,
datefmt='%Y-%m-%d %H:%M:%S')

#----------------------------------------------------------------------------------------------------
def MFbanner(text='',speed=150,repeat=1):
    for z in range(0,repeat):
        for i in range(0, len(text)+8):
            banner_text = '    '+text+'    '
            banner_init = i
            banner_end = i+4
            serialarduino.SendComSerial(arduino,"wr:"+banner_text[banner_init:banner_end])
            serialarduino.SendComSerial(arduino,"wait:"+str(speed))

#----------------------------------------------------------------------------------------------------
def MFcount_7segment(first=0,second=9999,wait=100,beep=0):
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
def MFLedShow():
    for i in range(1,16):
        if i < 10: txt_spaces='   '
        if i >= 10: txt_spaces='  '
        serialarduino.SendComSerial(arduino,"wr:"+txt_spaces+str(i))
        serialarduino.SendComSerial(arduino,"ld:"+str(i)+":1")
        time.sleep(.5)
        serialarduino.SendComSerial(arduino,"cl")

#----------------------------------------------------------------------------------------------------
def ReadComSerial():
    serialmessage = serialarduino.ReadComSerial(arduino)
    return serialmessage
#----------------------------------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'AvQvRBTiZfv8jGdGUHFXjUZMZDQ8GZt1'
app.config['TEMPLATES_AUTO_RELOAD'] = True

#----------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    tile = "ArduinoMF App"
    var_1 = "Wrapper_arduinoMF"
    var_2 = "Functions_arduinoMF"
    arduino_commands = serialarduino.SendComSerial(arduino,'help')
    commands_attributes = "Use Help:Command to view available parameters"
    arduino_functions = ['MFbanner','MFcount_7segment','MFLedShow','ReadComSerial']
    functions_attributes = ['Text banner test:150:2','100:0:150:10','','']
    list_1 = str(arduino_commands).split("Commands:")[1].replace(' ','').split(",")
    list_2 = arduino_functions
    list_3 = commands_attributes
    list_4 = functions_attributes
    return render_template('ff_wrapper_arduinoMF.html', tile=tile, var_1=var_1, var_2=var_2, list_1=list_1, list_2=list_2, list_3=list_3, list_4=list_4)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
#----------------------------------------------------------------------------------------------------
@app.route('/wrapper_arduinoMF', methods = ['POST'])
def ajax_request_1():
    form_value_1 = request.form['form_value_1']
    form_value_2 = request.form['form_value_2']
    
    arduino_response = serialarduino.SendComSerial(arduino,form_value_1+':'+form_value_2)
    
    out, err = subprocess.Popen(['tail','-30',log_filename], stdout=subprocess.PIPE).communicate() 
    log_tail = '<br>'.join(str(e) for e in out.splitlines() if "/ttyUSB" in str(e) and "Commands:" not in str(e)).replace('b"','').replace(';"',';').replace('b"','').replace(';"',';').replace("b'","").replace(";'",";")
    
    response_value = {'arduino_response': arduino_response, 'log_tail': '<hr>'+log_tail}
    return jsonify(response_value=response_value)

#----------------------------------------------------------------------------------------------------
@app.route('/Functions_arduinoMF', methods = ['POST'])
def ajax_request_2():
    form_value_3 = request.form['form_value_3']
    form_value_4 = request.form['form_value_4']
    
    if form_value_3 == 'MFbanner':
        try:
            attr_1 = str(form_value_4.split(":")[0])
            attr_2 = int(form_value_4.split(":")[1])
            attr_3 = int(form_value_4.split(":")[2])
            MFbanner(attr_1,attr_2,attr_3)
            function_response = 'MFbanner Ok'
        except:
            function_response = 'MFbanner Not Ok'
            pass
    elif form_value_3 == 'MFcount_7segment':
        try:
            attr_1 = int(form_value_4.split(":")[0])
            attr_2 = int(form_value_4.split(":")[1])
            attr_3 = int(form_value_4.split(":")[2])
            attr_4 = int(form_value_4.split(":")[3])
            MFcount_7segment(attr_1,attr_2,attr_3,attr_4)
            function_response = 'MFcount_7segment Ok'
        except:
            function_response = 'MFcount_7segment Not Ok'
            pass
    elif form_value_3 == 'MFLedShow':
        try:
            MFLedShow()
            function_response = 'MFLedShow Ok'
        except:
            function_response = 'MFLedShow Not Ok'
            pass
    elif form_value_3 == 'ReadComSerial':
        try:
            function_response = ReadComSerial()
        except:
            function_response = 'ReadComSerial Not Ok'
            pass
    else:
        function_response = 'InvalidCommand'
    
    out, err = subprocess.Popen(['tail','-30',log_filename], stdout=subprocess.PIPE).communicate() 
    log_tail = '<br>'.join(str(e) for e in out.splitlines() if "/ttyUSB" in str(e) and "Commands:" not in str(e)).replace("b'","").replace(";'",";")
    
    response_value = {'function_response': function_response, 'log_tail': '<hr>'+log_tail}
    return jsonify(response_value=response_value)

#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    serialarduino.CloseComSerial(arduino)
