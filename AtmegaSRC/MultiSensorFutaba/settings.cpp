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
*  @ File Name : settings.cpp
*  @ Date : 6/12/2013
*  @ Author : Bart Keser
*
*/
#include <avr/eeprom.h>
#include "settings.h"

#define  REPLY_ID                0x3355

#define  C1_CHECK_SYSYEM         0x01
#define  C1_SET_SYSYEM           0x02
#define  C1_SET_ESC              0x03
#define  C1_GET                  0x04
#define  C1_SET                  0x05
#define  C1_SAVE                 0x06

#define  C2_FUTABA               0x01
#define  C2_SPEKTRUM             0x02
#define  C2_JETI                 0x03
#define  C2_GRAPNER_HOT          0x04
#define  C2_HITEC                0x05

#define  C2_CASTLE_CREATIONS_ESC 0x11
#define  C2_JETI_ESC             0x12
#define  C2_GRAUPNER_ESC         0x13

#define  C2_CURRENT_PORT         0x21
#define  C2_RPM_PORT             0x22
#define  C2_ERROR_PORT           0x23
#define  C2_TEMPERATURE_PORT     0x24
#define  C2_NR_POLS              0x25

#define  C2_CAL_CURRENT_CAL      0x31

#define  C2_CAL_VOLTAGE_REV      0x41
#define  C2_CAL_VOLTAGE_MEAS     0x42


uint8_t  EEMEM EEcrc;
uint8_t  EEMEM EECurrentPort;
uint8_t  EEMEM EERPMPort;
uint8_t  EEMEM EEErrorPort;
uint8_t  EEMEM EETempraturePort;
uint8_t  EEMEM EENumberofPools;
uint8_t  EEMEM EECurrentCal;

static SETTINGS settings;

void store_settings()
{ 
   settings.crc = 0xBB;
   eeprom_write_block((const void*)&settings.crc, (void*)&EEcrc, sizeof(uint8_t));
   eeprom_write_block((const void*)&settings.CurrentPort, (void*)&EECurrentPort, sizeof(uint8_t));
   eeprom_write_block((const void*)&settings.RPMPort, (void*)&EERPMPort, sizeof(uint8_t));
   eeprom_write_block((const void*)&settings.ErrorPort, (void*)&EEErrorPort, sizeof(uint8_t));
   eeprom_write_block((const void*)&settings.TempraturePort, (void*)&EETempraturePort, sizeof(uint8_t));
   eeprom_write_block((const void*)&settings.NumberofPools, (void*)&EENumberofPools, sizeof(uint8_t));
   eeprom_write_block((const void*)&settings.CurrentCal, (void*)&EECurrentCal, sizeof(uint8_t));
}

void load_settings()
{
   
   settings.crc               = eeprom_read_byte(&EEcrc);
   if (settings.crc == 0xBB)
   {
      settings.CurrentPort    = eeprom_read_byte(&EECurrentPort);
      settings.RPMPort        = eeprom_read_byte(&EERPMPort);
      settings.ErrorPort      = eeprom_read_byte(&EEErrorPort);
      settings.TempraturePort = eeprom_read_byte(&EETempraturePort);
      settings.NumberofPools  = eeprom_read_byte(&EENumberofPools);
	  settings.CurrentCal     = eeprom_read_byte(&EECurrentCal);
   }
   else
   {
      settings.CurrentPort    = 4;
      settings.RPMPort        = 11;
      settings.ErrorPort      = 10;
      settings.TempraturePort = 15;
      settings.NumberofPools  = 14;
	  settings.CurrentCal     = 100;
   }
}

bool doSettingGet(COMMAND_STRUCT *command)
{
   bool result = false;
   //C2
   switch (command->command2)
   {
      case C2_CURRENT_PORT:  
         command->data = settings.CurrentPort;
         result = true;
         break;
      case C2_RPM_PORT:
         command->data = settings.RPMPort; 
         result = true;
         break;
      case C2_ERROR_PORT:
         command->data = settings.ErrorPort; 
         result = true;         
         break;
      case C2_TEMPERATURE_PORT:
         command->data = settings.TempraturePort; 
         result = true;
         break;
      case C2_NR_POLS:
         command->data = settings.NumberofPools; 
         result = true;
         break;             
	  case C2_CAL_CURRENT_CAL:
		command->data = settings.CurrentCal;
		result = true;
		break;
      default:
         result = false;
   }
   return result;
}

bool doSettingSet(COMMAND_STRUCT *command)
{
   bool result = false;
   
   switch (command->command2)
   {
      case C2_CURRENT_PORT:
         settings.CurrentPort = command->data;
         result = true;
         break;
      case C2_RPM_PORT:
         settings.RPMPort = command->data;
         result = true;
         break;
      case C2_ERROR_PORT:
         settings.ErrorPort = command->data;
         result = true;
         break;
      case C2_TEMPERATURE_PORT:
         settings.TempraturePort = command->data;
         result = true;
         break;
      case C2_NR_POLS:
         settings.NumberofPools = command->data;
         result = true;
         break;
      case C2_CAL_CURRENT_CAL:
      	  settings.CurrentCal = command->data;
      	  result = true;
      	  break;
      default:
         result = false;
   }
   return result;
}

bool doSettingCommand(COMMAND_STRUCT *command)
{
   bool result = false;
   //C1
   switch (command->command1)
   {
      case C1_CHECK_SYSYEM:
         command->command1 = 0;               
         command->command2 = 0;
         command->data     = 0; 
		 result = true;        
         break;
      case C1_SET_SYSYEM:
         break;
      case C1_SET_ESC:
         break;
      case C1_GET:
         result = doSettingGet(command);
         break;
      case C1_SET:
         result = doSettingSet(command);
         break;
      case C1_SAVE:
		 store_settings();
         result = true;
         break;
      default:         
         result = false;
   }
   command->Id = REPLY_ID;

   return result; 
}

uint8_t SettingsGetCurrentPort()
{
	return settings.CurrentPort;
}

uint8_t SettingsGetRPMPort()
{
	return settings.RPMPort;
}

uint8_t SettingsGetErrorPort()
{
	return settings.ErrorPort;
}

uint8_t SettingsGetTempraturePort()
{
	return settings.TempraturePort;
}

uint8_t SettingsGetNumberofPools()
{
	return settings.NumberofPools;
}

uint8_t SettingsGetCurentCal() 
{
	return 117;
}