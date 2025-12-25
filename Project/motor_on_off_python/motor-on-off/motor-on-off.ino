int ledPin = 2;

int motor1Pin1 = 27;
int motor1Pin2 = 26;
int enable1Pin = 12;

const int freq = 30000;
const int pwmChannel = 0;
const int resolution = 8;

void setup()
{
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);

  ledcSetup(pwmChannel, freq, resolution);
  ledcAttachPin(enable1Pin, pwmChannel);
}

void loop()
{
  if (Serial.available() > 0) {
    byte speedValue = Serial.read();

    if (speedValue > 0){
      digitalWrite(ledPin, HIGH);
      digitalWrite(motor1Pin1, HIGH);
      digitalWrite(motor1Pin2, LOW);
      ledcWrite(pwmChannel, speedValue);
    }
    else { // Jika speedValue adalah 0
      digitalWrite(ledPin, LOW);
      digitalWrite(motor1Pin1, LOW);
      digitalWrite(motor1Pin2, LOW);
      ledcWrite(pwmChannel, 0);
    }
  }
}

