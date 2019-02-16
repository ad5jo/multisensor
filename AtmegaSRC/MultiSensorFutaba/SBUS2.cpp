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
*  @ File Name : SBUS2.cpp
*  @ Date : 6/12/2013
*  @ Author : Bart Keser
*
*/

#include "SBUS2.h"
#include "SBUS_usart.h"
#include "CC_ESC.h"

#define SBUS2_TEL_DATA_SIZE        3
#define CURRENT_SENSOR_SLOT     0x04
#define TEMPERATURE_SENSOR_SLOT 0x0A
#define RPM_SENSOR_SLOT         0x0A

static void     do_servo_pulse_callback(uint32_t counter);

// absolute timer for capacity calculation
static volatile uint32_t  absTime        = 0;
static volatile bool      do_servo_pulse = false;

static uint8_t currentPort     = 0;
static uint8_t temperaturePort = 0;
static uint8_t rpmPort         = 0;
static uint8_t alarmPort       = 0;
static uint8_t currentCal      = 100;

void SBUS2_Setup(uint8_t current_port, 
				 uint8_t temperature_port, 
				 uint8_t rpm_port, 
				 uint8_t alarm_port, 
				 uint8_t current_cal,
				 uint8_t number_of_poles
				 )
{
   currentPort     = current_port;
   temperaturePort = temperature_port;
   rpmPort         = rpm_port;
   alarmPort       = alarm_port;
   currentCal      = current_cal;
   SBUS2_uart_setup(do_servo_pulse_callback);
   CCesc_pwm_setup();
   CCesc_Setup(number_of_poles);
}

void send_RPM(uint16_t RPM)
{
   int16_t value =  0;
   uint8_t bytes[SBUS2_TEL_DATA_SIZE] = {0x13, 0x00, 0x00 };

   value =  RPM / 6;
   bytes[2] = value >> 8;
   bytes[1] = value;
   SBUS2_transmit_telemetry_data( rpmPort , bytes);
}

void send_temp125(int16_t temp)
{
   int16_t value=  0;
   uint8_t bytes[SBUS2_TEL_DATA_SIZE] = {0x13, 0x40, 0x00 };

   value = temp | 0x4000;
   bytes[1] = value >> 8;
   bytes[2] = value;
   SBUS2_transmit_telemetry_data( temperaturePort , bytes);
}

void send_alarm_as_temp125(int16_t alarm)
{
   int16_t value=  0;
   uint8_t bytes[SBUS2_TEL_DATA_SIZE] = {0x13, 0x40, 0x00 };

   value = alarm | 0x4000;
   bytes[1] = value >> 8;
   bytes[2] = value;
   SBUS2_transmit_telemetry_data( alarmPort , bytes);
}


void send_s1678_current(uint16_t current, uint16_t capacity, uint16_t voltage)
{
   uint16_t value = 0;
   uint32_t local = 0;
   uint8_t bytes[SBUS2_TEL_DATA_SIZE] = {0x03, 0x40, 0x00 };
 
   
   // CURRENT
   local = ((uint32_t)current * 117) / 100 ;
   value = (uint16_t)local;   
   if ( value > 0x3FFF )
   {
      // max current is 163.83
      value = 0x3FFF;
   }  
   bytes[1] = value >> 8;
   bytes[1] = bytes[1] | 0x40;
   bytes[1] = bytes[1] & 0x7F;
   bytes[2] = value;
   SBUS2_transmit_telemetry_data( currentPort , bytes);

   //VOLTAGE
   local = ((uint32_t)voltage * 105) / 100;
   value = (uint16_t)local;   
   bytes[1] = value >> 8;
   bytes[2] = value;
   SBUS2_transmit_telemetry_data( currentPort+1 , bytes);

   // CAPACITY
   local = ((uint32_t)capacity * currentCal) / 100;
   value = (uint16_t)local;   
   bytes[1] = value >> 8;
   bytes[2] = value;
   SBUS2_transmit_telemetry_data( currentPort+2 , bytes);
}

void do_servo_pulse_callback(uint32_t counter)
{
   do_servo_pulse = true;
   absTime = counter;
}

uint16_t CalCapacity(uint32_t current_mA)
{
   // uAh
   static uint32_t usedCapacity = 0;
   static uint32_t refTimer =  0;

   uint32_t addUsedCapacity = 0;

   uint32_t deltaTime_ms = absTime - refTimer;
   refTimer = absTime;

   addUsedCapacity =  current_mA * deltaTime_ms / 3600;

   usedCapacity = usedCapacity + addUsedCapacity;
   return usedCapacity / 1000;
}


void SBUS2_loop()
{
   int16_t channel = 0;
   uint16_t uart_dropped_frame = false;
   bool transmision_dropt_frame = false;
   bool failsave = false;

   if (do_servo_pulse)
   {
      do_servo_pulse = false;

      channel = SBUS2_get_servo_data( 2 );
      if (channel != -1 )
      {
         if ( alarmPort != 0 )
         {
            SBUS2_get_status(&uart_dropped_frame, &transmision_dropt_frame, &failsave);
            send_alarm_as_temp125( (failsave*1000) + (transmision_dropt_frame*100) + uart_dropped_frame);
         }
         CCesc_start_servo_pulse(channel);

         send_temp125(CCesc_GetTemperature());
         //send_temp125(absTime/1000);
         send_s1678_current((uint16_t)(CCesc_GetCurrent()/10),
                            (uint16_t)CalCapacity(CCesc_GetCurrent()),
                            (uint16_t)(CCesc_GetVoltage()/10));
         send_RPM(CCesc_GetRPM());         

      }
   }
   
   CCesc_CheckSequence();
}


