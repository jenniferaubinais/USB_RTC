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
print('Set Time and Date')
print('=================')
print()
#################################
# 08:55:00 AM 03/12/20 EN
# 08:55:00 PM 12/03/2020 FR
# 23:00:45 03/12/2020 FR
# 10:00:00 12/03/2020 EN
# 12/03/2020 EN
# 03/12/20 FR
# 23:40:00
# 11:40:00 PM
# ERROR : 23:40:00 AM
# ERROR : 31/12/20 EN
# ERROR : 12/31/2020 FR
# ERROR 03/03/2020 10:00:00
#################################
mcpUsbRtc = JAUSBRTC()
mcpUsbRtc.Reset()
Freturn = -1
#################################
if len(sys.argv) == 2: # Time -- Date -- FROM (from the Raspberry Pi time)
    if str(sys.argv[1]) == 'FROM':
        Freturn = mcpUsbRtc.UpdateFrom(True)
    else:
        mcpUsbRtc = JAUSBRTC()
        if ':' in str(sys.argv[1]):
	        Freturn = mcpUsbRtc.SetTime(str(sys.argv[1]))
        if '/' in str(sys.argv[1]):
	        Freturn = mcpUsbRtc.SetDate(str(sys.argv[1]))
        mcpUsbRtc.Reset()
#################################	
if len(sys.argv) == 3: # Time Date -- Time AM/PM -- Date FR/EN
    mcpUsbRtc = JAUSBRTC()
    if ':' in str(sys.argv[1]):
        if 'M' in str(sys.argv[2]):
            Freturn = mcpUsbRtc.SetTime(str(sys.argv[1]),str(sys.argv[2]))
        if '/' in str(sys.argv[2]):
            Freturn = mcpUsbRtc.SetTime(str(sys.argv[1]))
            if Freturn == 0:
                Freturn = mcpUsbRtc.SetDate(str(sys.argv[1]))
    if '/' in str(sys.argv[1]):
        if ((str(sys.argv[2]) == 'FR') or (str(sys.argv[2]) == 'EN')):
            Freturn = mcpUsbRtc.SetDate(str(sys.argv[1]),str(sys.argv[2]))
    mcpUsbRtc.Reset()
#################################	
if len(sys.argv) == 4: # Time AM/PM Date -- Time Date FR/EN
    mcpUsbRtc = JAUSBRTC()
    if ':' in str(sys.argv[1]):
        if 'M' in str(sys.argv[2]):
            Freturn = mcpUsbRtc.SetTime(str(sys.argv[1]),str(sys.argv[2]))
        if '/' in str(sys.argv[2]):
            if ((str(sys.argv[3]) == 'FR') or (str(sys.argv[3]) == 'EN')):
                Freturn = mcpUsbRtc.SetDate(str(sys.argv[2]),str(sys.argv[3]))
    mcpUsbRtc.Reset()
#################################	
if len(sys.argv) == 5: # Time AM/PM Date FR/EN
    mcpUsbRtc = JAUSBRTC()
    if ':' in str(sys.argv[1]):
        if 'M' in str(sys.argv[2]):
            if '/' in str(sys.argv[3]):
                if mcpUsbRtc.SetTime(str(sys.argv[1]),str(sys.argv[2])) == 0:
                    if ((str(sys.argv[4]) == 'FR') or (str(sys.argv[4]) == 'EN')):
                        Freturn = mcpUsbRtc.SetDate(str(sys.argv[3]),str(sys.argv[4]))
    mcpUsbRtc.Reset()
#################################
if Freturn == -1:
	print('ERROR')
#################################	
mcpUsbRtc = JAUSBRTC()
print(mcpUsbRtc.GetTime(False))
print(mcpUsbRtc.GetDate(False))
#################################





#print (sys.argv[0]) #Affiche monfichier.py
#print (sys.argv[1]) #Affiche toto
#print (3 + sys.argv[2]) #Affiche 15
