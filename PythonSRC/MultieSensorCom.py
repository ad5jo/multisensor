import serial
from time import sleep
import crc
import struct

class Interface:
    REPLY_ID                = 0x5533
    DEVICE_ID               = 0x55
    C1_CHECK_SYSYEM         = 0x01
    C1_SET_SYSYEM           = 0x02
    C1_SET_ESC              = 0x03
    C1_GET                  = 0x04
    C1_SET                  = 0x05
    C1_SAVE                 = 0x06

    C2_FUTABA               = 0x01
    C2_SPEKTRUM             = 0x02
    C2_JETI                 = 0x03
    C2_GRAPNER_HOT          = 0x04
    C2_HITEC                = 0x05

    C2_CASTLE_CREATIONS_ESC = 0x11
    C2_JETI_ESC             = 0x12
    C2_GRAUPNER_ESC         = 0x13

    C2_CURRENT_PORT         = 0x21
    C2_RPM_PORT             = 0x22
    C2_ERROR_PORT           = 0x23
    C2_TEMPERATURE_PORT     = 0x24
    C2_NR_POLS              = 0x25

    C2_CAL_CURRENT_CAL      = 0x31    

    C2_CAL_VOLTAGE_REV      = 0x41
    C2_CAL_VOLTAGE_MEAS     = 0x42
    
    def __init__(self, comport):        
        self.CRC = crc.Crc()
        self.check_device = bytearray((0x55,0x9d,0x01,0xbe,0x46,0xdb,0x64,0xf8))
        ccrc = self.CRC.CRC_cal(self.check_device)
        self.check_device.append(ccrc)
        self.ser = serial.Serial()
        self.ser.baudrate = 100000
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_EVEN
        self.ser.stopbits = serial.STOPBITS_TWO
        self.ser.port = comport
        self.ser.timeout  = 0.04
    
    def openport(self):
        try:  
            print("open\n")
            self.ser.open()	
            print("opened\n")      
            return True
        except ValueError:
            return False
            
    def connect(self):
        tries = 10
        response = ""
        responseid =0

        while ((responseid != self.REPLY_ID) & (tries > 0)) :   
            sleep(1)
            self.ser.setDTR(True)  
            sleep(0.01)    
            self.ser.setDTR(False)

            while ( not( self.ser.read() == chr(0xAA))):
                pass
               
            sleep(0.2)
            self.ser.write(chr(0x55))
            self.ser.flush()
            self.ser.write(self.check_device) 
            response = self.ser.readline()
            if (len(response) > 2):
                responseid = ord(response[1])   + ( ord(response[0])* 256)
            else:
                responseid = 0
            print (responseid)
            str1 =   ':'.join(x.encode('hex') for x in response)    
            print(str1)            
            tries = tries -1

        sleep(0.2)
        if ( tries == 0 ):
            return -1
        else:
            return 0

    def SendCommandRaw(self, data):
        crc1_response = 1
        crc2_response = 0
        tries = 10
        response = bytearray(0x00)
        if ( len(data) == 8):
            ccrc = self.CRC.CRC_cal(data)
            data2 = data[:]
            data2.append(ccrc)
            while ((not(len(response) == 9)) & (tries > 0) & (not(crc1_response == crc2_response)) ):
                
                self.ser.write(data2) 
                response = self.ser.readline()
                str1 =   ':'.join(x.encode('hex') for x in response)            
                print(str1)
                if ( len(response) == 9 ):
                    crc1_response = self.CRC.CRC_cal( (bytearray(response[:-1]) ) )
                    crc2_response = ord(response[8])
                tries = tries - 1
        if ( tries == 0 ):
            return bytearray(0x00)
        else:
            return response[:-1]
      
    def SendCommandInt(self, deviceid, groupaction, action , data=0xFFFFFFFF):
        raw_data = bytearray()                       
        raw_data.append(chr((deviceid & 0xFF00) / 256 ))
        raw_data.append(chr( deviceid & 0x00FF ))
        
        raw_data.append(chr(groupaction))
        raw_data.append(chr(action))

        raw_data.append(chr( data & 0x000000FF ))
        raw_data.append(chr((data & 0x0000FF00) / 256 ))        
        raw_data.append(chr((data & 0x00FF0000) / 65536 ))
        raw_data.append(chr((data & 0xFF000000) / 16777216 ))
        
        response = self.SendCommandRaw(raw_data)
        
        resp_deviceid    = ord(response[1]) + ( ord(response[0]) * 256 )
        resp_groupaction = ord(response[2])
        resp_action      = ord(response[3])
        resp_data        = ord(response[4]) + ( ord(response[5]) * 256 ) + ( ord(response[6]) * 65536 ) + ( ord(response[7]) * 16777216 )
        if (resp_data > 2147483648):
            resp_data = resp_data - 4294967296
      
        return resp_deviceid, resp_groupaction, resp_action, resp_data

    def SendCommandFloat(self, deviceid, groupaction, action , data):
        raw_data = bytearray()

        print struct.unpack("<L", struct.pack('f', 2.5) )[0]
        
        raw_data.append(chr((deviceid & 0xFF00) / 256 ))
        raw_data.append(chr( deviceid & 0x00FF ))
        
        
        raw_data.append(chr(groupaction))
        raw_data.append(chr(action))

        raw_data.append(chr( data & 0x000000FF ))
        raw_data.append(chr((data & 0x0000FF00) / 256 ))        
        raw_data.append(chr((data & 0x00FF0000) / 65536 ))
        raw_data.append(chr((data & 0xFF000000) / 16777216 ))
        

        trycom.SendCommandRaw(raw_data)
        
        #return resp_deviceid, resp_groupaction, resp_action, resp_data


    def close(self):
        self.ser.close()
        return

