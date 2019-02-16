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
*  @ File Name : MultiSensorFutaba.cpp
*  @ Date : 6/12/2013
*  @ Author : Bart Keser
*
*/

#include "SBUS2.h"
#include "SBUS_usart.h"
#include "settings.h"
#include "crc2.h"

static COMMAND_DATA  command;

int main(void)
{
   load_settings();        
   SBUS2_Setup(	SettingsGetCurrentPort(), 
				SettingsGetTempraturePort(), 
				SettingsGetRPMPort(), 
				SettingsGetErrorPort(), 
				SettingsGetCurentCal(),
				SettingsGetNumberofPools());
   SBUS2_uart_command_length(sizeof(COMMAND_STRUCT));   

   while(1)
   {
      SBUS2_loop();
      if(SBUS2_get_command(command.array))
      { 
         if (crc_cal(command.array, sizeof(command)-1) == command.data.crc)
         {// setting command
            if ( doSettingCommand( &command.data ) )
            {
            
            }
            else
            {
               command.data.command1 = C1_ERROR;  
            }            
         }
         else
         {            
            command.data.command1 = C1_ERROR;
         }  
         command.data.crc = crc_cal(command.array, sizeof(command)-1);       
         SBUS2_send_command(command.array);             
      }      
   }
}
