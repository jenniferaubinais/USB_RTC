#################################
#    (c) Jennifer AUBINAIS      #
#################################
import sys, os
import time, datetime
from time import ctime
CurrentFile = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CurrentFile + "/JAUSBRTC")
from JAUSBRTC import JAUSBRTC
from JANTPInternet import JANTPInternet
import subprocess, shlex
#################################
def main(argv):
    #################################
    print('MCP2221A and MCP7490N')
    print('=====================')
    print()
    #################################
    myNTPInternet = JANTPInternet()
    #
    #if myNTPInternet.testNTPInternet():
    #    exit()
    #################################
    print('Update Raspberry Pi')
    print('===================')
    mcpUsbRtc = JAUSBRTC()
    if (mcpUsbRtc.Reset() == -1):
        print("ERROR : No key connected or driver not installed")
        exit()
    #################################
    mcpUsbRtc = JAUSBRTC()
    stTime = mcpUsbRtc.GetTime()
    print(stTime)
    if isinstance(stTime, str):
        stDate = mcpUsbRtc.GetDate()  
        if isinstance(stDate, str):
            stDateSplit = stDate.split('/')
            stDateTime = stDateSplit[2] + "-" + stDateSplit[1] + "-"
            stDateTime += stDateSplit[0] + " " + stTime
            print()
            try:
                subprocess.call(shlex.split("sudo date -s '%s'" % stDateTime))
            except:
                exit()
            print()
            print("OK : Raspberry Pi is updated")
        else:
            print("ERROR : Not get Date")
    else:
        print("ERROR : Not get Time")
#################################
if __name__ == '__main__':
    main(sys.argv[:1])
    

