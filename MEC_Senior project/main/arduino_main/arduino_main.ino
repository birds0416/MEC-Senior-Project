#include <Pixy2.h>
#include <PIDLoop.h>
#include <Stepper.h>

#define STEPS 200

Pixy2 pixy;
PIDLoop panLoop(400, 0, 40, true);
PIDLoop tiltLoop(500, 0, 500, true);

Stepper step(STEPS, 8, 9, 10, 11); //for arduino uno

// for Arduino nano, Stepper.h is not used
// const int EN = 2;   // ENABLE PIN
// const int Step = 3; // STEP PIN
// const int dir = 4;  // DIRECTION PIN

void setup() {
  // for arduino uno
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.print("Startin...\n");

  // initialize pixy object
  pixy.init();
  // use color connected components program for the pan tilt to track
  pixy.changeProg("color_connected_components");

  // for arduino nano
  // pinMode(EN, OUTPUT);    // ENABLE as OUTPUT
  // pinMode(dir, OUTPUT);   // DIRECTION as OUTPUT
  // pinMode(Step, OUTPUT);  // STEP as OUTPUT
  // digitalWrite(EN, LOW);  // Set ENABLE to LOW
}

void loop() {
  // put your main code here, to run repeatedly:
  static int i = 0;
  int j;
  char buf[64];
  int32_t panOffset, tiltOffset;

  // get active blocks from Pixy
  pixy.ccc.getBlocks();

  if(pixy.ccc.numBlocks)
  {
    i++;

    if(i % 60 == 0)
    {
      Serial.println(i);
    }

    // calculate pan and tilt "errors" with respect to first object (blocks[0]), which is the biggest object (sorted by size)
    panOffset = (int32_t)pixy.frameWidth / 2 - (int32_t)pixy.ccc.blocks[0].m_x;
    tiltOffset = (int32_t)pixy.ccc.blocks[0].m_y - (int32_t)pixy.frameHeight / 2;

    // update loops
    panLoop.update(panOffset);
    tiltLoop.update(tiltOffset);

    // set pan and tilt servos
    pixy.setServos(panLoop.m_command, tiltLoop.m_command);

#if 0 // for debugging
  sprintf(buf, "%ld %ld %ld", rotateLoop.m_command, translateLoop.m_command, left, right);
  Serial.println(buf);
#endif
  }
  else
  {
    panLoop.reset();
    tiltLoop.reset();
    pixy.setServos(panLoop.m_command, tiltLoop.m_command);
  }

  // for arduino nano, stepper motor control example
  // digitalWrite(dir,LOW);        // SET DIRECTION LOW FOR FORWARD ROTATION

  // for(int x = 0; x < 1000; x++) // LOOP 1000 TIMES FOR 1000 RISING EDGE ON STEP PIN
  // {
  //   digitalWrite(Step,HIGH);    // STEP HIGH
  //   delay(1);                   // WAIT
  //   digitalWrite(Step,LOW);     // STEP LOW
  //   delay(1);                   // WAIT
  // }

  // delay(10);                    // DELAY BEFOR SWITCH DIRECTION
  // digitalWrite(dir,HIGH);       // SET DIRECTION HIGH FOR BACKWARD ROTATION

  // for(int x = 0; x < 1000; x++) // LOOP 1000 TIMES FOR 1000 RISING EDGE ON STEP PIN
  // {
  //   digitalWrite(Step,HIGH);    // STEP HIGH
  //   delay(1);                   // WAIT
  //   digitalWrite(Step,LOW);     // STEP LOW
  //   delay(1);                   // WAIT
  // }

  // delay(10);                    // DELAY BEFOR SWITCH DIRECTION

}
