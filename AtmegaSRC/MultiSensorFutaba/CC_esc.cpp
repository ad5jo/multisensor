/*
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*  @ Project : MultiSensor
*  @ File Name : CC_esc.cpp
*  @ Date : 6/12/2013
*  @ Author : Bart Keser
*
*/
#define NO_ARDUINO_TIMER

#include <avr/interrupt.h>

#include "myavr.h"
#include "CC_esc.h"


#define MA_FILTER_SIZE 5
#define TIMEOUT_DATA  6000

//Local definitions

#define ENABLE_TIMER1_FOR_PWM  0x09 // WGM12 and CS10 set CTC mode prescaller 1
#define ENABLE_TIMER1_FOR_PULS_MEASURE  0x0A // WGM12 and CS11 set CTC mode prescaller 1

#define ESC_PIN  PIN_3

// hash table with precalculed ntc temperatures
#define TEMP_NTC_SUB_INDEX 100 // 100 us per index
// table is temperature (mC) based on ms ( 1 index is 100us no float calclations ( way to slow )
int32_t tempNtc[] = {744254,157334,121860,103184,90615,81153,73550,67174,61659,56778,52379,48355,44628,41140,
                  37846,34708,31698,28789,25961,23194,20470,17773,15086,12393,9676,6916,4092,1178,-1858,
                  -5056,-8470,-12176,-16288,-20990,-26612,-33862,-44821,-81963
                 };

typedef enum
{
    FRAME_SYNC =  0,
    FRAME_REFERENCE,
    FRAME_VOLTAGE,
    FRAME_RIPPLE_VOLTAGE,
    FRAME_CURRENT,
    FRAME_THROTTLE,
    FRAME_OUTPUT_POWER,
    FRAME_RPM,
    FRAME_BEC_VOLTAGE,
    FRAME_BEC_CURRENT,
    FRAME_TEMP1,
    FRAME_TEMP2
} ENUM_FRAMES;


// local varibles
uint8_t numberOfPoles = 1;
uint32_t validVoltage;
uint32_t validRippleVoltage; 
uint32_t validCurrent;
uint32_t validRpm;
int32_t validTemperature;

// function definitions
inline void NoPulsTimeout();
inline void ResetRefTimer();
inline void StartRefTimer();

volatile ENUM_FRAMES dataFrame;
volatile uint8_t     refTimer = 0;
volatile uint16_t    pulseLength = 0;


void CCesc_pwm_setup()
{
    TCCR1A = 0;               // normal counting mode
    TCCR1B = 0;               // stop counter
    TCNT1 = 0;                // clear the timer count
    TIFR1 = 0;                // clear any pending interrupts;
    TIMSK1 = 0x03;            // enable the output compare interrupt
    PinDasOutput(ESC_PIN);
    PinCasOutput(PIN_4);
    PinCasOutput(PIN_5);
}

inline void StopRefTimer()
{
    TCCR0B = 0;
}

inline void ResetRefTimer()
{
    TCNT0 = 0;
    refTimer = 0;
}

inline void StartRefTimer()
{
    TCCR0B |=  (1<<CS00);
 //   PinCOutput( PIN_4, LOW);
//    PinCOutput( PIN_5, LOW);
}

void SetupRefTimer()
{
    StopRefTimer();// stop counter
    TCCR0A = 0;// normal counting mode
    TCCR0B = 0;// normal counting mode and stop timer
    TIMSK0 |= (1<<TOIE0);// enable overflow interrupt
    TIFR0  = 0; // clear any pending interrupts;
}

ISR(TIMER0_OVF_vect)
{
    refTimer++;

    if ( refTimer == 0)
    {
        NoPulsTimeout();        
//PinCOutput( PIN_4, HIGH);
    }
}

ISR(TIMER1_COMPA_vect)
{
    PinDOutput( ESC_PIN, HIGH);
    PinDasInput(ESC_PIN);
    TCCR1B = 0; // stop pwm timer timer
    ResetRefTimer();
    StartRefTimer();
    pulseLength = 0;
    EIFR &= ~(0x00);
    EIMSK |= 0x02; // enable int1 interrupt

    TIFR1 = 0;// clear any pending interrupts;

    PinCOutput( PIN_4, HIGH);
}


void CCesc_start_servo_pulse(uint16_t SBUS_servo_data )
{
    uint16_t comp_reg = ((1000 + SBUS_servo_data) * 24) / 4;
    pulseLength = 0; //ready for next Data
    TCNT1 = 0;
    OCR1A = comp_reg;

    PinDOutput( ESC_PIN, HIGH);
    PinDasOutput(ESC_PIN);
    PinDOutput( ESC_PIN, LOW);

    TCCR1B = ENABLE_TIMER1_FOR_PWM;
}


void setupCaptureEscData()
{
    EICRA |=  (1<<ISC11);
    EICRA &=  ~(1<<ISC10);
    PCMSK2 |= (1<<ESC_PIN);
}

void CCesc_Setup(uint8_t number_of_poles)
{
    //CapRefTime = micros();

    // interrupts when the ESC signal the its data tick
    // this tick occurs between 0.5 e 5.5 milliseconds after the signal sent
    numberOfPoles = number_of_poles;
    SetupRefTimer();
    setupCaptureEscData();
}

