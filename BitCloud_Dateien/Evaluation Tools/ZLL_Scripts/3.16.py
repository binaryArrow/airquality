"""
@testcase
@description 3.16 TP-CST-TC-16: Color control cluster with client as DUT

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

idle([client1, server1])
#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 Client sends move to color command (Red)")
sendMoveToColorCommand(client1, 40000, 20000, 0x0032)
receiveAndCheck(server1, moveToColorIndStr)

writeLog("2 Client sends move to color command (Green)")
sendMoveToColorCommand(client1, 10000, 40000, 0x00C8)
receiveAndCheck(server1, moveToColorIndStr)

writeLog("3 Client sends move to hue command (Blue)")
sendMoveToHueCommand(client1, 180, ZCL_ZLL_MOVE_TO_HUE_DIRECTION_SHORTEST_DISTANCE, 0x0032)
receiveAndCheck(server1, moveToHueIndStr)

writeLog("4 Client sends move hue command")
sendMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_UP, 0x0a)
receiveAndCheck(server1, moveHueIndStr)

writeLog("5 Client sends move hue command")
sendMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_DOWN, 0x14)
receiveAndCheck(server1, moveHueIndStr)

writeLog("6 Client sends move hue command")
sendMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_STOP, 1)
receiveAndCheck(server1, moveHueIndStr)

writeLog("7 Client sends step hue command")
sendStepHueCommand(client1, ZCL_ZLL_STEP_SATURATION_STEP_MODE_UP, 0x40, 0x64)
receiveAndCheck(server1, stepHueIndStr)

writeLog("8 Client sends move to saturation command")
sendMoveToSaturationCommand(client1, 0x00, 0x32)
receiveAndCheck(server1, moveToSaturationIndStr)

writeLog("9 Client sends move saturation command")
sendMoveSaturationCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_UP, 0x0a)
receiveAndCheck(server1, moveSaturationIndStr)

writeLog("10 Client sends move saturation command")
sendMoveSaturationCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_DOWN, 0x14)
receiveAndCheck(server1, moveSaturationIndStr)

writeLog("11 Client sends move saturation command")
sendMoveSaturationCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_STOP, 1)
receiveAndCheck(server1, moveSaturationIndStr)

writeLog("12 Client sends step saturation command")
sendStepSaturationCommand(client1, ZCL_ZLL_STEP_SATURATION_STEP_MODE_UP, 0x40, 0x64)
receiveAndCheck(server1, stepSaturationIndStr)

writeLog("13 Client sends move to hue and saturation command")
sendMoveToHueAndSaturationCommand(client1, 180, 0x7F, 0x0064)
receiveAndCheck(server1, moveToHueAndSaturationIndStr)

writeLog("14a Client sends store scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_STORE_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, storeSceneIndStr)
receiveAndCheck(client1, storeSceneRespIndStr % 0)

writeLog("14b Client sends move to color command (Red)")
sendMoveToColorCommand(client1, 40000, 20000, 0x0032)
receiveAndCheck(server1, moveToColorIndStr)

sleep(6)

writeLog("14c Client sends recall scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_RECALL_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, recallSceneIndStr)

writeLog("15 Client sends move to color command (Green)")
sendMoveToColorCommand(client1, 10000, 40000, 0x00C8)
receiveAndCheck(server1, moveToColorIndStr)

writeLog("16 Client sends move color command")
sendMoveColorCommand(client1, 0x03e8, 0xd8f0)
receiveAndCheck(server1, moveColorIndStr)

writeLog("17 Client sends move color command")
sendMoveColorCommand(client1, 0, 0)
receiveAndCheck(server1, moveColorIndStr)

writeLog("18 Client sends move to color command")
sendMoveToColorCommand(client1, 20000, 20000, 0x0032)
receiveAndCheck(server1, moveToColorIndStr)

writeLog("19 Client sends step color command")
sendStepColorCommand(client1, 0x01f4, 0xfc18, 0x0064)
receiveAndCheck(server1, stepColorIndStr)

writeLog("20 Client sends enhanced move to hue command")
sendEnhancedMoveToHueCommand(client1, 45000, ZCL_ZLL_MOVE_TO_HUE_DIRECTION_SHORTEST_DISTANCE, 0x0032)
receiveAndCheck(server1, enhancedMoveToHueIndStr)

writeLog("21 Client sends enhanced move hue command")
sendEnhancedMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_UP, 0x0a)
receiveAndCheck(server1, enhancedMoveHueIndStr)

writeLog("22 Client sends enhanced move hue command")
sendEnhancedMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_DOWN, 0x14)
receiveAndCheck(server1, enhancedMoveHueIndStr)

writeLog("23 Client sends enhanced move hue command")
sendEnhancedMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_STOP, 1)
receiveAndCheck(server1, enhancedMoveHueIndStr)

writeLog("24 Client sends enhanced step hue command")
sendEnhancedStepHueCommand(client1, ZCL_ZLL_STEP_SATURATION_STEP_MODE_UP, 0x4000, 0x0a)
receiveAndCheck(server1, enhancedStepHueIndStr)

writeLog("25 Client sends enhanced move to hue and saturation command")
sendEnhancedMoveToHueAndSaturationCommand(client1, 45000, 0x7f, 0x0064)
receiveAndCheck(server1, enhancedMoveToHueAndSaturationIndStr)

writeLog("26a Client sends move to color command")
sendMoveToColorCommand(client1, 20000, 20000, 0x0064)
receiveAndCheck(server1, moveToColorIndStr)

writeLog("26b Client sends stop move step command")
sendStopMoveStepHueCommand(client1)

