//stepper code finished 1-5-16
//joystick code finished 1-6-16
// modified for pan code 1-14-16
// modified for tilt code 1-16-16
// joystick code removed to simplify pixy code
//modified for smoother opperation 1-17-16
//modified for pan and tilt calibration 1-23-16
//--apply fixes to code 1-23-16


#include <SPI.h>  
#include <Pixy.h>

//---------stepper code------------------
const int analogInPin0 = A0; //joystick 
const int analogInPin1 = A1; //joystick

const int XstepperPulse = 2;
const int XstepperDirection = 3;
const int XstepperEnable = 4;
const int YstepperPulse = 5;
const int YstepperDirection = 6;
const int YstepperEnable = 7;
const int XstopBit = 22;
const int YstopBit = 24;


int StepDelay1 = 0;// 0 is fastest
int StepDelay2 =1;// 1 is fastest
int StepDelay3=0;
int sensorValue0 = 0; //joystick
int sensorValue1 = 0; //joystick
int Xhome=1600;
int Yhome=1000;
int gg=0;
int dd=2;
int ee = 0;
int ff = 0;
int tt=0;
int panSpan =0;
int tiltSpan=0;
int panMove=0;
int panStop=0;
int xStop=1;
int yStop=1;
int kk=2;
int Xcal=0;
int Ycal=0;
int follow=0;
//----------------end stepper code------------


//--------------- camera code 
int pan = 0;
int tilt = 0;
// This is the main Pixy object 
Pixy pixy;
//------------------ end camera code-----------



void setup()
{
// Serial.begin(9600);
//  Serial.print("Starting...\n");
//-----------------stepper setup code---------------------  
  pinMode(XstepperPulse, OUTPUT);
  pinMode(XstepperDirection, OUTPUT);
  pinMode(XstepperEnable, OUTPUT);
  pinMode(XstopBit, INPUT_PULLUP);
  digitalWrite (XstepperEnable, LOW);

  pinMode(YstepperPulse, OUTPUT);
  pinMode(YstepperDirection, OUTPUT);
  pinMode(YstepperEnable, OUTPUT);
  pinMode(YstopBit, INPUT_PULLUP);
  digitalWrite (YstepperEnable, LOW);
//------------end stepper setup code---------------

  pixy.init();
  delay(200);
  
  //--------------------------------------------
  
//Serial.begin(9600);
// delay (300); 
  

//----------initilize camera pan and tilt------
do
{
  digitalWrite (XstepperDirection, HIGH);
  digitalWrite (XstepperPulse, HIGH);
  delay (StepDelay1);
  digitalWrite (XstepperPulse, LOW);
  delay (StepDelay2);
  xStop = (digitalRead(XstopBit));
} while (xStop==1);

for (panSpan=0; panSpan<5700; panSpan++)
{
  digitalWrite (XstepperDirection, LOW);
  digitalWrite (XstepperPulse, HIGH);
  delay (StepDelay1);
  digitalWrite (XstepperPulse, LOW);
  delay (StepDelay2);
}
//--------------find tilt home----------------------


do
{
  digitalWrite (YstepperDirection, LOW);
  digitalWrite (YstepperPulse, HIGH);
  delay (StepDelay1);
  digitalWrite (YstepperPulse, LOW);
  delay (StepDelay2);
  yStop = (digitalRead(YstopBit));
} while (yStop==1 );

for (tiltSpan=0; tiltSpan<3500; tiltSpan++)
{
  digitalWrite (YstepperDirection, HIGH);
  digitalWrite (YstepperPulse, HIGH);
  delay (StepDelay1);
  digitalWrite (YstepperPulse, LOW);
  delay (StepDelay2);
}


}

void loop()
{ 
//-------------------main loop------------------
  int j;
  uint16_t blocks;
  char buf[32];  
  
  // grab blocks!
  blocks = pixy.getBlocks();
  
  gg++;
  if (gg >5)// pixy asks for data
  { 
      pan=(((pixy.blocks[j].x)*10)+1);
      tilt=(((pixy.blocks[j].y)*10.3)+1);
      gg=0;
      
      if (blocks==1) { follow = 2000;}// the follow value counts down while program loops.  
                                      // If object is lost then the follow value will
                                      // count down to zero and the camera stops moving. 
                                     //  A value of 3000 is about 1.5 seconds
          
  }
   
  follow--; // follow counts down. if value not refreshed then camera will stop moving
  
  if (follow== 0){follow=1;} // keeps value from going below zero

  if (follow>3)// as long as follow is above 3 then the pan and tilt will opperate.
             // this if statement is huge and contains all pan and tilt code.
  {

    ff++;// counter to slow pan movement

    if (ff>3)// when value is reached code for stepper is run 1 cycle
    {
 
  
//------pan code----------------  
      if (pan > (Xhome+20))
      {
        panMove=1;// flag set to modify speed for tilt
        digitalWrite (XstepperDirection, LOW);
        digitalWrite (XstepperPulse, HIGH);
        delay (StepDelay1);
        digitalWrite (XstepperPulse, LOW);
        delay (StepDelay2);
      }
      if (pan < (Xhome -20))
      {
        panMove=1;  // flag set to modify speed for tilt
        digitalWrite (XstepperDirection, HIGH);
        digitalWrite (XstepperPulse, HIGH);
        delay (StepDelay1);
        digitalWrite (XstepperPulse, LOW);
        delay (StepDelay2);
      }
    ff=0; //resets loop counter for pan stepper 
    }
//--------------end pan code-------------------


//--------------TILT CODE-----------------------------------------

    ee++;

    if (ee>panMove)// if the pan is moving then tilt controls are spead up for smooth action .
    {
      if (tilt > (Yhome +30))
      {
        digitalWrite (YstepperDirection, LOW);
        digitalWrite (YstepperPulse, HIGH);
        delay (StepDelay3);
        digitalWrite (YstepperPulse, LOW);
        delay (StepDelay3);
      }
      if (tilt < (Yhome -30))
      {
        digitalWrite (YstepperDirection, HIGH);
        digitalWrite (YstepperPulse, HIGH);
        delay (StepDelay3);
        digitalWrite (YstepperPulse, LOW);
        delay (StepDelay3);
      }
    ee=0;
    }
//------------END TILT CODE-----------------------------------------
    panMove=25; // when pan is not moving, this value will slow the tilt for smooth action




//Serial.println (pan);
//Serial.println ("");
//Serial.println (Xhome);

//delay (2);
      
  }
}
