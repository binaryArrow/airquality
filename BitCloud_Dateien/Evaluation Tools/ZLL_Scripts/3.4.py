"""
@testcase
@description 3.4 TP-CST-TC-04: Level control cluster with server as DUT

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

client1ExtAddr = getExtAddr(client1)
writeLog("ED1 extended address - %016X" % client1ExtAddr)

server1ExtAddr = getExtAddr(server1)
writeLog("R1 extended address - %016X" % server1ExtAddr)

writeLog("P1 Power on client and server1")
powerOn([client1, server1])

writeLog("P2 Touchlink client and server1")
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

writeLog("P4 Client sends move to level (with on/off) command")
sendMoveToLevelCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MEDIUM_LEVEL, time = 1)

#Wait for level to change(100ms)
sleep(1)
writeLog("P5 Client sends off command")
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

writeLog("4a Client sends off command")
sendOffCommand(client1) 
receiveOffCommand(server1)

writeLog("4b Client sends read attribute command")
check(readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) == ZCL_LEVEL_CONTROL_CLUSTER_MEDIUM_LEVEL)

writeLog("5a Client sends on command")
sendOnCommand(client1) 
receiveOnCommand(server1)

writeLog("5b Client sends read attribute command")
check(readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) == ZCL_LEVEL_CONTROL_CLUSTER_MEDIUM_LEVEL)

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

writeLog("7b Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) == ZCL_LEVEL_CONTROL_CLUSTER_MINIMUM_LEVEL)

writeLog("8a Client sends toggle command")
sendToggleCommand(client1) 
receiveToggleCommand(server1)

writeLog("8b Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) == ZCL_LEVEL_CONTROL_CLUSTER_MINIMUM_LEVEL)

writeLog("9a Client sends move command")
sendMoveCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MODE_UP, 0x0A)

sleep(10)

writeLog("9b Client sends stop command")
sendSimpleLevelControlCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_STOP_COMMAND_ID)

writeLog("9c Client sends read attribute command")
level = readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID)
check((level >= 0x5B) and (level <= 0x6F)) # 10 percent window near 0x65

writeLog("10a Client sends move command")
sendMoveCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MODE_DOWN, 0x04)

sleep(10)

writeLog("10b Client sends stop command")
sendSimpleLevelControlCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_STOP_COMMAND_ID)

writeLog("10c Client sends read attribute command")
level = readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID)
check((level >= 0x37) and (level <= 0x43)) # 10 percent window near 0x3D

writeLog("11a Client sends move to level (with on/off) command")
sendMoveToLevelCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MINIMUM_LEVEL, time = 600)

sleep(10)

writeLog("11b Client sends read attribute command")
remainingTime = readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_REMAINING_TIME_ATTRIBUTE_ID)
check(remainingTime >= 475 and remainingTime <= 525) # 5 percent window near 500

sleep(50)

writeLog("11c Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) == ZCL_LEVEL_CONTROL_CLUSTER_MINIMUM_LEVEL)

writeLog("12a Client sends step (with on/off) command")
sendStepCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_STEP_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MODE_UP, 0x01, 0xFFFF)

writeLog("12b Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readLevelControlClusterAttribute(client1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) == ZCL_LEVEL_CONTROL_CLUSTER_MINIMUM_LEVEL + 1)
