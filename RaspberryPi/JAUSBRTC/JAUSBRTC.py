#######################################################################
#    (c) Jennifer AUBINAIS - 2019                                     #
#    from Github Yuta KItagami                                        #   
#######################################################################
import hid
import time
import sys, os, time
from time import strftime
import subprocess, shlex
#######################################################################
class JAUSBRTC():
    def __init__(self,VID = 0x04D8,PID = 0x00DD,devnum = 0):
        self.mcp2221a = hid.device()
        try:
            self.mcp2221a.open_path(hid.enumerate(0x04D8, 0x00DD)[devnum]["path"])
        except:
            pass 
        self.CLKDUTY_0 = 0x00
        self.CLKDUTY_25 = 0x08
        self.CLKDUTY_50 = 0x10
        self.CLKDUTY_75 = 0x18
        # self.CLKDIV_1 = 0x00    # 48MHz  Dont work.
        self.CLKDIV_2 = 0x01    # 24MHz
        self.CLKDIV_4 = 0x02    # 12MHz
        self.CLKDIV_8 = 0x03    # 6MHz
        self.CLKDIV_16 = 0x04   # 3MHz
        self.CLKDIV_32 = 0x05   # 1.5MHz
        self.CLKDIV_64 = 0x06   # 750KHz
        self.CLKDIV_128 = 0x07  # 375KHz
#######################################################################
# Update Time and Date from Raspberry Pi
#######################################################################
    def UpdateFrom(self,Fdebug = False):
        self.printSeparator(Fdebug)
        Freturn = -1
        stTime = strftime("%H:%M:%S", time.localtime())
        stDate = strftime("%d/%m/%Y", time.localtime())
        self.printDebug(stTime, Fdebug)
        self.printDebug(stDate, Fdebug)
        mcpUsbRtc = JAUSBRTC()
        Freturn = mcpUsbRtc.SetTime(stTime, '', Fdebug)
        if Freturn == 0:
            Freturn = mcpUsbRtc.SetDate(stDate, '', Fdebug)
        mcpUsbRtc.Reset()
        self.printDebug('', Fdebug)
        return Freturn
#######################################################################
# Set Time
#######################################################################
    def SetTime(self,stTime,stAMPM = '',Fdebug = False):
        self.printSeparator(Fdebug)
        self.I2C_Init(Fdebug)
#################################
        stHour, stMinute, stSecond = stTime.split(':')
#################################
        valHour = self.ConvertToByte(stHour, 0x5F , "Hour", stAMPM, Fdebug)
        iHour = self.parseInt(stHour)
        ValH = int(iHour / 10)
        ValL = iHour - int(ValH*10)
        self.printDebug("Hour : ", str(ValH), str(ValL), Fdebug)
        if stAMPM == 'AM':
                val = (ValH << 4) + ValL
                val = val | 0x40 & 0x5F
                if self.Write_MCP7490(0x02, val, Fdebug) == -1:
                        self.printDebug('', Fdebug)
                        return -1
        if stAMPM == 'PM':
                val = (ValH << 4) + ValL
                val = val | 0x40 | 0x20
                if self.Write_MCP7490(0x02, val, Fdebug) == -1:
                        self.printDebug('', Fdebug)
                        return -1
        if stAMPM == '':
                val = (ValH << 4) + ValL
                val = val & 0x3F
                if self.Write_MCP7490(0x02, val, Fdebug) == -1:
                        self.printDebug('', Fdebug)
                        return -1
#################################
        iMinute = self.parseInt(stMinute)
        ValH = int(iMinute / 10)
        ValL = iMinute - int(ValH*10)
        self.printDebug("Minute : ", str(ValH), str(ValL), Fdebug)
        val = (ValH << 4) + ValL
        val = val & 0x7F
        if self.Write_MCP7490(0x01, val, Fdebug) == -1:
            self.printDebug('', Fdebug)
            return -1
