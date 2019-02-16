
import serial
from time import sleep
import random
import crc

check_device = bytearray((0x55,0x9d,0x01,0xbe,0x46,0xdb,0x64,0xf8))

data = bytearray((0x55,0x9d,0x23,0xbe,0x46,0xdb,0x64,0xf8))



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
ccrc = CRC.CRC_cal(data)
data.append(ccrc)
ccrc = CRC.CRC_cal(check_device)
check_device.append(ccrc)


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
    print (CRC.CRC_cal( (bytearray(response[:-1]) ) ) )
       

sleep(0.2)
counter = 0
while ( counter < 100 ):    	   

    ser.write(data) 
    response = ser.readline()
    str1 =   ':'.join(x.encode('hex') for x in response)
    print(counter)
    print(str1)
    counter = counter +1

