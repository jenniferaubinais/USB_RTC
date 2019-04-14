nfile = "/etc/xdg/lxsession/LXDE-pi/autostart"
f = open(nfile, "r")
contents = f.readlines()
f.close()
###
for line in contents:
	if "USB-RTC-Key" in str(line):
		exit(1)
###
position = 0
for line in contents:
	if "xscreensaver" in str(line):
		break
	position = position + 1
###
contents.insert(position, "/home/pi/USB-RTC-Key/UPDATE_RaspberryPi.py\n")
###
f = open(nfile, "w")
contents = "".join(contents)
f.write(contents)
f.close()
exit(0)
