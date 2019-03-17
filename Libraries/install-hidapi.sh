# https://github.com/signal11/hidapi
# install hidapi
sudo apt-get install libudev-dev libusb-1.0-0-dev libfox-1.6-dev -y
sudo apt-get install autotools-dev autoconf automake libtool -y
# compiling
cd hidapi
./bootstrap
./configure
make
sudo make install