#################################
        iSecond = self.parseInt(stSecond)
        ValH = int(iSecond / 10)
        ValL = iSecond - int(ValH*10)
        self.printDebug("Second : ", str(ValH), str(ValL), Fdebug)
        val = (ValH << 4) + ValL
        val = val | 0x80
        if self.Write_MCP7490(0x00, val, Fdebug) == -1:
            self.printDebug('', Fdebug)
            return -1
        self.printDebug('', Fdebug)
        return 0
#######################################################################
# Set Time
#######################################################################
    def SetDate(self,stDate,stFREN = '',Fdebug = False):
        self.printSeparator(Fdebug)
        self.I2C_Init(Fdebug)
#################################
        stDay, stMonth, stYear = stDate.split('/')
#################################
        iDay = self.parseInt(stDay)
        ValH = int(iDay / 10)
        ValL = iDay - int(ValH*10)
        self.printDebug("Day : ", str(ValH), str(ValL), Fdebug)
        val = (ValH << 4) + ValL
        val = val & 0x3F
        if self.Write_MCP7490(0x04, val, Fdebug) == -1:
            self.printDebug('', Fdebug)
            return -1
#################################
        iMonth = self.parseInt(stMonth)
        ValH = int(iMonth / 10)
        ValL = iMonth - int(ValH*10)
        self.printDebug("Month : ", str(ValH), str(ValL), Fdebug)
        val = (ValH << 4) + ValL
        # Leap Year
        val = val & 0x1F
        if self.Write_MCP7490(0x05, val, Fdebug) == -1:
            self.printDebug('', Fdebug)
            return -1
#################################
        iYear = self.parseInt(stYear)
        if iYear > 99:
            iYear = iYear - 2000
        ValH = int(iYear / 10)
        ValL = iYear - int(ValH*10)
        self.printDebug("Year : ", str(ValH), str(ValL), Fdebug)
        val = (ValH << 4) + ValL
        if self.Write_MCP7490(0x06, val, Fdebug) == -1:
            self.printDebug('', Fdebug)
            return -1
        self.printDebug('', Fdebug)
        return 0
#######################################################################
# Return int
#######################################################################
    def parseInt(self,s):
        try:
            res = int(s)
            return res
        except:
            return
#######################################################################
# Return Time
#######################################################################
    def GetTime(self,Fdebug = False):
        self.printSeparator(Fdebug)
        ValReturn = ''
        self.I2C_Init(Fdebug)
        buf = self.Read_MCP7490(Fdebug)
        if (buf == -1):
            self.printError(Fdebug)
            return -1
        if ((buf[4+2] & 0b01000000) == 0):
            # not US format
            # Hours
            valTime = self.ExtractString(buf[4+2], 0x03)
            valTime += ':'
            # Minutes
            valTime += self.ExtractString(buf[4+1], 0x07)
            valTime += ':'
            # Seconds
            valTime += self.ExtractString(buf[4+0], 0x07)
        else:
            # US format
            # Hours
            valTime = self.ExtractString(buf[4+2], 0x01)
            valTime += ':'
            # Minutes
            valTime += self.ExtractString(buf[4+1], 0x07)
            valTime += ':'
            # Seconds
            valTime += self.ExtractString(buf[4+0], 0x07)
            if ((buf[4+2] & 0b00100000) == 0):
                # AM
                valTime += ' AM'
            else:
                # PM
                valTime += ' PM'
        self.printDebug('', Fdebug)
        return valTime
#######################################################################
# Return Date
#######################################################################
    def GetDate(self,Fdebug = False):
        self.printSeparator(Fdebug)
        ValReturn = ''
        self.I2C_Init(Fdebug)
        buf = self.Read_MCP7490(Fdebug)
        if (buf == -1):
            self.printError(Fdebug)
            return -1
        # Day
        valDate = self.ExtractString(buf[4+4], 0x03)
        valDate += '/'
        # Month
        valDate += self.ExtractString(buf[4+5], 0x01)
        valDate += '/20'
        # Year
        valDate += self.ExtractString(buf[4+6], 0x0F)
        print(valDate)
        self.printDebug('', Fdebug)
        return valDate
