"""
@testcase
@description 3.8 TP-CST-TC-08: Manufacturer specific commands with server as DUT

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
from identifyCluster import *
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

writeLog("P3 Client sends read attribute command")
check((readBasicClusterAttribute(client1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID)) == 0x01)

writeLog("P4 Client sends write attribute command")
writeIdentifyClusterAttribute(client1, ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID, ZCL_U16BIT_DATA_TYPE_ID, 0x0000)

#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("Set illegal addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT, 0xFFFF, DISABLE_DEFAULT_RESPONSE)

writeLog("1a Client sends identify command with manufacturer code of 0x0000")
sendIdentifyCommand(client1)
receiveAndCheck(client1, zclDefRespReceivedIndStr % ZCL_UNSUP_MANUF_CLUSTER_COMMAND)
idle([client1], 1000)

writeLog("Set legal addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("1b Client immediately reads attributes")
check(readIdentifyClusterAttribute(client1, ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID) == 0x0000)

writeLog("Set illegal addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT, 0xFFFF, ENABLE_DEFAULT_RESPONSE)

writeLog("2a Client sends write attribute command with manufacturer code of 0x0000")
sendCommand(client1, writeIdentifyClusterAttrCmd % (ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID, ZCL_U16BIT_DATA_TYPE_ID, 0x003C))
writeLog("Client receives response from server")
receiveAndCheck(client1, zclDefRespReceivedIndStr % ZCL_UNSUP_MANUF_GENERAL_COMMAND_STATUS)
idle([client1], 5000)

writeLog("Set legal addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("2b Client immediately reads attributes")
check(readIdentifyClusterAttribute(client1, ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID) == 0x0000)

writeLog("Set illegal addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT, 0xFFFF)
writeLog("3 Client sends read attribute command with manufacturer code of 0x0000")
sendCommand(client1, readBasicClusterAttrCmd % ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID)
receiveAndCheck(client1, zclDefRespReceivedIndStr % ZCL_UNSUP_MANUF_GENERAL_COMMAND_STATUS)
idle([client1], 1000)

