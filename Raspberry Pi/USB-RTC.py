#################################
#    (c) Jennifer AUBINAIS      #
#################################
import sys, os, time
from time import strftime
CurrentFile = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CurrentFile + "/JAUSBRTC")
from JAUSBRTC import JAUSBRTC
#################################
print(strftime("%H:%M:%S", time.localtime()))
print(strftime("%d  %b", time.localtime()))
print('MCP2221A and MCP7490N')
print('=====================')
print('Time - Date')
print('===========')
print()
#################################
mcpUsbRtc = JAUSBRTC()
mcpUsbRtc.Reset(False)
#################################
mcpUsbRtc = JAUSBRTC()
print(mcpUsbRtc.GetTime(False))
print(mcpUsbRtc.GetDate(False))
#################################

