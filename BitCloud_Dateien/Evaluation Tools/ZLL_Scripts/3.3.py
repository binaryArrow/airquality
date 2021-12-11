"""
@testcase
@description 3.3 TP-CST-TC-03: Group addressed commands with server as DUT

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
from groupsCluster import *
from sceneCluster import *
from levelControlCluster import *
from commissioningCluster import *
sys.path.remove(scriptPath)

group1Id = 0x0001

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []

configureCommunication()

client1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
server1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
server2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
resetRouterToFN([server1, server2])
resetEndDeviceToFN([client1])
clearPorts([server1, server2, client1])
powerOff([server1, server2, client1])

client1ExtAddr = getExtAddr(client1)
writeLog("ED1 extended address - %016X" % client1ExtAddr)

server1ExtAddr = getExtAddr(server1)
writeLog("R1 extended address - %016X" % server1ExtAddr)

writeLog("P1 Power on client and server1")
powerOn([client1, server1])

writeLog("P2 Touchlink client and server1")
touchlink(client1, server1)
idle([client1, server1, server2])

server1NwkAddr = getNwkAddress(server1)
writeLog("R1 network address - 0x%04X" % server1NwkAddr)

client1NwkAddr = getNwkAddress(client1)
writeLog("ED1 network address - 0x%04X" % client1NwkAddr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, server1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("P3 Client sends Remove all groups command")
sendRemoveAllGroupsCommand(client1)
receiveAndCheck(server1, removeAllGroupsIndStr)

writeLog("P4 Client sends Add group command")
sendAddGroupCommand(client1, server1NwkAddr, APP_ENDPOINT_LIGHT, group1Id)
check(receiveAddGroupInd(server1) == group1Id)
receiveAndCheck(client1, addGroupResponseStr)
receiveAndCheck(client1, endpointInformationIndStr % APP_ENDPOINT_LIGHT)
receiveAndCheck(server1, zclDefRespReceivedIndStr % 0)

writeLog("P5 Power on server2")
powerOn([server2])

writeLog("P6 Touchlink client and server2")
touchlink(client1, server2)
idle([client1, server1, server2])

server2NwkAddr = getNwkAddress(server2)
writeLog("R2 network address - 0x%04X" % server2NwkAddr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, server2NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("P7 Client sends Remove all groups command")
sendRemoveAllGroupsCommand(client1)
receiveAndCheck(server2, removeAllGroupsIndStr)

writeLog("P8 Client sends Add group command")
sendAddGroupCommand(client1, server2NwkAddr, APP_ENDPOINT_LIGHT, group1Id)
check(receiveAddGroupInd(server2) == group1Id)
receiveAndCheck(client1, addGroupResponseStr)
receiveAndCheck(client1, endpointInformationIndStr % APP_ENDPOINT_LIGHT)
#receiveAndCheck(server1, zclDefRespReceivedIndStr % 0)

writeLog("Set addressing on client")
setAddressing(client1, APS_GROUP_ADDRESS, group1Id, APP_ENDPOINT_LIGHT)

#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 Client sends on command")
sendOnCommand(client1) 
receiveOnCommand(server1)

writeLog("2 Client sends off command")
sendOffCommand(client1) 
receiveOffCommand(server1)

writeLog("3 Client sends toggle command")
sendToggleCommand(client1) 
receiveToggleCommand(server1)

writeLog("Set addressing on client to address server1")
setAddressing(client1, APS_SHORT_ADDRESS, server1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("4 Client sends read attribute command to server1")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)

writeLog("Set addressing on client to address server2")
setAddressing(client1, APS_SHORT_ADDRESS, server2NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("5 Client sends read attribute command to server2")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)

writeLog("Set addressing on client to address group1")
setAddressing(client1, APS_GROUP_ADDRESS, group1Id, APP_ENDPOINT_LIGHT)

writeLog("6 Client sends toggle command")
sendToggleCommand(client1) 
receiveToggleCommand(server1)

writeLog("Set addressing on client to address server1")
setAddressing(client1, APS_SHORT_ADDRESS, server1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("7 Client sends read attribute command to server1")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)

writeLog("Set addressing on client to address server2")
setAddressing(client1, APS_SHORT_ADDRESS, server2NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("8 Client sends read attribute command to server2")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)

