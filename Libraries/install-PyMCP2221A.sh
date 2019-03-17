# https://github.com/nonNoise/PyMCP2221A.git
git clone https://github.com/nonNoise/PyMCP2221A.git
# compiling
cd PyMCP2221A/pypi/main
sudo python3 setup.py build
sudo python3 setup.py install
# ATTENTION : launch with sudo
cd ..
cd ..
cd examples
sudo python3 HIDAPItest.py