#######################################################################
# I2C Init
#######################################################################
    def I2C_Init(self, Fdeb = False, speed = 100000):  # speed = 100000
        self.printDebug("Init MCP2221A", Fdeb)
        buf = [0x10, 0x00, 0x00, 0x00, 0x00]
        #buf = buf + [0 for i in range(65 - len(buf))]
        buf[2] = 0x00  # Cancel current I2C/SMBus transfer (sub-command)
        buf[3] = 0x20  # Set I2C/SMBus communication speed (sub-command)
        # The I2C/SMBus system clock divider that will be used to establish the communication speed
        buf[4] = int((12000000 / speed) - 3)
        try:
            self.mcp2221a.write(buf)
        except:
            return -1
        rbuf = self.mcp2221a.read(65)
        if(rbuf[22] == 0):
            self.printDebug("Error MCP2221A : SCL is low.", Fdeb)
            self.printDebug('', Fdeb)
            exit()
            return -1
        if(rbuf[23] == 0):
            printDebug("Error MCP2221A : SDA is low.", Fdeb)
            self.printDebug('', Fdeb)
            exit()
            return -1
#######################################################################
# I2C Cancel
#######################################################################
    def I2C_Cancel(self, Fdeb = False):
        self.printDebug("Cancel MPC2221A", Fdeb)
        buf = [0x10, 0x00, 0x00]
        buf[2] = 0x10  # Cancel current I2C/SMBus transfer (sub-command)
        try:
            self.mcp2221a.write(buf)
            self.mcp2221a.read(65)
        except:
          return -1
        return 0
#######################################################################
# MCP7490 Write
#######################################################################
    def Write_MCP7490(self, addr, data, Fdebug = False):
        self.printDebug("Write MCP7490 - address:0x{:02x} - data:0x{:02x}".format(addr, data),Fdebug)
        buf = [0 for i in range(7)]
        buf[0] = 0x00
        buf[1] = 0x90
        buf[2] = 2 # Low len
        buf[3] = 0 # high len
        buf[4] = 0xDE
        buf[5] = addr
        buf[6] = data
        self.printDebugBuffer('Write MCP7490', buf, Fdebug)
        try:
            self.mcp2221a.write(buf)
        except:
            return -1
        rbuf = self.mcp2221a.read(0x40)
        if (rbuf[1] != 0x00):
                self.printDebug('ERROR MCP7490',Fdebug)
                self.I2C_Cancel(Fdebug)
                self.I2C_Init(Fdebug)
                return -1
        buf = [0x40, 0x00, 0x00, 0x00]
        self.printDebugBuffer('Write MCP7490', buf, Fdebug)
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(0x40)
        if (rbuf[2] == 0x00 and rbuf[3] == 0x00):
            self.printDebug('Write MCP7490 : OK', Fdebug)
            self.I2C_Cancel(Fdebug)
            self.I2C_Init(Fdebug)
            return 0
        else:
            self.printDebug('ERROR MCP7490', Fdebug)
            self.I2C_Cancel(Fdebug)
            self.I2C_Init(Fdebug)
            return -1
        return 0
#######################################################################
# MCP7490 Read
####################################################################### 
    def Read_MCP7490(self, Fdebug = False):
        #Fdebug = True
        buf = [0 for i in range(5)]
        buf[0] = 0x90
        buf[1] = 1 # low len
        buf[2] = 0 # high len
        buf[3] = 0xDE
        buf[4] = 0x00
        self.printDebugBuffer('Read MCP7490 ', buf, Fdebug)
        try:
            self.mcp2221a.write(buf)
        except:
            return -1
        rbuf = self.mcp2221a.read(0x90)
        self.printDebugBuffer('Result MCP7490 ', rbuf, Fdebug)
