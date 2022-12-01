// #include <AFMotor.h>

// AF_DCMotor motor(4);

// int incomingData;

// void setup() {
//     Serial.begin(9600);

//     // speed - Valid values for 'speed' are between 0 and 255 with 0 being off and 255 as full throttle
//     motor.setSpeed(255);
//     motor.run(RELEASE);
// }

// void loop() {
//     if(Serial.available() > 0)
// 	{
// 	    incomingData = Serial.read();

//         if (incomingData == 'F') {
//             motor.run(FORWARD);
//         }

//         if (incomingData == 'R') {
//             motor.run(BACKWARD);
//         }

//         if (incomingData == 'Q') {
//             motor.run(RELEASE);
//         }
//     }
// }

#include <Stepper.h>

const int stepRev = 200;
char state;

Stepper stepper(stepRev, 8, 9, 10, 11);
int steps = 0;

void setup() {
    stepper.setSpeed(30);
    Serial.begin(9600);
    Serial.println("Arduino ready.");
}
 
void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available())
  {
    state = Serial.read();
    while (Serial.available())
    {
      Serial.read();  // 첫 번째 문자만 입력받고 나머지는 버린다.
    }
    
    if (state == '0')
    {
        stepper.step(steps);
        steps = 0;
        Serial.println("LED OFF");
    } else
    {
        stepper.step(steps);
        steps = 0;
        Serial.println("LED ON");
    }
  }
  delay(100);
}