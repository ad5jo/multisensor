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
*  @ File Name : crc2.cpp
*  @ Date : 6/12/2013
*  @ Author : Bart Keser
*
*/

#include <avr/io.h>
#include "crc2.h"

static const unsigned char L[16]={0x00,0x5e,0xbc,0xe2,0x61,0x3f,0xdd,0x83,0xc2,0x9c,0x7e,0x20,0xa3,0xfd,0x1f,0x41};
static const unsigned char H[16]={0x00,0x9d,0x23,0xbe,0x46,0xdb,0x65,0xf8,0x8c,0x11,0xaf,0x32,0xca,0x57,0xe9,0x74};

uint8_t crc_add_byte(uint8_t crc, uint8_t crc_data)
{
   uint8_t i;
   i = (crc_data ^ crc) ;
   crc = L[i&0x0F]^H[i>>4];
   return crc;
}

uint8_t crc_cal( uint8_t data[], uint8_t size)
{
   uint8_t crc = 0;
   
   for (uint8_t i=0; i < size; i++)
   {
      crc = crc_add_byte(crc, data[i]);
   }
   
   return crc;
}