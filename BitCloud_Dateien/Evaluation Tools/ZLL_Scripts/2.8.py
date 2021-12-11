"""
@testcase
@description 2.7 TP-PRE-TC-07: Security feature with ZR as DUT

@tags
  POSITIVE

@connection dummyPort = router
"""

#*****************************************************************************************
#Defines section
#*****************************************************************************************
import sys
sys.path.append(scriptPath)
from common import *
from deviceScanner import *
from basicCluster import *
sys.path.remove(scriptPath)

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []

configureCommunication()

ed1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
ed2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
r1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
r2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
resetRouterToFN([r1, r2])
resetEndDeviceToFN([ed1, ed2])
clearPorts([r1, r2, ed1, ed2])
powerOff([r1, r2, ed1, ed2])

ed1ExtAddr = getExtAddr(ed1)
writeLog("ED1 extended address - %016X" % ed1ExtAddr)

r1ExtAddr = getExtAddr(r1)
writeLog("R1 extended address - %016X" % r1ExtAddr)

#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 Power on ZR1 and ED1")
powerOn([ed1, r1])

writeLog("2 Initiate touchlink on ED1 with R1")
touchlink(ed1, r1)
idle([ed1, r1])

writeLog("3a, 3b, 3c, 3d ED1 joins the network (shall be checked by sniffer)")

r1NwkAddr = getNwkAddress(r1)
writeLog("R1 network address - 0x%04X" % r1NwkAddr)
ed1NwkAddr = getNwkAddress(ed1)
writeLog("ED1 network address - 0x%04X" % ed1NwkAddr)

writeLog("Set addressing on ED1")
setAddressing(ed1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("Disable NWK security")
sendCommand(ed1, setNwkSecurityCmd % 0)

writeLog("4a ED1 reads basic cluster attribute with network security disabled")
writeLog("4b There is no response from R1 on the air")
readBasicClusterAttribute(ed1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID, retStatus = ZCL_NO_RESPONSE_ERROR_STATUS)
idle([ed1, r1])

writeLog("Enable NWK security")
sendCommand(ed1, setNwkSecurityCmd % 1)

writeLog("5a ED1 reads basic cluster attribute with network security enabled")
writeLog("5b ED1 receives response from ZR1")
readBasicClusterAttribute(ed1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID)
idle([ed1, r1])

