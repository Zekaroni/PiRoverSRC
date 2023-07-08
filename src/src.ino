#include <stdio.h>
#include <AFMotor.h>

/*
NOTES:
    - The reason some information that will only populate a couple bits uses an entire byte is because
    with most cpu architecture, it is harder to manipulate data underthing since the cpu is built to
    interact with at least a byte.
    - When using .run(), the predefined values for FORWARD and BACKWARD are 1 and 2 respective.
    - When rewritting, I decided to leave

TODO:
    - Create a way to have the Motors struct and actual motor objects be called from the same parent


Data input layout:
    unsigned 16 bit (uint16_t)
        10101           00           0       00000000
    VerifyIncoming, Motor number, Direction,  Speed
*/


// Datatypes

struct InformationBytes
{// This is a struct and union for the incoming data from the Raspberry Pi.
    uint8_t Speed;
    uint8_t Direction: 1;
    uint8_t MotorNumber: 2;
    uint8_t Verification: 5;
};

union IntUnion
{
    InformationBytes Data;
    uint16_t rawBits;
};


// Declarations

AF_DCMotor Motor1(1),Motor2(2),Motor3(3),Motor4(4);                // Objects linked to the actual motors using the AF_Motor lib
AF_DCMotor* MotorCluster[4] = {&Motor1, &Motor2,&Motor3, &Motor4}; // Array of pointers to motors for indexing the motors

IntUnion receivedData;                                             // Variable used to store incoming data from Pi
byte byte1, byte2;                                                 // Declaration of the bytes being used in data transmition
byte verificationBits = 0b10101;                                   // Bits that are used to check incoming serial. ONLY 5 BITS


// Functions

void activateMotor(){
    // TODO: Add directional motor
    if (receivedData.Data.Speed)
    { // Called if speed is non-zero
        MotorCluster[receivedData.Data.MotorNumber]->run(receivedData.Data.Direction+1); // Starts the motor (direction TBA)
        MotorCluster[receivedData.Data.MotorNumber]->setSpeed(receivedData.Data.Speed);  // Sets speed of motor
    } else 
    { // Called when speed is 0
        MotorCluster[receivedData.Data.MotorNumber]->run(RELEASE);         // Better way to turn off motor than setting speed to 0
    }
};

bool validateStartingByte(byte inByte, byte searchPattern)
{
  // Mask the first 5 bits of the byte, starting from the fourth bit
  unsigned char maskedBits = (inByte >> 3);
  return maskedBits == searchPattern;
}


// Main Arduino code

void setup()
{
    Serial.begin(9600); // Begins serial 
}

void loop()
{
    if (Serial.available() >= 2)
    {
        byte byte1 = Serial.read();
        if (validateStartingByte(byte1, verificationBits))
        {
            receivedData.rawBits = 0x0000; // Clears anything in receivedData
            receivedData.rawBits = byte1 << 8;
            receivedData.Data.Speed = Serial.read();
            Serial.println(receivedData.rawBits, BIN);
            activateMotor();
        }
    }
}
