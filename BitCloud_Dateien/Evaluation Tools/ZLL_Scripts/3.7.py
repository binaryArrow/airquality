"""
@testcase
@description 3.7 TP-CST-TC-07: Basic cluster with client as DUT

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
from onOffCluster import *
from basicCluster import *
sys.path.remove(scriptPath)

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []

configureCommunication()

client1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
server1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
resetRouterToFN([server1])
resetEndDeviceToFN([client1])
clearPorts([server1, client1])
powerOff([server1, client1])

ed1ExtAddr = getExtAddr(client1)
writeLog("ED1 extended address - %016X" % ed1ExtAddr)

r1ExtAddr = getExtAddr(server1)
writeLog("R1 extended address - %016X" % r1ExtAddr)

writeLog("P1 Power on client and server1")
powerOn([client1, server1])

writeLog("P2 Touchlink client and server")
touchlink(client1, server1)
idle([client1, server1])

r1NwkAddr = getNwkAddress(server1)
writeLog("R1 network address - 0x%04X" % r1NwkAddr)

ed1NwkAddr = getNwkAddress(client1)
writeLog("ED1 network address - 0x%04X" % ed1NwkAddr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("P3 Client sends on command")
sendOnCommand(client1) 
receiveOnCommand(server1)

#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1a Client sends read attribute command")
check(readBasicClusterAttribute(client1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("1b Client sends read attribute command")
readBasicClusterAttribute(client1, ZCL_BASIC_CLUSTER_SERVER_APPLICATION_VERSION_ATTRIBUTE_ID)

writeLog("1c Client sends read attribute command")
readBasicClusterAttribute(client1, ZCL_BASIC_CLUSTER_SERVER_STACK_VERSION_ATTRIBUTE_ID)

writeLog("1d Client sends read attribute command")
readBasicClusterAttribute(client1, ZCL_BASIC_CLUSTER_SERVER_HW_VERSION_ATTRIBUTE_ID)

writeLog("1e Client sends read attribute command")
readBasicClusterAttribute(client1, ZCL_BASIC_CLUSTER_SERVER_MANUFACTURER_NAME_ATTRIBUTE_ID)

writeLog("1f Client sends read attribute command")
readBasicClusterAttribute(client1, ZCL_BASIC_CLUSTER_SERVER_MODEL_IDENTIFIER_ATTRIBUTE_ID)

writeLog("1g Client sends read attribute command")
readBasicClusterAttribute(client1, ZCL_BASIC_CLUSTER_SERVER_DATE_CODE_ATTRIBUTE_ID)

writeLog("1h Client sends read attribute command")
readBasicClusterAttribute(client1, ZCL_BASIC_CLUSTER_SERVER_POWER_SOURCE_ATTRIBUTE_ID)

writeLog("1i Client sends read attribute command")
readBasicClusterAttribute(client1, ZCL_BASIC_CLUSTER_SERVER_SW_BUILD_ID_ATTRIBUTE_ID)
