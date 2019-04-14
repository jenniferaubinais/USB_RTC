######################################
#    (c) Jennifer AUBINAIS          #
#   Check hid and found MCP2221 key #
#####################################
import hid
count = 0
for d in hid.enumerate(0x04D8, 0x00DD):
    keys = d.keys()
    for key in keys:
        count = count +1
if (count == 0):
    exit(1)
mcp2221a = hid.device()
try:
    mcp2221a.open_path(hid.enumerate(0x0488, 0x00DD)[0]["path"])
except:
    exit(2)
