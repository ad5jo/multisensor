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
*  @ File Name : CC_esc.h
*  @ Date : 6/12/2013
*  @ Author : Bart Keser
*
*/

#if !defined(_CC_ESC_H)
#define _CC_ESC_H
#include <avr/io.h>

void CCesc_pwm_setup();
void CCesc_Setup(uint8_t number_of_poles);

void CCesc_CheckSequence();
void CCesc_start_servo_pulse(uint16_t SBUS_servo_data );

//void CCesc_SetPWM_high();
//void CCesc_SetPWM_low();

uint32_t CCesc_GetVoltage();
uint32_t CCesc_GetCapacity();
uint32_t CCesc_GetCurrent();
uint16_t CCesc_GetRPM();
uint32_t CCesc_GetTemperature();
	

#endif  //_CC_ESC_H
