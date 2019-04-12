#####################################
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
    print("#####################################")
    print("#             Test HIDAPI           #")
    print("# ERROR : MCP2221 key not connected #")
    print("#####################################")
    exit(1)
mcp2221a = hid.device()
try:
    mcp2221a.open_path(hid.enumerate(0x04D8, 0x00DD)[0]["path"])
    print("###############")
    print("# Test HIDAPI #")
    print("###############")
except:
    print("#################################")
    print("#           Test HIDAPI         #")
    print("# ERROR : MCP2221 key not found #")
    print("#################################")
