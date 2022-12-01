#include <Pixy2.h>
#include <PIDLoop.h>

Pixy2 pixy;
PIDLoop panLoop(400, 0, 40, true);
PIDLoop tiltLoop(500, 0, 500, true);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.print("Startin...\n");

  // initialize pixy object
  pixy.init();
  // use color connected components program for the pan tilt to track
  pixy.changeProg("color_connected_components");
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
}
