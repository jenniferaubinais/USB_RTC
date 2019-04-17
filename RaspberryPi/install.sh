#!/bin/bash
echo "#########################"
echo "# (c) Jennifer AUBINAIS #"
echo "# (c) Elektor magazine  #"
echo "#    project 1?????     #"
echo "#########################"
echo 
###
prompt=$(sudo -nv 2>&1)
if [ $? -eq 0 ]; then
  echo "##################"
  echo "# sudo access OK #"
  echo "##################"
elif echo $prompt | grep -q '^sudo:'; then
  echo "############################################################"
  echo "# ERROR : this script must be launched with sudo superuser #"
  echo "# (sudo ./install_USBRTC.sh)                               #"
  echo "############################################################"
  exit 1
else
  echo "########################################" 
  echo "# ERROR : sudo superuser doesn't exist #"
  echo "########################################"
  exit 1
fi
###
if ! hash python; then
    echo "###################################"
    echo "# ERROR : Python is not installed #"
    echo "###################################"
    exit 1
fi
ver=$(python3 -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "35" ]; then
    echo "#######################################################"
    echo "# ERROR : This project requires python 3.5 or greater #"
    echo "#######################################################"
    exit 1
fi
ver=$(python3 -V 2>&1)
ver="# $ver #"
echo "################"
echo $ver
echo "################"
###
echo "####################"
echo "# Update / Upgrade #"
echo "####################"
sudo apt-get update > /dev/null
sudo apt-get -y dist-upgrade > /dev/null
###
echo "#####################"
echo "# Install libraries #"
echo "#####################"
sudo apt-get install libudev-dev -y > /dev/null
matches=$(ldconfig -p | grep libudev);
if [ -z "$matches" ]; then
    echo "################################"
    echo "# ERROR : Installation libudev #"
    echo "################################"
    exit 1
fi
sudo apt-get install libusb-1.0-0-dev -y > /dev/null
matches=$(ldconfig -p | grep libusb-);
if [ -z "$matches" ]; then
    echo "#####################################"
    echo "# ERROR : Installation libusb-1.0.0 #"
    echo "#####################################"
    exit 1
fi
###
echo "##################"
echo "# Install Hidapi #"
echo "##################"
sudo pip3 install hidapi > /dev/null
ver=$(python3 -V 2>&1)
version=$(echo $ver | egrep -o '[0-9]+.[0-9]+')
matches=$(ls /usr/local/lib/python$version/dist-packages | grep hidapi);
if [ -z "$matches" ]; then
    echo "###############################"
    echo "# ERROR : Installation hidapi #"
    echo "###############################"
    exit 1
fi
###
echo "############################"
echo "# Install subversion (SVN) #"
echo "############################"
sudo apt-get install subversion -y > /dev/null
matches=$(svn help | grep 'subversion');
if [ -z "$matches" ]; then
    echo "###################################"
    echo "# ERROR : Installation subversion #"
    echo "###################################"
    exit 1
fi
###
echo "#####################################"
echo "# Copy files libmcp2221 from github #"
echo "#####################################"
sudo rm -Rf libmcp2221 > /dev/null
sudo rm -Rf hidapi > /dev/null
sudo rm -Rf RaspberryPi > /dev/null
sudo rm -Rf USB-RTC-Key > /dev/null
git clone --quiet https://github.com/zkemble/libmcp2221.git > /dev/null
matches=$(ls -l | grep 'libmcp2221');
if [ -z "$matches" ]; then
    echo "############################"
    echo "# ERROR : Clone libmcp2221 #"
    echo "############################"
    exit 1
fi
####
echo "#################################"
echo "# Copy files hidapi from github #"
echo "#################################"
git clone --quiet https://github.com/signal11/hidapi.git > /dev/null
matches=$(ls -l | grep 'hidapi');
if [ -z "$matches" ]; then
    echo "########################"
    echo "# ERROR : Clone hidapi #"
    echo "########################"
    exit 1
fi
####
echo "######################################"
echo "# Copy files USB RTC Key from github #"
echo "######################################"
svn export https://github.com/jenniferaubinais/USB_RTC/trunk/RaspberryPi > /dev/null
matches=$(ls -l | grep 'RaspberryPi');
if [ -z "$matches" ]; then
    echo "#############################"
    echo "# ERROR : Clone USB_RTC_Key #"
    echo "#############################"
    exit 1
fi
sudo mv RaspberryPi USB-RTC-Key > /dev/null
sudo chmod 777 -R USB-RTC-Key > /dev/null
matches=$(ls -l | grep 'USB-RTC-Key');
if [ -z "$matches" ]; then
    echo "#############################"
    echo "# ERROR : Rename USB-RTC-Key "
    echo "#############################"
    exit 1
fi
###
echo "#################################"
echo "# Prepare to compile libmcp2221 #"
echo "#################################"
sudo cp -rf ./USB-RTC-Key/complements/Makefile ./libmcp2221/libmcp2221/ > /dev/null
sudo cp ./libmcp2221/libmcp2221/libmcp2221.h /usr/include/ > /dev/null
cp ./hidapi/hidapi/hidapi.h ./libmcp2221/libmcp2221/ > /dev/null
cp ./hidapi/linux/hid.c ./libmcp2221/libmcp2221/ > /dev/null
echo "##########################"
echo "# compiling libmcp2221 # #"
echo "##########################"
cd libmcp2221/libmcp2221/
make > /dev/null
echo "##########################"
echo "# copy result libmcp2221 #"
echo "##########################"
cd ..
cd ..
sudo cp ./libmcp2221/libmcp2221/bin/libmcp2221.* /usr/lib/ > /dev/null
###
echo "##################"
echo "# Install ntplib #"
echo "##################"
sudo pip3 install ntplib > /dev/null
echo "##########################"
echo "# compiling libmcp2221 # #"
echo "##########################"
cd libmcp2221/libmcp2221/
make > /dev/null
cd /home/pi/
###
echo "###########################"
echo "# connect the USB RTC Key #"
echo "###########################"
echo "Press ENTER when you have connected the USB RTC Key !"
read pressEnter
sudo python3 ./USB-RTC-Key/complements/Test_hidapi.py
result=$(echo $?);
if [ $result -eq 1 ]; then
    echo "#####################################"
    echo "#             Test HIDAPI           #"
    echo "# ERROR : MCP2221 key not connected #"
    echo "#####################################"
    exit 1
fi
if [ $result -eq 3 ]; then
    echo "#################################"
    echo "#           Test HIDAPI         #"
    echo "# ERROR : MCP2221 key not found #"
    echo "#################################"
    exit 1
fi
echo "###############"
echo "# Test HIDAPI #"
echo "###############"
###
echo "#########################"
echo "# Insert Update at boot #"
echo "#########################"
mkdir -vp /home/pi/.config/autostart
sudo cp -rf /home/pi/USB-RTC-Key/complements/usbrtc.desktop /home/pi/.config/autostart > /dev/null
###
echo
echo "##########################"
echo " END install USB RTC key #"
echo "##########################"