uint32_t CCesc_GetVoltage()
{
    return validVoltage;
}

uint32_t CCesc_GetCurrent()
{
    return validCurrent;
}

uint16_t CCesc_GetRPM()
{
    return validRpm;
}

uint32_t CCesc_GetTemperature()
{
    // returns milli Degrees celsius
    return validTemperature;
}


/*
void CCesc_SetPWM_high()
{
digitalWrite(ESC_PIN, HIGH);
// digitalWrite(13, LOW);
// setup the ESC's port to read mode, since a pulse will be output in no more than 6 ms
pinMode(ESC_PIN, INPUT);
// saves the current time, to calculate the elapsed time to the tick output by the ESC
StartRefTime = micros();
}

void CCesc_SetPWM_low()
{
pinMode(ESC_PIN, OUTPUT);
digitalWrite(ESC_PIN, LOW);
}*/


inline void NoPulsTimeout()
{
    StopRefTimer();
    EIMSK &= ~(0x02); // disable int1 interrupt
    dataFrame = FRAME_SYNC;
    pulseLength = 0;
//PinCOutput( PIN_4, HIGH);

}


ISR(INT1_vect)
{
    //get timer status
    StopRefTimer();
    pulseLength = TCNT0;
    pulseLength += ((uint16_t)refTimer)<<8 ;
    EIMSK &= ~(0x02); // disable int1 interrupt    
}

uint32_t det_value( uint32_t offset0_5,  uint32_t value)
{
    uint32_t new_value = 0;

    if (value > offset0_5)
        new_value = value - offset0_5;

    return new_value;
}

void CCesc_CheckSequence()
{
    static uint16_t reference1ms = 1000;
    static uint16_t offset0_5    = 500;

    // local varibles
    static uint32_t voltage;
    static uint32_t current;
    static uint32_t rpm;
    static int32_t temperature;    

    static uint32_t temp1;
    static uint32_t temp2;
    
    // if there is no new pulse time don't do anything
    if (pulseLength != 0)
    {
        PinCOutput( PIN_5, HIGH);
        dataFrame = (ENUM_FRAMES)((int)dataFrame+1);
        
        switch (dataFrame)
        {
            case FRAME_REFERENCE:
                // moving average filter on 1ms pulse 
                reference1ms = ((reference1ms * 7) + (pulseLength/8)) /8;
                break;
            case FRAME_VOLTAGE:
                //result is mV
                voltage = det_value( (reference1ms/2)*8, pulseLength ) * 20000L / reference1ms/8;                
                break;
            case FRAME_CURRENT:
                // result is mA
                current = det_value( (reference1ms/2)*8, pulseLength ) * 50000L / reference1ms/8 ;                
                break;
            case FRAME_RPM:                
                if ((pulseLength/8) > (offset0_5+10) )
                {
                    rpm = ((det_value((reference1ms/2)*8, pulseLength) * 20417) / reference1ms / (numberOfPoles/2)/8) ;   
                }
                else
                {               
                    rpm = 0;
                }                     
                break;
            case FRAME_TEMP1:
                temp1 = pulseLength;
                break;
            case FRAME_TEMP2:
                temp2 = pulseLength;
                // according to the Castle Link Live's protocol manual:
                // -- "Temperature is measured in one of two ways, and embedded temp sensor or an external
                // -- NTC resistor. Only one of these two data fields will have valid data (greater than 0.5ms).
                // -- If the controller is NTC type, logarithmic math is required to do the conversion."
                // We are not going to calculate logarithmic here. Instead, we gonna use a loo table
                // with pre-calculated temperatures, interpolating the in-between values.
                if (temp1 > temp2)
                {
                    temperature = det_value( offset0_5, temp1/8 ) * 30000L / reference1ms;
                    // save new offset
                    
                   offset0_5 = (((offset0_5 * 7) + (temp2/8)) /8);                   
                }
                else
                {
                    uint32_t temp = (det_value( offset0_5, temp2/8 ) * 1000) / reference1ms;
                    uint8_t  index = (temp / TEMP_NTC_SUB_INDEX) - 1;
                    int      rest = temp % TEMP_NTC_SUB_INDEX;

                    if (index >= 0 && index < (sizeof(tempNtc) / sizeof(int32_t)))
                    {
                        int32_t tempAbove = tempNtc[index];
                        int32_t tempBelow = tempNtc[index + 1];
                        temperature = tempAbove + (((tempBelow - tempAbove ) * rest) / TEMP_NTC_SUB_INDEX );                        
                    }
                    else
                    {
                        temperature = 0;
                    }                     
                    // save new offset, with moving average filter                    
                    offset0_5 = ((offset0_5 * 7) + (temp1/8)) /8;
                }                
                
                // Data is valid so copy to telemetry data 
                validVoltage = voltage;
                validCurrent = current;
                validRpm = rpm;
                validTemperature = temperature/1000;               
                break;
            default:
                break;
        }
        pulseLength = 0;
        PinCOutput( PIN_5, LOW);
    }
    
}
