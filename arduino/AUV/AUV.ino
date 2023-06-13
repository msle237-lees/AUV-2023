#define NUM_BUTTONS 10

const int buttonPins[NUM_BUTTONS] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11}; 
const int joystickPins[6] = {A0, A1, A2, A3, A4, A5}; 
bool buttonStates[NUM_BUTTONS]; 

void setup() {
  Serial.begin(9600); 
  for (int i = 0; i < NUM_BUTTONS; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP); 
  }
}

void loop() {
  int joystickValues[6];
  for (int i = 0; i < 6; i++) {
    joystickValues[i] = analogRead(joystickPins[i]);
  }

  for (int i = 0; i < NUM_BUTTONS; i++) {
    buttonStates[i] = digitalRead(buttonPins[i]);
  }

  sendValues(joystickValues, buttonStates);
  delay(10); 
}

void sendValues(int joystickValues[], bool buttonStates[]) {
  for (int i = 0; i < 6; i++) {
    Serial.print(joystickValues[i]);
    Serial.print(",");
  }
  
  for (int i = 0; i < NUM_BUTTONS; i++) {
    Serial.print(buttonStates[i] == HIGH ? "False" : "True");
    if (i < NUM_BUTTONS - 1) {
      Serial.print(",");
    }
  }

  Serial.println();
}
