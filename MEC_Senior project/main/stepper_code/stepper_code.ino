// Reference from
// https://lastminuteengineers.com/stepper-motor-l298n-arduino-tutorial/
// For stepper speed control
// https://www.arduino.cc/en/Tutorial/LibraryExamples/StepperSpeedControl
// https://mytectutor.com/l293d-motor-driver-shield-for-arduino/
// https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=roboholic84&logNo=220463437745

// // Include the Arduino Stepper Library
#include <Stepper.h>
#include <AF_Motor.h>

// Number of steps per output rotation
const int stepsPerRevolution = 200;

// Create Instance of Stepper library
AF_Stepper stepper(stepsPerRevolution, 2);


void setup()
{
	// set the speed at 60 rpm:
	stepper.setSpeed(30);
	// initialize the serial port:
	Serial.begin(9600);
}

void loop() 
{
	// // step one revolution in one direction:
	// Serial.println("clockwise");
	// myStepper.step(stepsPerRevolution);
	// delay(100);

	// // step one revolution in the other direction:
	// Serial.println("counterclockwise");
	// myStepper.step(-stepsPerRevolution);
	// delay(100);

	// if(Serial.available()) {
	// 	char ch = Serial.read();

	// 	if(isDigit(ch)) {
	// 		steps = steps * 10 + ch - '0';
	// 	}
	// 	else if(ch == '+') {
	// 		myStepper.step(steps);
	// 		steps = 0;
	// 	}
	// 	else if(ch == '-') {
	// 		myStepper.step(steps * -1);
	// 		steps = 0;
	// 	}
	// }
	if (Serial.read()=='b'){
		stepper.run(100, BACKWARD, SINGLE);
	}
	else if(Serial.read()=='f'){
		stepper.run(100, FORWARD, SINGLE);
	}
	else if(Serial.read()=='s'){
		stepper.run(100, FORWARD, MIRCROSTEP);
	}
	else if(Serial.read()=='r'){
		stepper.run(100, BACKWARD, SINGLE);
	}
	else if(Serial.read()=='l'){
		stepper.run(100, FORWARD, SINGLE);
	}
}
