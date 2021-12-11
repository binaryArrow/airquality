"""
@testcase
@description 3.17 TP-CST-TC-17: Color control cluster (color loop) with server as DUT

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
from colorControlCluster import *
from commissioningCluster import *
sys.path.remove(scriptPath)

group1Id = 0x0001
group2Id = 0x0002
group3Id = 0x0003
group4Id = 0x0004

broadcastAllAddr = 0xFFFF
broadcastEndpoint = 0xFF

scene1Id = 0x01
scene2Id = 0x02
scene3Id = 0x02

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
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT, ENABLE_DEFAULT_RESPONSE)

writeLog("P3 Client sends on command")
sendOnCommand(client1)
receiveOnCommand(server1)

writeLog("P4 Client sends remove all groups command")
sendRemoveAllGroupsCommand(client1)
receiveAndCheck(server1, removeAllGroupsIndStr)

writeLog("Client sends add group command")
sendAddGroupCommand(client1, r1NwkAddr, APP_ENDPOINT_LIGHT, group1Id)
check(receiveAddGroupInd(server1) == group1Id)
receiveAndCheck(client1, addGroupResponseStr)
receiveAndCheck(client1, endpointInformationIndStr % APP_ENDPOINT_LIGHT)
receiveAndCheck(server1, zclDefRespReceivedIndStr % 0)

writeLog("P5 Client sends move to color command (Red)")
sendMoveToColorCommand(client1, 40000, 20000, 0x000a)
receiveAndCheck(server1, moveToColorIndStr)

idle([client1, server1])
#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1a Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x0e,
                           direction = ZCL_ZLL_COLOR_LOOP_SET_DIRECTION_DECREMENT_HUE,
                           time = 0x000a,
                           startHue = 0xAA00)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("1b Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_ACTIVE_SERVER_ATTRIBUTE_ID) == 0x00)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_DIRECTION_SERVER_ATTRIBUTE_ID) == 0x00)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_TIME_SERVER_ATTRIBUTE_ID) == 0x000a)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_START_ENHANCED_HUE_SERVER_ATTRIBUTE_ID) == 0xAA00)

writeLog("2a Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x02,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_ACTIVATE,
                           direction = ZCL_ZLL_COLOR_LOOP_SET_DIRECTION_INCREMENT_HUE)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("2b Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_ACTIVE_SERVER_ATTRIBUTE_ID) == 0x00)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_DIRECTION_SERVER_ATTRIBUTE_ID) == 0x01)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_TIME_SERVER_ATTRIBUTE_ID) == 0x000a)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_START_ENHANCED_HUE_SERVER_ATTRIBUTE_ID) == 0xAA00)

writeLog("3a Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x01,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_ACTIVATE_ENHANCED)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("3b Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_ACTIVE_SERVER_ATTRIBUTE_ID) == 0x01)

writeLog("3c Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x01,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_DEACTIVATE)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("3d Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_ACTIVE_SERVER_ATTRIBUTE_ID) == 0x00)

writeLog("4a Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x01,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_ACTIVATE)
receiveAndCheck(server1, colorLoopSetIndStr)

sleep(12)

writeLog("4b Client sends read attribute command")
storedHue = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_STORED_ENHANCED_HUE_SERVER_ATTRIBUTE_ID)
print 'Stored hue = %d' % storedHue

writeLog("4c Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x01,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_DEACTIVATE)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("5a Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x01,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_ACTIVATE_ENHANCED)
receiveAndCheck(server1, colorLoopSetIndStr)

sleep(12)

writeLog("5b Client sends read attribute command")
storedHue = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_STORED_ENHANCED_HUE_SERVER_ATTRIBUTE_ID)
print 'Stored hue = %d' % storedHue

writeLog("5c Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x01,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_DEACTIVATE)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("6a Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x05,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_ACTIVATE_ENHANCED,
                           time = 0x0064)
receiveAndCheck(server1, colorLoopSetIndStr)

sleep(10)

writeLog("6b Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x02,
                           direction = ZCL_ZLL_COLOR_LOOP_SET_DIRECTION_DECREMENT_HUE)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("6c Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x01,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_DEACTIVATE)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("7a Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x07,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_ACTIVATE_ENHANCED,
                           direction = ZCL_ZLL_COLOR_LOOP_SET_DIRECTION_INCREMENT_HUE,
                           time = 0x0064)
receiveAndCheck(server1, colorLoopSetIndStr)

sleep(10)

writeLog("7b Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x04,
                           time = 0x000a)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("7c Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x01,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_DEACTIVATE)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("8a Client sends read attribute command")
currentHue = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_ENHANCED_CURRENT_HUE_SERVER_ATTRIBUTE_ID)
print 'Current Hue = %d' % currentHue

writeLog("8b Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x05,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_ACTIVATE_ENHANCED,
                           time = 0x001e)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("8c Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_LOOP_STORED_ENHANCED_HUE_SERVER_ATTRIBUTE_ID) == currentHue)

writeLog("8d Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x01,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_DEACTIVATE)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("8e Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_ENHANCED_CURRENT_HUE_SERVER_ATTRIBUTE_ID) == currentHue)

writeLog("9a Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x07,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_ACTIVATE_ENHANCED,
                           direction = ZCL_ZLL_COLOR_LOOP_SET_DIRECTION_INCREMENT_HUE,
                           time = 0x000a)
receiveAndCheck(server1, colorLoopSetIndStr)

writeLog("9b Client sends enhanced move to hue command (Blue)")
sendEnhancedMoveToHueCommand(client1, 45000, ZCL_ZLL_MOVE_TO_HUE_DIRECTION_SHORTEST_DISTANCE, 0x000a)
receiveAndCheck(server1, enhancedMoveToHueIndStr)

writeLog("9c Client sends color loop set command")
sendColorLoopSetCmdCommand(client1,
                           0x01,
                           action = ZCL_ZLL_COLOR_LOOP_SET_ACTION_DEACTIVATE)
receiveAndCheck(server1, colorLoopSetIndStr)



