"""
@testcase
@description 5.10 TP-LLI-TC-09: Color control

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

v1rc1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
v2l1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
resetRouterToFN([v2l1])
resetEndDeviceToFN([v1rc1])
clearPorts([v2l1, v1rc1])
powerOff([v2l1, v1rc1])

ed1ExtAddr = getExtAddr(v1rc1)
writeLog("ED1 extended address - %016X" % ed1ExtAddr)

r1ExtAddr = getExtAddr(v2l1)
writeLog("R1 extended address - %016X" % r1ExtAddr)

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
setAddressing(v1rc1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT, ENABLE_DEFAULT_RESPONSE)

writeLog("v1rc1 sends add group command")
sendAddGroupCommand(v1rc1, r1NwkAddr, APP_ENDPOINT_LIGHT, group1Id)
check(receiveAddGroupInd(v2l1) == group1Id)
receiveAndCheck(v1rc1, addGroupResponseStr)
receiveAndCheck(v1rc1, endpointInformationIndStr % APP_ENDPOINT_LIGHT)
receiveAndCheck(v2l1, zclDefRespReceivedIndStr % 0)

idle([v1rc1, v2l1])
#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 v1rc1 sends on command")
sendOnCommand(v1rc1) 
receiveOnCommand(v2l1)

writeLog("2a v1rc1 sends move to hue command (Red)")
sendMoveToHueCommand(v1rc1, 240, ZCL_ZLL_MOVE_TO_HUE_DIRECTION_SHORTEST_DISTANCE, 0x0014)
receiveAndCheck(v2l1, moveToHueIndStr)

sleep(3)

writeLog("2b v1rc1 sends move to hue command (Green)")
sendMoveToHueCommand(v1rc1, 120, ZCL_ZLL_MOVE_TO_HUE_DIRECTION_SHORTEST_DISTANCE, 0x0014)
receiveAndCheck(v2l1, moveToHueIndStr)

sleep(3)

writeLog("2c v1rc1 sends move to hue command (Blue)")
sendMoveToHueCommand(v1rc1, 180, ZCL_ZLL_MOVE_TO_HUE_DIRECTION_SHORTEST_DISTANCE, 0x0014)
receiveAndCheck(v2l1, moveToHueIndStr)

sleep(3)

writeLog("3 v1rc1 sends move to saturation command")
sendMoveToSaturationCommand(v1rc1, 0x00, 0x32)
receiveAndCheck(v2l1, moveToSaturationIndStr)