#################################
        buf[0] = 0x91
        buf = buf + [0 for i in range(3)]
        buf[1] = 8 #(size & 0x00FF)  # Read LEN
        buf[2] = 0 #(size & 0xFF00) >> 8  # Read LEN
        buf[3] = 0xDE #0xFF & (addrs << 1) # addrs
        buf[4] = 0
        self.printDebugBuffer('Read MCP7490 ', buf, Fdebug)
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(0x91)
        self.printDebugBuffer('Result MCP7490 ', rbuf, Fdebug)
        if (rbuf[1] != 0x00):
            self.printDebug('ERROR Read', Fdebug)
            self.I2C_Cancel(Fdebug)
            self.I2C_Init(Fdebug)
            return -1
        buf = [0x40, 0x00, 0x00, 0x00]
        self.printDebugBuffer("Read MCP7490 ", buf, Fdebug)
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(0x40)
        self.printDebugBuffer('Result MCP7490  ', rbuf, Fdebug)
        if (rbuf[2] == 0x55):
            self.printDebugBuffer('Read 0x55', rbuf, Fdebug)
            return rbuf
        else:
            print('not')
            self.printDebug('ERROR Read',Fdebug)
            self.I2C_Cancel(Fdebug)
            self.I2C_Init(Fdebug)
        return -1
#######################################################################
# Convert byte to string
#######################################################################
    def ExtractString(self, value, mask):
        valueH = (value >> 4) & mask
        valueL = value & 0x0F
        return str(valueH) + str(valueL)
#######################################################################
# Print Buffer if Debug is True
#######################################################################
    def printDebugBuffer(self, St, Vbuf, Fdeb = False):
        if Fdeb:
            iLen = len(Vbuf)
            if iLen < 3:
                return
            if iLen > 12:
                iLen = 12
            print(St, end='')
            print(" : [0x{:02x}".format(Vbuf[0]), end='')
            for i in range(1,iLen):
                print(":0x{:02x}".format(Vbuf[i]), end='')
            print("]")
        # do nothing
        time.sleep(0.01)
#######################################################################
# Print Message if Debug is True
#######################################################################
    def printDebug(self, St1, St2 = '', St3 = '', Fdeb = False):
        if Fdeb:
            print(St1, St2, St3)
#######################################################################
# Print line separator if Debug is True
#######################################################################
    def printSeparator(self, Fdeb = False):
        self.printDebug('==============================================', Fdeb)
#######################################################################
# Print ERROR if Debug is True
#######################################################################
    def printError(self, Fdeb = False):
        self.printDebug("ERROR", Fdeb)
        self.printDebug('', Fdeb)
        return -1
#######################################################################
# reset
#######################################################################
    def Reset(self, Fdeb = False):
        self.printDebug("Reset MCP2221A", Fdeb)
        try:
            buf = [0x70, 0xAB, 0xCD, 0xEF]
            self.mcp2221a.write(buf)
        except:
            return -1
        time.sleep(1)
        return 0
#######################################################################
# Print the address with this name
#######################################################################
    def printAddr(self, stTx, addr, Fdeb):
        if Fdeb:
            try:
                stText = {
                    0x00 : "RTCSEC", 0x01 : "RTCMIN", 0x02 : "RTCHOUR",
                    0x03 : "RTCWKDAY", 0x04 : "RTCDATE", 0x05 : "RTCMTH",
                    0x06 : "RTCYEAR", 0x07 : "CONTROL", 0x08 : "OSCTRIM",
                    0x09 : "Reserved", 0x0A : "ALM0SEC", 0x0B : "ALM0MIN",
                    0x0C : "ALM0HOUR", 0x0D : "ALM0WKDAY", 0x0E : "ALM0DATE",
                    0x0F : "ALM0MTH", 0x10 : "Reserved", 0x11 : "ALM1SEC",
                    0x12 : "ALM1MIN", 0x13 : "ALM1HOUR", 0x14 : "ALM1WKDAY",
                    0x15 : "ALM1DATE", 0x16 : "ALM1MTH", 0x17 : "Reserved",
                    0x18 : "PWRDNMIN", 0x19 : "PWRDNHOUR", 0x1A : "PWRDNDATE",
                    0x1B : "PWRDNMTH", 0x1C : "PWRUPMIN", 0x1D : "PWRUPHOUR",
                    0x1F : "PWRUPMTH"
                }[addr]
                print(stTx, ":", "0x{:02x}".format(addr), ':', stText)
            except KeyError:
                return 'ERROR'

