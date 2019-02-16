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
*  @ File Name : settings.h
*  @ Date : 6/12/2013
*  @ Author : Bart Keser
*
*/


#ifndef SETTINGS_H_
#define SETTINGS_H_

#define C1_ERROR 0xF1

typedef struct
{
   uint16_t  Id;
   uint8_t  command1;
   uint8_t  command2;
   uint32_t data;
   uint8_t  crc;
} COMMAND_STRUCT;

typedef union command_data 
{
   COMMAND_STRUCT data;
   uint8_t        array[sizeof(COMMAND_STRUCT)];
}COMMAND_DATA;

typedef struct
{   
   uint8_t  CurrentPort;
   uint8_t  RPMPort;
   uint8_t  ErrorPort;
   uint8_t  TempraturePort;
   uint8_t  NumberofPools;
   uint8_t  CurrentCal;
   uint8_t  crc;
} SETTINGS;

void load_settings();
bool doSettingCommand(COMMAND_STRUCT *command);
uint8_t SettingsGetCurrentPort();
uint8_t SettingsGetRPMPort();
uint8_t SettingsGetErrorPort();
uint8_t SettingsGetTempraturePort();
uint8_t SettingsGetNumberofPools();
uint8_t SettingsGetCurentCal();

#endif /* SETTINGS_H_ */