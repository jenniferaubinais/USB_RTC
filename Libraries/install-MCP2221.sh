# https://github.com/signal11/hidapi
# https://github.com/zkemble/libmcp2221
#
sudo pip3 install hidapi
sudo apt install libudev-dev libusb-1.0-0-dev
# download
git clone https://github.com/zkemble/libmcp2221.git
git clone https://github.com/signal11/hidapi.git
# prepare to compile
sudo cp ./libmcp2221/libmcp2221/libmcp2221.h /usr/include/
cp ./hidapi/hidapi/hidapi.h ./libmcp2221/libmcp2221/
cp ./hidapi/linux/hid.c ./libmcp2221/libmcp2221/
# compiling
cd libmcp2221/libmcp2221/
make
# copy
cd ..
cd ..
sudo cp ./libmcp2221/libmcp2221/bin/libmcp2221.* /usr/lib/
