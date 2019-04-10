#################################
#    (c) Jennifer AUBINAIS      #
#################################
from PyMCP2221A import PyMCP2221A

print('MCP2221A connect to MCP7490N')
print('============================')
print()

mcp2221 = PyMCP2221A.PyMCP2221A()
mcp2221.Reset(False)
mcp2221 = PyMCP2221A.PyMCP2221A()

mcp2221.I2C_Init(False)

Creturn = 0
Creturn = mcp2221.Write_MCP7490(0x00, 0xAA, True)
if Creturn == 0:
    value = mcp2221.Read_MCP7490(0x00, False)
    if value != -1:
        print("Value : 0x{:02X}".format(value))
    else:
        print("ERROR")
else:
    print("ERROR")
#################################
Creturn = 0
#Creturn = mcp2221.Write_MCP7490(0x00, 0xAA, True)
if Creturn == 0:
    value = mcp2221.Read_MCP7490(0x01, False)
    if value != -1:
        print("Value : 0x{:02X}".format(value))
    else:
        print("ERROR")
else:
    print("ERROR")
#################################
Creturn = mcp2221.Write_MCP7490(0x07, 0x43, False)
if Creturn == 0:
    value = mcp2221.Read_MCP7490(0x07, False)
    if value != -1:
        print("Value : 0x{:02X}".format(value))
    else:
        print("ERROR")
else:
    print("ERROR")


