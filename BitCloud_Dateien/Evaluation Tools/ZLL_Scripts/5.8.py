"""
@testcase
@description 5.8 TP-LLI-TC-07: Level control

@tags
  INTEROPERABILITY
  CHAPTER_5
  TOUCHLINK
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

v1rc1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
v2l1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
resetRouterToFN([v2l1])
resetEndDeviceToFN([v1rc1])
clearPorts([v2l1, v1rc1])
powerOff([v2l1, v1rc1])

v1rc1ExtAddr = getExtAddr(v1rc1)
writeLog("ED1 extended address - %016X" % v1rc1ExtAddr)

v2l1ExtAddr = getExtAddr(v2l1)
writeLog("R1 extended address - %016X" % v2l1ExtAddr)

writeLog("P1 Power on v1rc1 and v2l1")
powerOn([v1rc1, v2l1])

writeLog("P2 Touchlink v1rc1 and v2l1")
touchlink(v1rc1, v2l1)
idle([v1rc1, v2l1])

r1NwkAddr = getNwkAddress(v2l1)
writeLog("R1 network address - 0x%04X" % r1NwkAddr)

ed1NwkAddr = getNwkAddress(v1rc1)
writeLog("ED1 network address - 0x%04X" % ed1NwkAddr)

writeLog("Set addressing on v1rc1")
setAddressing(v1rc1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)


writeLog("P4 v1rc1 sends move to level (with on/off) command")
sendMoveToLevelCommand(v1rc1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MEDIUM_LEVEL, time = 1)

#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 v1rc1 sends on command")
sendOnCommand(v1rc1) 
receiveOnCommand(v2l1)

writeLog("2 v1rc1 sends move to level command")
sendMoveToLevelCommand(v1rc1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MEDIUM_LEVEL, time = 0)

writeLog("3 v1rc1 sends off command")
sendOffCommand(v1rc1) 
receiveOffCommand(v2l1)

writeLog("v1rc1 sends read attribute command")
check(readOnOffClusterAttribute(v1rc1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)

writeLog("4a v1rc1 sends move command")
sendMoveCommand(v1rc1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MODE_UP, 0x0A)

writeLog("4b v1rc1 sends move command")
sendMoveCommand(v1rc1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MODE_UP, 0x0A)

sleep(2)

writeLog("v1rc1 sends read attribute command")
check(readOnOffClusterAttribute(v1rc1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readLevelControlClusterAttribute(v1rc1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) > ZCL_LEVEL_CONTROL_CLUSTER_MEDIUM_LEVEL)

writeLog("5a v1rc1 sends move command")
sendMoveCommand(v1rc1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MODE_DOWN, 0x0A)

writeLog("5b v1rc1 sends move command")
sendMoveCommand(v1rc1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MODE_DOWN, 0x40)

sleep(10)

writeLog("v1rc1 sends read attribute command")
check(readOnOffClusterAttribute(v1rc1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readLevelControlClusterAttribute(v1rc1, ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID) == ZCL_LEVEL_CONTROL_CLUSTER_MINIMUM_LEVEL)
