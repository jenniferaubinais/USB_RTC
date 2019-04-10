#######################################################################
#    (c) Jennifer AUBINAIS - 2019                                     #
#    from Github Yuta KItagami                                        #   
#######################################################################
import hid
import time
import sys, os, time
from time import strftime
#######################################################################
class JAUSBRTC:
    def __init__(self,VID = 0x04D8,PID = 0x00DD,devnum = 0):
        self.mcp2221a = hid.device()
        self.mcp2221a.open_path(hid.enumerate(0x04D8, 0x00DD)[devnum]["path"])
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
        Freturn = -1
        stTime = strftime("%H:%M:%S", time.localtime())
        stDate = strftime("%d/%m/%Y", time.localtime())
        if Fdebug:
            print(stTime)
            print(stDate)
        mcpUsbRtc = JAUSBRTC()
        Freturn = mcpUsbRtc.SetTime(stTime)
        if Freturn == 0:
            Freturn = mcpUsbRtc.SetDate(stDate)
        mcpUsbRtc.Reset()
        return Freturn
#######################################################################
# Set Time
#######################################################################
    def SetTime(self,stTime,stAMPM = '',Fdebug = False):
        self.I2C_Init(Fdebug)
#################################
        stHours, stMinutes, stSeconds = stTime.split(':')
#################################
        iHours = self.parseInt(stHours)
        ValH = int(iHours / 10)
        ValL = iHours - int(ValH*10)
        if Fdebug:
            print(str(ValH),str(ValL))
        if stAMPM == 'AM':
                val = (ValH << 4) + ValL
                val = val | 0x40 & 0x5F
                if self.Write_MCP7490(0x02, val, Fdebug) == -1:
                        return -1
        if stAMPM == 'PM':
                val = (ValH << 4) + ValL
                val = val | 0x40 | 0x20
                if self.Write_MCP7490(0x02, val, Fdebug) == -1:
                        return -1
        if stAMPM == '':
                val = (ValH << 4) + ValL
                val = val & 0x3F
                if self.Write_MCP7490(0x02, val, Fdebug) == -1:
                        return -1
#################################
        iMinutes = self.parseInt(stMinutes)
        ValH = int(iMinutes / 10)
        ValL = iMinutes - int(ValH*10)
        if Fdebug:
            print(str(ValH),str(ValL))
        val = (ValH << 4) + ValL
        val = val & 0x7F
        if self.Write_MCP7490(0x01, val, Fdebug) == -1:
                return -1
#################################
        iSeconds = self.parseInt(stSeconds)
        ValH = int(iSeconds / 10)
        ValL = iSeconds - int(ValH*10)
        if Fdebug:
            print(str(ValH),str(ValL))
        val = (ValH << 4) + ValL
        val = val | 0x80
        if self.Write_MCP7490(0x00, val, Fdebug) == -1:
                return -1
        return 0
#######################################################################
# Set Time
#######################################################################
    def SetDate(self,stDate,stFREN = '',Fdebug = False):
        self.I2C_Init(Fdebug)
#################################
        stDay, stMonth, stYear = stDate.split('/')
#################################
        iDay = self.parseInt(stDay)
        ValH = int(iDay / 10)
        ValL = iDay - int(ValH*10)
        if Fdebug:
            print(str(ValH),str(ValL))
        val = (ValH << 4) + ValL
        val = val & 0x3F
        if self.Write_MCP7490(0x04, val, Fdebug) == -1:
            return -1
#################################
        iMonth = self.parseInt(stMonth)
        ValH = int(iMonth / 10)
        ValL = iMonth - int(ValH*10)
        if Fdebug:
            print(str(ValH),str(ValL))
        val = (ValH << 4) + ValL
        # Leap Year
        val = val & 0x1F
        if self.Write_MCP7490(0x05, val, Fdebug) == -1:
            return -1
#################################
        iYear = self.parseInt(stYear)
        if iYear > 99:
                iYear = iYear - 2000
        ValH = int(iYear / 10)
        ValL = iYear - int(ValH*10)
        if Fdebug:
            print(str(ValH),str(ValL))
        val = (ValH << 4) + ValL
        if self.Write_MCP7490(0x06, val, Fdebug) == -1:
            return -1
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
        ValReturn = ''
        self.I2C_Init(Fdebug)
#################################
        value = self.Read_MCP7490(0x02, Fdebug)
        if value != -1:
            valueH = value >> 4
            valueH = valueH & 0x03
            valueL = value & 0x0F
            ValReturn += str(valueH)
            ValReturn += str(valueL)
            ValReturn += ':'
        else:
            self.printError(Fdebug)
