#!/usr/bin/python
# -*- coding: utf-8 -*-

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

        self.ser = serial.Serial()      
        
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
        self.Bind(wx.EVT_COMBOBOX, self.EvtChangeESC, self.cmbComPort)

        self.lblRX = wx.StaticText(self, label="RX System")
        self.rxList = ['None', 'Spektrum', 'Futaba']
        grid.Add(self.lblRX, pos=(0,2))
        self.cmbRX = wx.ComboBox(self, size=(115, -1), choices=self.rxList, style=wx.CB_DROPDOWN)
        grid.Add(self.cmbRX, pos=(0,3))
        self.cmbRX.SetSelection(0)
        self.Bind(wx.EVT_COMBOBOX, self.EvtChangeRX, self.cmbComPort)
 
        # Checkbox
        self.current     = wx.CheckBox(self, label="Current")
        grid.Add(self.current,     pos=(2,0))
        self.currentPortList = ['1', '2', '3']
        self.cmbCurrent = wx.ComboBox(self, size=(45, -1), choices=self.currentPortList, style=wx.CB_DROPDOWN)
        grid.Add(self.cmbCurrent, pos=(2,1))
        self.cmbCurrent.SetSelection(0)
        
        self.voltage     = wx.CheckBox(self, label="Voltage")
        grid.Add(self.voltage,     pos=(3,0), span=(1,2))

        self.temperature = wx.CheckBox(self, label="Temperature")
        grid.Add(self.temperature, pos=(4,0), span=(1,2))

        self.capacity    = wx.CheckBox(self, label="Capacity")
        grid.Add(self.capacity,    pos=(5,0), span=(1,2))

        self.rpm         = wx.CheckBox(self, label="RPM")
        grid.Add(self.rpm,         pos=(6,0), span=(1,2))

        self.power       = wx.CheckBox(self, label="Power")
        grid.Add(self.power,       pos=(7,0), span=(1,2))
        
        self.powerbox    = wx.CheckBox(self, label="Powerbox")
        grid.Add(self.powerbox,    pos=(8,0), span=(1,2))
        
        self.lblV1 = wx.StaticText(self, label="V1 min")
        grid.Add(self.lblV1, pos=(9,0))
        self.editV1 = wx.TextCtrl(self, value="0", size=(115,-1))
        grid.Add(self.editV1, pos=(9,1))
        self.lblV2 = wx.StaticText(self, label="V2 min")
        grid.Add(self.lblV2, pos=(10,0))
        self.editV2 = wx.TextCtrl(self, value="0", size=(115,-1))
        grid.Add(self.editV2, pos=(10,1))
        self.lblC1 = wx.StaticText(self, label="Cap1 max")
        grid.Add(self.lblC1, pos=(9,2))
        self.editC1 = wx.TextCtrl(self, value="0", size=(115,-1))
        grid.Add(self.editC1, pos=(9,3))
        self.lblC2 = wx.StaticText(self, label="Cap2 max")
        grid.Add(self.lblC2, pos=(10,2))
        self.editC2 = wx.TextCtrl(self, value="0", size=(115,-1))
        grid.Add(self.editC2, pos=(10,3))
        
        # Buttons
        self.save = wx.Button(self, label="Save")
        grid.Add(self.save, pos=(11,0))
        self.retrieve = wx.Button(self, label="Retrieve")
        grid.Add(self.retrieve, pos=(11,1))
        self.exit = wx.Button(self, label="Exit")
        grid.Add(self.exit, pos=(11,3))
        self.Bind(wx.EVT_BUTTON, self.EvtSave, self.save)
        self.Bind(wx.EVT_BUTTON, self.EvtRetrieve, self.retrieve)
        self.Bind(wx.EVT_BUTTON, self.stop, self.exit)
         
        hSizer.Add(grid, 0, wx.ALL, 5)
        hSizer.Add(self.logger)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        #mainSizer.Add(self.button, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

    def HideSpectrum(self):
        self.lblV1.Hide()
        self.editV1.Hide()
        self.lblC1.Hide()
        self.editC1.Hide()
        self.lblV2.Hide()
        self.editV2.Hide()
        self.lblC2.Hide()
        self.editC2.Hide()
        self.powerbox.Hide()
        self.power.Hide()
        
    def ShowSpectrum(self):
        self.lblV1.Show()
        self.editV1.Show()
        self.lblC1.Show()
        self.editC1.Show()
        self.lblV2.Show()
        self.editV2.Show()
        self.lblC2.Show()
        self.editC2.Show()
        self.powerbox.Show()
        self.power.Show()
        
    def HideFutaba(self):
        self.power.Show()
    
    def ShowFutaba(self):
        self.power.Show()
   
    def EvtSave(self,event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked()) 
        #set esc type
        
        #self.request[4] = self.cmbESC.GetSelection()
        

        #set V1
        #self.request[4] = int(self.editV1.GetValue()) & 0xFF
        #self.request[5] = int(self.editV1.GetValue()) >> 8

        #        #set V2
        #self.request[4] = int(self.editV2.GetValue()) & 0xFF
        #self.request[5] = int(self.editV2.GetValue()) >> 8
   
        #set C1
        #self.request[4] = int(self.editC1.GetValue()) & 0xFF
        #self.request[5] = int(self.editC1.GetValue()) >> 8
        
        #set C2
        #self.request[4] = int(self.editC2.GetValue()) & 0xFF
        #self.request[5] = int(self.editC2.GetValue()) >> 8
  
        #get RX type
            
    def EvtRetrieve(self, event):        
        self.logger.AppendText(self.cmbComPort.GetValue())
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
        print("cle")
    def EvtChangeESC(self, event):
        print("cle")

    def EvtChangeRX(self, event):
        print("cle")

    def stop(self, event):
        print("close")
        self.ser.close()        
        self.Destroy()
        event.Skip()

app = wx.App(False)
frame = InsertFrame()
frame.Show()
app.MainLoop()


