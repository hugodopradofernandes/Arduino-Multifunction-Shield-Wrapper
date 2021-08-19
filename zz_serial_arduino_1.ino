#include<TimerOne.h>
#include<Wire.h>
#include<MultiFuncShield.h>
#include<OneWire.h>
#include<DallasTemperature.h>
// ----------------------------------------------------------------------------------------------------
// how much serial data we expect before a newline
const unsigned int MAX_INPUT = 500;

// DS18B20 init
#define ONE_WIRE_BUS A4
OneWire oneWire(ONE_WIRE_BUS);
float tempMin = 999;
float tempMax = 0;
DallasTemperature sensors(&oneWire);
// ----------------------------------------------------------------------------------------------------
void setup() 
{
// put your setup code here, to run once:
Serial.begin(115200);
Timer1.initialize();
MFS.initialize(&Timer1);
sensors.begin();
// initialize multi-function shield library
MFS.write("co.n.n");
}
// ----------------------------------------------------------------------------------------------------
// here to process incoming serial data after a terminator received
void process_data (char * data)
{

  char *sep_comma, *sep_colon, *command, *attribute_1, *attribute_2, *attribute_3, *attribute_4, *attribute_5;
  uint8_t counter_comma, counter_colon;
  for (counter_comma = 1, sep_comma = strtok_r(data,",", &data); sep_comma != NULL; sep_comma = strtok_r(NULL,",", &data), counter_comma++) 
  {
    for (counter_colon = 1, sep_colon = strtok_r(sep_comma,":", &sep_comma); sep_colon != NULL; sep_colon = strtok_r(NULL,":", &sep_comma), counter_colon++) 
    {
      switch(counter_colon) 
      {
        case 1:
          command = sep_colon;
        case 2:
          attribute_1 = sep_colon;
        case 3:
          attribute_2 = sep_colon;
        case 4:
          attribute_3 = sep_colon;
        case 5:
          attribute_4 = sep_colon;
        case 6:
          attribute_5 = sep_colon;
      }
    }
      // ------------- delay -------------
      if ((strcmp(command,"delay")==0)||(strcmp(command,"sleep")==0)||(strcmp(command,"wait")==0)||(strcmp(command,"dl")==0)||(strcmp(command,"sl")==0))
      {
        MFS.wait(atoi(attribute_1));
        Serial.flush();
        Serial.print(F("[delay]"));
        Serial.print(attribute_1);
        Serial.print(F(";"));
      }
      // ------------- write -------------
      else if ((strcmp(command,"write")==0)||(strcmp(command,"wr")==0))
      {
        MFS.write(attribute_1);
        Serial.flush();
        Serial.print(F("[write]"));
        Serial.print(attribute_1);
        Serial.print(F(";"));
      }
      // ------------- blink -------------
      else if ((strcmp(command,"blink")==0)||(strcmp(command,"bd")==0))
      {
        MFS.blinkDisplay(atoi(attribute_1),atoi(attribute_2));
        Serial.flush();
        Serial.print(F("[blink]"));
        Serial.print(atoi(attribute_1));
        Serial.print(F(","));
        Serial.print(atoi(attribute_2));
        Serial.print(F(";"));
      }
      // ------------- blinkled -------------
      else if ((strcmp(command,"blinkled")==0)||(strcmp(command,"bl")==0))
      {
        MFS.blinkLeds(atoi(attribute_1),atoi(attribute_2));
        Serial.flush();
        Serial.print(F("[blinkled]"));
        Serial.print(atoi(attribute_1));
        Serial.print(F(","));
        Serial.print(atoi(attribute_2));
        Serial.print(F(";"));
      }
      // ------------- led -------------
      else if ((strcmp(command,"led")==0)||(strcmp(command,"ld")==0))
      {
        MFS.writeLeds(atoi(attribute_1),atoi(attribute_2));
        Serial.flush();
        Serial.print(F("[led]"));
        Serial.print(atoi(attribute_1));
        Serial.print(F(","));
        Serial.print(atoi(attribute_2));
        Serial.print(F(";"));
      }
      // ------------- readpot -------------
      else if ((strcmp(command,"readpot")==0)||(strcmp(command,"rp")==0))
      {
        pinMode(0, INPUT);
        Serial.flush();
        float analog = analogRead(0);
        Serial.print(F("@@pot_"));
        Serial.print(analog);
      }
      // ------------- readanalog -------------
      else if ((strcmp(command,"readanalog")==0)||(strcmp(command,"ra")==0))
      {
        pinMode(A5, INPUT);
        Serial.flush();
        float analog = analogRead(A5);
        Serial.print(F("@@analog_"));
        Serial.print(analog);
      }
      // ------------- setpin -------------
      else if ((strcmp(command,"setpin")==0)||(strcmp(command,"sp")==0))
      {
        if ((atoi(attribute_1)) == 5) 
        {
          if ((atoi(attribute_2)) == 0)
          {pinMode(5, OUTPUT); digitalWrite(5, LOW);}
          else
          {pinMode(5, OUTPUT); digitalWrite(5, HIGH);}
        }
        else if ((atoi(attribute_1)) == 6) 
        {
          if ((atoi(attribute_2)) == 0)
          {pinMode(6, OUTPUT); digitalWrite(6, LOW);}
          else
          {pinMode(6, OUTPUT); digitalWrite(6, HIGH);}
        }
        else if ((atoi(attribute_1)) == 9) 
        {
          if ((atoi(attribute_2)) == 0)
          {pinMode(9, OUTPUT); digitalWrite(9, LOW);}
          else
          {pinMode(9, OUTPUT); digitalWrite(9, HIGH);}
        }
        else if ((strcmp(attribute_1,"A5")==0)||(strcmp(attribute_1,"a5")==0))
        {
          if ((atoi(attribute_2)) == 0)
          {pinMode(A5, OUTPUT); digitalWrite(A5, LOW);}
          else
          {pinMode(A5, OUTPUT); digitalWrite(A5, HIGH);}
        }
        Serial.flush();
        Serial.print(F("[setpin]"));
        Serial.print(attribute_1);
        Serial.print(F(","));
        Serial.print(atoi(attribute_2));
        Serial.print(F(";"));
      }
      // ------------- gettemp -------------
      else if ((strcmp(command,"gettemp")==0)||(strcmp(command,"gt")==0))
      {
        sensors.requestTemperatures();
        float tempC = sensors.getTempCByIndex(atoi(attribute_1));
        Serial.flush();
        Serial.print(F("@@temp_"));
        Serial.print(tempC);
        Serial.print(F("_"));
        Serial.print(atoi(attribute_1));
      }
      // ------------- clear -------------
      else if ((strcmp(command,"clear")==0)||(strcmp(command,"cl")==0))
      {
        if ((atoi(attribute_1)) == 0) 
        {
          MFS.write("    "); MFS.blinkDisplay(15,0); MFS.writeLeds(15,0); MFS.blinkLeds(15,0);
          pinMode(5, OUTPUT); digitalWrite(5, LOW);
          pinMode(6, OUTPUT); digitalWrite(6, LOW);
          pinMode(9, OUTPUT); digitalWrite(9, LOW);
          pinMode(A5, OUTPUT); digitalWrite(A5, LOW);
        }
        else if ((atoi(attribute_1)) == 1) {MFS.write("    ");}
        else if ((atoi(attribute_1)) == 2) {MFS.blinkDisplay(15,0);}
        else if ((atoi(attribute_1)) == 3) {MFS.writeLeds(15,0);}
        else if ((atoi(attribute_1)) == 4) {MFS.blinkLeds(15,0);}
        else if ((atoi(attribute_1)) == 5) 
        {
          pinMode(5, OUTPUT); digitalWrite(5, LOW);
          pinMode(6, OUTPUT); digitalWrite(6, LOW);
          pinMode(9, OUTPUT); digitalWrite(9, LOW);
          pinMode(A5, OUTPUT); digitalWrite(A5, LOW);
        }
        else 
        {
          MFS.write("    "); MFS.blinkDisplay(15,0); MFS.writeLeds(15,0); MFS.blinkLeds(15,0);
          pinMode(5, OUTPUT); digitalWrite(5, LOW);
          pinMode(6, OUTPUT); digitalWrite(6, LOW);
          pinMode(9, OUTPUT); digitalWrite(9, LOW);
          pinMode(A5, OUTPUT); digitalWrite(A5, LOW);
        }
        Serial.flush();
        Serial.print(F("[clear]"));
        Serial.print(atoi(attribute_1));
        Serial.print(F(";"));
      }
      // ------------- beep -------------
      else if ((strcmp(command,"beep")==0)||(strcmp(command,"bp")==0))
      {
        MFS.beep(atoi(attribute_1),atoi(attribute_2),atoi(attribute_3),atoi(attribute_4),atoi(attribute_5));
        Serial.flush();
        Serial.print(F("[beep]"));
        Serial.print(atoi(attribute_1));
        Serial.print(F(","));
        Serial.print(atoi(attribute_2));
        Serial.print(F(","));
        Serial.print(atoi(attribute_3));
        Serial.print(F(","));
        Serial.print(atoi(attribute_4));
        Serial.print(F(","));
        Serial.print(atoi(attribute_5));
        Serial.print(F(";"));
      }
      // ------------- help -------------
      else if ((strcmp(command,"help")==0)||(strcmp(command,"-h")==0)||(strcmp(command,"--help")==0))
      {
        if (strcmp(attribute_1,"delay")==0) {Serial.print(F("delay(dl):[miliseconds]"));}
        else if (strcmp(attribute_1,"write")==0) {Serial.print(F("write(wr):[4char]"));}
        else if (strcmp(attribute_1,"blink")==0) {Serial.print(F("blink(bd):[dig1-15]:[bool]"));}
        else if (strcmp(attribute_1,"clear")==0) {Serial.print(F("clear(cl):[0=all,1=dig,2=digblink,3=led,4=ledblink,5=pin]"));}
        else if (strcmp(attribute_1,"led")==0) {Serial.print(F("led(ld):[pin1-15]:[bool]"));}
        else if (strcmp(attribute_1,"blinkled")==0) {Serial.print(F("blinkled(bl):[dig1-15]:[bool]"));}
        else if (strcmp(attribute_1,"beep")==0) {Serial.print(F("beep(bp):[beep ms]:[pause ms]:[repeats]:[loops]:[loop pause ms]"));}
        else if (strcmp(attribute_1,"readpot")==0) {Serial.print(F("readpot(rp)"));}
        else if (strcmp(attribute_1,"readanalog")==0) {Serial.print(F("rereadanalog(ra)"));}
        else if (strcmp(attribute_1,"gettemp")==0) {Serial.print(F("gettemp(gt):[sensor]"));}
        else if (strcmp(attribute_1,"setpin")==0) {Serial.print(F("setpin(sp):[5,6,9 or A5]:[bool]"));}
        else {
               Serial.print(F("Use help:[command] | "));
               Serial.print(F("Commands: delay, write, blink, clear, led, blinkled, beep, readpot, setpin, readanalog, gettemp"));
             }
     }
      else
      {
      // ------------- CMDInvalid -------------
        Serial.flush();
        Serial.print(F("[CMDInvalid]"));
        Serial.print(command);
        Serial.print(F("; "));
        Serial.print(F("Use [help] to list valid commands"));
        Serial.print(F(";"));
      }
  }
Serial.println();
}  // end of process_data
// ----------------------------------------------------------------------------------------------------
void loop() 
{
// put your main code here, to run repeatedly:

static char input_line [MAX_INPUT];
static unsigned int input_pos = 0;

  if (Serial.available () > 0) 
    {
    char inByte = Serial.read ();

    switch (inByte)
      {

      case '\n':   // end of text
        input_line [input_pos] = 0;  // terminating null byte
        
        // terminator reached! process input_line here ...
        process_data (input_line);
        
        // reset buffer for next time
        input_pos = 0;  
        break;

      case '\r':   // discard carriage return
        break;
  
      default:
        // keep adding if not full ... allow for terminating null byte
        if (input_pos < (MAX_INPUT - 1))
          input_line [input_pos++] = inByte;
        break;

      }  // end of switch

    }  // end of incoming data

byte btn = MFS.getButton(); // Normally it is sufficient to compare the return
// value to predefined macros, e.g.BUTTON_1_PRESSED, BUTTON_1_LONG_PRESSED etc.
if (btn)
{
byte buttonNumber = btn & B00111111;
byte buttonAction = btn & B11000000;
Serial.print(F("@@button_"));
Serial.write(buttonNumber + '0');
Serial.print(F("_"));
if (buttonAction == BUTTON_PRESSED_IND)
{
Serial.println("pressed");
}
else if (buttonAction == BUTTON_SHORT_RELEASE_IND)
{
Serial.println("shortrelease");
}
else if (buttonAction == BUTTON_LONG_PRESSED_IND)
{
Serial.println("longpressed");
}
else if (buttonAction == BUTTON_LONG_RELEASE_IND)
{
Serial.println("longrelease");
}
}


// This is the rest of loop
}
// ----------------------------------------------------------------------------------------------------
