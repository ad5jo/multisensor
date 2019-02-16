
import serial
from time import sleep
import random

L = bytearray((0x00,0x5e,0xbc,0xe2,0x61,0x3f,0xdd,0x83,0xc2,0x9c,0x7e,0x20,0xa3,0xfd,0x1f,0x41))
H = bytearray((0x00,0x9d,0x23,0xbe,0x46,0xdb,0x65,0xf8,0x8c,0x11,0xaf,0x32,0xca,0x57,0xe9,0x74))

check_device = bytearray((0x55,0x9d,0x01,0xbe,0x46,0xdb,0x64,0xf8))

data = bytearray((0x55,0x9d,0x23,0xbe,0x46,0xdb,0x64,0xf8))


def crc_add_byte( crc, crc_data ):
	 i = (crc_data ^ crc )
	 crc =  L[i&0x0F]^H[(i>>4)&0x0F]
	 return crc
	 
def crc_cal( data ):
   crc = 0	 
   for var in data:
      crc = crc_add_byte(crc, var)	 
   return crc

ser = serial.Serial()
ser.baudrate = 100000
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_EVEN
ser.stopbits = serial.STOPBITS_TWO
ser.port = 'COM7'
ser.timeout  = 0.04
print("open\n")
ser.open()	
print("opened\n")
crc = crc_cal(data)
data.append(crc)
crc = crc_cal(check_device)
check_device.append(crc)


response = ""
responseid =0

while (responseid != 0x3355 ) :   
    sleep(1)
    ser.setDTR(True)  
    sleep(0.01)    
    ser.setDTR(False)

    while ( not( ser.read() == chr(0xAA))):
        pass
       
    sleep(0.2)
    ser.write(chr(0x55))
    ser.flush()
    ser.write(check_device) 
    response = ser.readline()
    if (len(response) > 2):
        responseid = ord(response[1])   + ( ord(response[0])* 256)
    else:
        responseid = 0
    print (responseid)
    str1 =   ':'.join(x.encode('hex') for x in response)    
    print(str1)
    print (crc_cal(bytearray(response[:-1])))
       

sleep(0.2)
counter = 0
while ( counter < 100 ):    	   

    ser.write(data) 
    response = ser.readline()
    str1 =   ':'.join(x.encode('hex') for x in response)
    print(counter)
    print(str1)
    counter = counter +1