#################################
        value = self.Read_MCP7490(0x01, Fdebug)
        if value != -1:
            valueH = value >> 4
            valueH = valueH & 0x07
            valueL = value & 0x0F
            ValReturn += str(valueH)
            ValReturn += str(valueL)
            ValReturn += ':'
        else:
            self.printError(Fdebug)
#################################
        value = self.Read_MCP7490(0x00, Fdebug)
        if value != -1:
            valueH = value >> 4
            valueH = valueH & 0x07
            valueL = value & 0x0F
            ValReturn += str(valueH)
            ValReturn += str(valueL)
        else:
            self.printError(Fdebug)
        return ValReturn
#######################################################################
# Return Date
#######################################################################
    def GetDate(self,Fdebug = False):
        ValReturn = ''
        self.I2C_Init(Fdebug)
#################################
        value = self.Read_MCP7490(0x04, Fdebug)
        if value != -1:
            valueH = value >> 4
            valueH = valueH & 0x0
            valueL = value & 0x0F
            ValReturn += str(valueH)
            ValReturn += str(valueL)
            ValReturn += '/'
        else:
            self.printError(Fdebug)
#################################
        value = self.Read_MCP7490(0x05, Fdebug)
        if value != -1:
            valueH = value >> 4
            valueH = valueH & 0x01
            valueL = value & 0x0F
            ValReturn += str(valueH)
            ValReturn += str(valueL)
            ValReturn += '/'
        else:
            self.printError(Fdebug)
#################################
        value = self.Read_MCP7490(0x06, Fdebug)
        if value != -1:
            valueH = value >> 4
            valueH = valueH & 0x0F
            valueL = value & 0x0F
            ValReturn += str(valueH)
            ValReturn += str(valueL)
        else:
            self.printError(Fdebug)
        return ValReturn
#######################################################################
# I2C Init
#######################################################################
    def I2C_Init(self, Fdeb = False, speed = 100000):  # speed = 100000
        if Fdeb:
            print("Init MCP2221A")
        buf = [0x00, 0x10]
        buf = buf + [0 for i in range(65 - len(buf))]
        buf[2 + 1] = 0x00  # Cancel current I2C/SMBus transfer (sub-command)
        buf[3 + 1] = 0x20  # Set I2C/SMBus communication speed (sub-command)
        # The I2C/SMBus system clock divider that will be used to establish the communication speed
        buf[4 + 1] = int((12000000 / speed) - 3)
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(65)
        if(rbuf[22] == 0):
            print("Error MCP2221A : SCL is low.")
            exit()
            return -1
        if(rbuf[23] == 0):
            print("Error MCP2221A : SDA is low.")
            exit()
            return -1
#######################################################################
# I2C Cancel
#######################################################################
    def I2C_Cancel(self, Fdeb = False):
        if Fdeb:
            print("Cancel MPC2221A")
        buf = [0x00, 0x10]
        buf = buf + [0 for i in range(65 - len(buf))]
        buf[2 + 1] = 0x10  # Cancel current I2C/SMBus transfer (sub-command)
        self.mcp2221a.write(buf)
        self.mcp2221a.read(65)
#######################################################################
# MCP7490 Write
#######################################################################
    def Write_MCP7490(self, addr, data, Fdebug = False):
        if Fdebug:
             print("Write MCP7490 - address:0x{:02x} - data:0x{:02x}".format(addr, data))
        buf = [0 for i in range(7)]
        buf[0] = 0x00
        buf[1] = 0x90
        buf[2] = 2 # Low len
        buf[3] = 0 # high len
        buf[4] = 0xDE
        buf[5] = addr
        buf[6] = data
        if Fdebug:
            print('Write MCP7490 : ', end='')
            print("[0x{:02x}:0x{:02x}:0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x}]".format(buf[0],buf[1],buf[2],buf[3],buf[4],buf[5],buf[6]))
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(0x40)
        if (rbuf[1] != 0x00):
                if Fdebug:
                    print('ERROR MCP7490')
                self.I2C_Cancel(Fdebug)
                self.I2C_Init(Fdebug)
                return -1
        buf = [0x00, 0x40, 0x00, 0x00, 0x00]
        if Fdebug:
            print('Write MCP7490 : ', end='')
            print("[0x{:02x}:0x{:02x}:0x{:02x},0x{:02x},0x{:02x}]".format(buf[0],buf[1],buf[2],buf[3],buf[4]))
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(0x40)
        if (rbuf[2] == 0x00 and rbuf[3] == 0x00):
            if Fdebug:
                print('Write MCP7490 OK')
            self.I2C_Cancel(Fdebug)
            self.I2C_Init(Fdebug)
            return 0
        else:
            if Fdebug:
                print('ERROR MCP7490')
            self.I2C_Cancel(Fdebug)
            self.I2C_Init(Fdebug)
            return -1
        return 0
