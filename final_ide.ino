#include <Servo.h>

Servo servoX;  // horizontal servo
Servo servoY;  // vertical servo

// LDR pin connections
int LDRTL = A0; // top left
int LDRTR = A1; // top right
int LDRBL = A2; // bottom left
int LDRBR = A3; // bottom right

// Start servo positions
int posX = 90;
int posY = 90;

// Settings
const int tol = 80;        // tolerance to prevent jitter
const int step = 4;        // servo movement step
const int delayTime = 80; // update speed (ms)
const float rightBoost = 1.15; // make right side stronger (tilts more easily)

void setup() {
  Serial.begin(9600);
  servoX.attach(9);
  servoY.attach(10);
  servoX.write(posX);
  servoY.write(posY);
  delay(1000);
}

void loop() {
  int TL = analogRead(LDRTL);
  int TR = analogRead(LDRTR);
  int BL = analogRead(LDRBL);
  int BR = analogRead(LDRBR);

  // Average readings
  int topAvg = (TL + TR) / 2;
  int bottomAvg = (BL + BR) / 2;
  int leftAvg = (TL + BL) / 2;
  int rightAvg = (TR + BR) / 2;

  // Apply slight boost to right LDRs (makes system favor right more)
  rightAvg = rightAvg * rightBoost;

  // ----------- Horizontal Movement -----------
  int diffX = leftAvg - rightAvg;

  if (abs(diffX) > tol) {
    if (diffX > 0) posX -= step;  // more light on left → move left
    else posX += step;             // more light on right → move right
  }

  // ----------- Vertical Movement -----------
  int diffY = topAvg - bottomAvg;

  if (abs(diffY) > tol) {
    if (diffY > 0) posY += step;  // more light on top
    else posY -= step;            // more light on bottom
  }

  // Constrain servo positions
  posX = constrain(posX, 0, 180);
  posY = constrain(posY, 60, 120); // limits tilt range vertically

  // Write servo positions
  servoX.write(posX);
  servoY.write(posY);

  // Send data to Serial Monitor / Python dashboard
  Serial.print(TL); Serial.print(",");
  Serial.print(TR); Serial.print(",");
  Serial.print(BL); Serial.print(",");
  Serial.print(BR); Serial.print(",");
  Serial.print(posX); Serial.print(",");
  Serial.println(posY);

  delay(delayTime);
}