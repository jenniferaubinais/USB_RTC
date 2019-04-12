#######################################################################
#    (c) Jennifer AUBINAIS - 2019                                     #
#######################################################################
import ntplib
import threading
import subprocess, shlex
import socket
import http.client
#######################################################################
class JANTPInternet(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
#######################################################################
# TEST if NTP server and connected to internet
#######################################################################
    def haveInternet(self):
        try:
            # first check if we get the correct IP-Address or just the router's IP-Address
            info = socket.getaddrinfo("www.google.com", None)[0]
            ipAddr = info[4][0]
            if ipAddr == "192.168.0.1" :
                return False
        except Exception as e:
            print(e)
            return False
#################################            
        conn = http.client.HTTPConnection("www.google.com", timeout=5)
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(e)
            return False
#######################################################################
# TEST if NTP server and connected to internet
#######################################################################        
    def testNTPInternet(self):
        # test NTP server
        out = subprocess.check_output(['timedatectl'], universal_newlines=True)
        print(str(out))
        if ('NTP synchronized: yes' in out) == True:
            # test internet connection
            print()
            if self.haveInternet():
                print('===============================================')
                print("Your Raspberry Pi is connected to time's server")
                print("Your Raspberry Pi is connected to internet")
                print("WARNING : Not update from USB-RTC key")
                print('===============================================')
            else:
                print('===============================================')
                print("Your Raspberry Pi is connected to time's server")
                print("Your Raspberry Pi is NOT connected to internet")
                print('===============================================')
            return True
        else:
            print('===================================================')
            print("Your Raspberry Pi is NOT connected to time's server")
            print('===================================================')
        return False
#######################################################################