#######################################################################
# MCP7490 Read
####################################################################### 
    def Read_MCP7490(self, addr, Fdebug = False):
        buf = [0 for i in range(6)]
        buf[0] = 0x00
        buf[1] = 0x90
        buf[2] = 1 # low len
        buf[3] = 0 # high len
        buf[4] = 0xDE
        buf[5] = addr
        if Fdebug:
            print('Read MCP7490 : ', end='')
            print("[0x{:02x}:0x{:02x}:0x{:02x},0x{:02x},0x{:02x},0x{:02x}]".format(buf[0],buf[1],buf[2],buf[3],buf[4],buf[5]))
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(64)
        if (rbuf[1] != 0x00):
                self.I2C_Cancel(Fdebug)
                self.I2C_Init(Fdebug)
                return -1
        buf = [0x00, 0x40, 0x00, 0x00, 0x00]
        if Fdebug:
            print('Write MCP7490 : ', end='')
            print("[0x{:02x}:0x{:02x}:0x{:02x},0x{:02x},0x{:02x}]".format(buf[0],buf[1],buf[2],buf[3],buf[4]))
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(0x40)
        if (rbuf[1] != 0x00):
                if Fdebug:
                    print('Read ERROR')
                self.I2C_Cancel(Fdebug)
                self.I2C_Init(Fdebug)
                return -1
        if (rbuf[2] == 0x00 and rbuf[3] == 0x00):
            if Fdebug:
                print('Read 0x00 : ', end='')
                print("[0x{:02x},0x{:02x}]".format(rbuf[2],rbuf[3]))
        if (rbuf[2] == 0x55):
            if Fdebug:
                print('Read 0x55 : ', end='')
                print("[0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x}]".format(rbuf[0],rbuf[1],rbuf[2],rbuf[3],rbuf[4],rbuf[5]))
            rdata = [0] * size
            for i in range(size):
                rdata[i] = rbuf[4 + i]
        if Fdebug:
            print("END WRITE")
        # Next
        buf[1] = 0x91
        buf = buf + [0 for i in range(3)]
        buf[1 + 1] = 2 #(size & 0x00FF)  # Read LEN
        buf[2 + 1] = 0 #(size & 0xFF00) >> 8  # Read LEN
        buf[3 + 1] = 0xDE #0xFF & (addrs << 1) # addrs
        buf[4 + 1] = 0
        if Fdebug:
            print('Write 1R buf : ', end='')
            print("[0x{:02x}:0x{:02x}:0x{:02x},0x{:02x},0x{:02x},0x{:02x}]".format(buf[0],buf[1],buf[2],buf[3],buf[4],buf[5]))
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(0x40)
        if (rbuf[1] != 0x00):
            if Fdebug:
                print('ERROR Read')
            self.I2C_Cancel(Fdebug)
            self.I2C_Init(Fdebug)
            return -1
        buf = [0x00, 0x40]
        buf = buf + [0 for i in range(65 - len(buf))]
        buf[1 + 1] = 0x00
        buf[2 + 1] = 0x00
        buf[3 + 1] = 0x00
        self.printDebug("Read MCP7490 : ", buf, 8, Fdebug)
        self.mcp2221a.write(buf)
        rbuf = self.mcp2221a.read(0x40)
        if (rbuf[2] == 0x55):
            if Fdebug:
                print('Read 0x55 : ', end='')
                print("[0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x}]".format(rbuf[0],rbuf[1],rbuf[2],rbuf[3],rbuf[4],rbuf[5]))
            return rbuf[4]
        else:
            if Fdebug:
                print('ERROR Read')
            self.I2C_Cancel(Fdebug)
            self.I2C_Init(Fdebug)
        return -1
#######################################################################
# Print message id Debug is True
#######################################################################
    def printDebug(self, St, Vbuf, iLen, Fdeb = False):
        if Fdeb:
            print(St, end='')
            print("[0x{:02x}:0x{:02x}:0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x}]".format(Vbuf[0],Vbuf[1],Vbuf[2],Vbuf[3],Vbuf[4],Vbuf[5],Vbuf[6],Vbuf[7],Vbuf[8]))
#######################################################################
# Print message id Debug is True
#######################################################################
    def printERROR(self, Fdeb = False):
        if Fdeb:
            print('ERROR')
            return 'ERROR'
#######################################################################
# reset
#######################################################################
    def Reset(self, Fdeb = False):
        if Fdeb:
            print ("Reset MCP2221A")
        buf = [0x00, 0x70, 0xAB, 0xCD, 0xEF]
        buf = buf + [0 for i in range(65 - len(buf))]
        self.mcp2221a.write(buf)
        time.sleep(1)


