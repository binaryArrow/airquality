"""
@testcase
@description 3.5 TP-CST-TC-05: Level control cluster with client as DUT

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
from sceneCluster import *
from levelControlCluster import *
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

writeLog("P3 Client sends move to level (with on/off) command")
sendMoveToLevelCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MEDIUM_LEVEL, time = 1)

#Wait for level to change(100ms)
sleep(1)

writeLog("P3 Client sends off command")
sendOffCommand(client1) 
receiveOffCommand(server1)

#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 Client sends read attribute command")
check(readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) == ZCL_LEVEL_CONTROL_CLUSTER_MEDIUM_LEVEL)

writeLog("2a Client sends move (with on/off) command")
sendMoveCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MODE_UP, 0x40)

#sleeping little more than 2 sec(time for level to change)
sleep(3) # (ZCL_LEVEL_CONTROL_CLUSTER_MAXIMUM_LEVEL - 128) / 0x40

writeLog("2b Client sends read attribute command")
check(readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) == ZCL_LEVEL_CONTROL_CLUSTER_MAXIMUM_LEVEL)

writeLog("3a Client sends move to level command")
sendMoveToLevelCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MEDIUM_LEVEL, time = 0)

writeLog("3b Client sends read attribute command")
check(readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) == ZCL_LEVEL_CONTROL_CLUSTER_MEDIUM_LEVEL)

writeLog("4 Client sends off command")
sendOffCommand(client1) 
receiveOffCommand(server1)

writeLog("5 Client sends on command")
sendOnCommand(client1) 
receiveOnCommand(server1)

writeLog("6a Client sends step command")
sendStepCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_STEP_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MODE_DOWN, 0x40, 0x0014)

sleep(2)

writeLog("6b Client sends step command")
sendStepCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_STEP_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MODE_DOWN, 0x40, 0x0014)

writeLog("6c Client sends read attribute command")
check(readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) == ZCL_LEVEL_CONTROL_CLUSTER_MINIMUM_LEVEL)

writeLog("7a Client sends toggle command")
sendToggleCommand(client1) 
receiveToggleCommand(server1)

writeLog("7b Client sends on command")
sendOnCommand(client1) 
receiveOnCommand(server1)

writeLog("8 Client sends move to level (with on/off) command")
sendMoveToLevelCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MINIMUM_LEVEL, time = 600)

writeLog("9 Client sends stop command")
sendSimpleLevelControlCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_STOP_COMMAND_ID)

writeLog("10 Client sends step (with on/off) command")
sendStepCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_STEP_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MODE_DOWN, 0xFE, 0x0258)

writeLog("11 Client sends stop (with on/off) command")
sendSimpleLevelControlCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_STOP_W_ONOFF_COMMAND_ID)
