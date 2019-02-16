#!/usr/bin/python # -*- coding: utf-8 -*-

"""
Tkinter tutorial

This script shows a simple window
on the screen.

last modified: January 2011
website: www.zetcode.com
"""
import time
import wx
import serial
from serial.tools import list_ports
import MultieSensorCom

class InsertFrame(wx.Frame):
    def __init__(self):
        #wx.Panel.__init__(self, parent)
        wx.Frame.__init__(self, None, title='Frame With Button',size=(300, 100))        
        panel = wx.Panel(self)

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)        
        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        self.logger = wx.TextCtrl(self, size=(300,170), style=wx.TE_MULTILINE | wx.TE_READONLY)
        #self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())

        #self.ser = serial.Serial()      
        
        
        #COM port 
        self.ports = list_ports.comports()
        self.portList = []        
        for self.port in self.ports:
           self.portList.append(self.port[0])      
        self.lblComPort = wx.StaticText(self, label="Com Port")
        grid.Add(self.lblComPort, pos=(1,0))
        self.cmbComPort = wx.ComboBox(self, size=(115, -1), choices=self.portList, style=wx.CB_DROPDOWN)
        grid.Add(self.cmbComPort, pos=(1,1))
        self.Bind(wx.EVT_COMBOBOX, self.EvtChangePort, self.cmbComPort)
               
        self.lblESC = wx.StaticText(self, label="ESC")
        self.escList = ['None', 'Castle Creations']
        grid.Add(self.lblESC, pos=(0,0))
        self.cmbESC = wx.ComboBox(self, size=(115, -1), choices=self.escList, style=wx.CB_DROPDOWN)
        grid.Add(self.cmbESC, pos=(0,1))
        self.cmbESC.SetSelection(0)
        self.Bind(wx.EVT_COMBOBOX, self.EvtChangeESC, self.cmbESC)
        self.cmbESC.SetSelection(1)
        self.cmbESC.Enable(False)

        self.lblRX = wx.StaticText(self, label="RX System")
        self.rxList = ['None', 'Spektrum', 'Futaba']
        grid.Add(self.lblRX, pos=(0,2))
        self.cmbRX = wx.ComboBox(self, size=(115, -1), choices=self.rxList, style=wx.CB_DROPDOWN)
        grid.Add(self.cmbRX, pos=(0,3))
        self.cmbRX.SetSelection(0)
        self.Bind(wx.EVT_COMBOBOX, self.EvtChangeRX, self.cmbRX)
        self.cmbRX.SetSelection(2)
        self.cmbRX.Enable(False)
 
        # Checkbox
        self.slot         = wx.StaticText(self, label="Slot")
        grid.Add(self.slot,pos=(2,2))
        self.current     = wx.CheckBox(self, label="Current Sensor mAh/V/A")
        grid.Add(self.current,     pos=(3,0))
        self.currentPortList = ['1', '2', '3','4','5','8','9','10','11','12','13','16','17','18','19','20','21','24','25','26','27','28','29']
        self.cmbCurrent = wx.ComboBox(self, size=(45, -1), choices=self.currentPortList, style=wx.CB_DROPDOWN)
        grid.Add(self.cmbCurrent, pos=(3,2))
        self.cmbCurrent.SetSelection(0)
 
        self.temperature = wx.CheckBox(self, label="Temperature")
        grid.Add(self.temperature, pos=(4,0))
        self.SinglePortList = ['1', '2', '3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
        self.cmbTemperature = wx.ComboBox(self, size=(45, -1), choices=self.SinglePortList, style=wx.CB_DROPDOWN)
        grid.Add(self.cmbTemperature, pos=(4,2))
        self.cmbTemperature.SetSelection(1)

        self.rpm         = wx.CheckBox(self, label="RPM")
        grid.Add(self.rpm,         pos=(5,0))              
        self.cmbRPM = wx.ComboBox(self, size=(45, -1), choices=self.SinglePortList, style=wx.CB_DROPDOWN)
        grid.Add(self.cmbRPM, pos=(5,2))
        self.cmbRPM.SetSelection(2)

        
        self.lblCapUsed = wx.StaticText(self, label="Capacity Telemetry")
        grid.Add(self.lblCapUsed, pos=(6,0))
        self.editCapUsed = wx.TextCtrl(self, value="0", size=(115,-1))
        grid.Add(self.editCapUsed, pos=(6,1))
        
        self.lblCapCharged = wx.StaticText(self, label="Capacity Charged")
        grid.Add(self.lblCapCharged, pos=(7,0))
        self.editCapCharged = wx.TextCtrl(self, value="0", size=(115,-1))
        grid.Add(self.editCapCharged, pos=(7,1))

      
        self.lblPoles = wx.StaticText(self, label="Engine Poles")
        grid.Add(self.lblPoles, pos=(8,0))
        self.NrOfPolesList = ['2','4','6','8','10','12','14','16','18','20','22','24','26','28']
        self.cmbNrOfPoles = wx.ComboBox(self, size=(45, -1), choices=self.NrOfPolesList, style=wx.CB_DROPDOWN)
        grid.Add(self.cmbNrOfPoles, pos=(8,2))
        self.cmbNrOfPoles.SetSelection(6)
        
        # Buttons
        self.save = wx.Button(self, label="Save")
        grid.Add(self.save, pos=(10,0))
        self.retrieve = wx.Button(self, label="Retrieve")
        grid.Add(self.retrieve, pos=(10,1))
        self.exit = wx.Button(self, label="Exit")
        grid.Add(self.exit, pos=(10,3))
        self.Bind(wx.EVT_BUTTON, self.EvtSave, self.save)
        self.Bind(wx.EVT_BUTTON, self.EvtRetrieve, self.retrieve)
        self.Bind(wx.EVT_BUTTON, self.stop, self.exit)
         
        hSizer.Add(grid, 0, wx.ALL, 5)
        hSizer.Add(self.logger)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        #mainSizer.Add(self.button, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

    def EvtSave(self,event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked()) 
        #set esc type
        
        #self.request[4] = self.cmbESC.GetSelection()
 
        self.com.SendCommandInt( self.com.DEVICE_ID, self.com.C1_SET, self.com.C2_CURRENT_PORT, int( self.cmbCurrent.GetValue() ) )         
        self.com.SendCommandInt( self.com.DEVICE_ID, self.com.C1_SET, self.com.C2_RPM_PORT, int( self.cmbRPM.GetValue() ) )
        self.com.SendCommandInt( self.com.DEVICE_ID, self.com.C1_SET, self.com.C2_TEMPERATURE_PORT, int( self.cmbTemperature.GetValue() ) )
        self.com.SendCommandInt( self.com.DEVICE_ID, self.com.C1_SET, self.com.C2_NR_POLS, int( self.cmbNrOfPoles.GetValue() ) )

        used = int( self.editCapUsed.GetValue() )
        charged = int( self.editCapCharged.GetValue() )        
        self.com.SendCommandInt( self.com.DEVICE_ID, self.com.C1_SET, self.com.C2_CAL_CURRENT_CAL, int((charged * 100 )/ used) ) 
        
   
        #get RX type
        self.com.SendCommandInt( 0x55, 0x06, 0x22, 0xFFFF )
            
    def EvtRetrieve(self, event):        
        _,_,_, data = self.com.SendCommandInt( self.com.DEVICE_ID, self.com.C1_GET, self.com.C2_CURRENT_PORT )        
        self.cmbCurrent.SetValue(str(data))
        _,_,_, data = self.com.SendCommandInt( self.com.DEVICE_ID, self.com.C1_GET, self.com.C2_RPM_PORT )
        self.cmbRPM.SetValue(str(data))
        _,_,_, data = self.com.SendCommandInt( self.com.DEVICE_ID, self.com.C1_GET, self.com.C2_TEMPERATURE_PORT )
        self.cmbTemperature.SetValue(str(data))
        _,_,_, data = self.com.SendCommandInt( self.com.DEVICE_ID, self.com.C1_GET, self.com.C2_NR_POLS )
        self.cmbNrOfPoles.SetValue(str(data))

        _,_,_, data = self.com.SendCommandInt( self.com.DEVICE_ID, self.com.C1_GET, self.com.C2_CAL_CURRENT_CAL )
        
        self.editCapUsed.SetValue(str(1000))
        self.editCapCharged.SetValue(str(data*10))
        
        #get esc type
        #self.cmbESC.SetSelection(ord(self.response[2]))  
                    
        #get RX type
        #self.cmbRX.SetSelection(ord(self.response[2]))         
        
        #get Simulation sensors type
        #self.current.SetValue( ord(self.response[2]) & 0x01 )   
        #self.voltage.SetValue( ord(self.response[2]) & 0x02 )     
        #self.powerbox.SetValue( ord(self.response[2]) & 0x04 )    
        #self.temperature.SetValue( ord(self.response[2]) & 0x08 ) 
        #self.power.SetValue( ord(self.response[2]) & 0x10 )       
        #self.capacity.SetValue( ord(self.response[2]) & 0x20 )    
        #self.rpm.SetValue( ord(self.response[2]) & 0x40 )
        
        #get V1
        #self.editV1.SetValue( str(ord(self.response[2]) + (ord(self.response[3]) << 8)))
        
        #get V1
        #self.editV2.SetValue( str(ord(self.response[2]) + (ord(self.response[3]) << 8)))

        #get C1
        #self.editC1.SetValue( str(ord(self.response[2]) + (ord(self.response[3]) << 8)))
        
        #get C1
        #self.editC2.SetValue( str(ord(self.response[2]) + (ord(self.response[3]) << 8)))

    def EvtChangePort(self, event):
        self.com = MultieSensorCom.Interface(self.cmbComPort.GetValue())
        if ( self.com.openport() ):
            self.com.connect()
            self.logger.AppendText('MultiInterface found on : ' + self.cmbComPort.GetValue() +'\n')
        else:
            self.logger.AppendText('ERROR MultiInterface not found : ' + self.cmbComPort.GetValue() +'\n')
        
        
    def EvtChangeESC(self, event):
        print("clsdsde")

    def EvtChangeRX(self, event):
        print("clssssse")

    def stop(self, event):
        print("close")        
        #self.com.close()        
        self.Destroy()
        event.Skip()

app = wx.App(False)
frame = InsertFrame()
frame.Show()
app.MainLoop()


