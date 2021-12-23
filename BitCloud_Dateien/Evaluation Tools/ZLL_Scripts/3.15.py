"""
@testcase
@description 3.15 TP-CST-TC-15: Color control cluster with server as DUT

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
writeLog("1 Client sends read attribute command")
capabilities = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_CAPABILITIES_SERVER_ATTRIBUTE_ID)
check(capabilities == 0x0F or capabilities == 0x1F or capabilities == 0x10)

if capabilities & 8:# Check XYAttributesSupported in ColorCapabilities
  writeLog("2 Client sends move to color command")
  sendMoveToColorCommand(client1, 40000, 20000, 0x0032)
  receiveAndCheck(server1, moveToColorIndStr)

  writeLog("3a Client sends move to color command")
  sendMoveToColorCommand(client1, 10000, 40000, 0x00C8)
  receiveAndCheck(server1, moveToColorIndStr)

sleep(10)

writeLog("3b Client sends read attribute command")
remainingTime = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_REMAINING_TIME_SERVER_ATTRIBUTE_ID)
check(remainingTime >= 0x5A and remainingTime <= 0x6E) # 10 percent window near 0x64

sleep(15)

writeLog("3c Client sends read attribute command")
remainingTime = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_REMAINING_TIME_SERVER_ATTRIBUTE_ID)
check(remainingTime == 0)

writeLog("4 Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_CURRENT_X_SERVER_ATTRIBUTE_ID) == 10000)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_CURRENT_Y_SERVER_ATTRIBUTE_ID) == 40000)

writeLog("5 Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0x01)

writeLog("6 Client sends read attribute command")
numberOfPrimaries = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_NUMBER_OF_PRIMARIES_SERVER_ATTRIBUTE_ID)
check(numberOfPrimaries >= 0x01 and numberOfPrimaries <= 0x06)

writeLog("6a Client sends read attribute command")
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_1_X_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_1_Y_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_1_INTENSITY_SERVER_ATTRIBUTE_ID)

writeLog("6b Client sends read attribute command")
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_2_X_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_2_Y_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_2_INTENSITY_SERVER_ATTRIBUTE_ID)

writeLog("6c Client sends read attribute command")
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_3_X_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_3_Y_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_3_INTENSITY_SERVER_ATTRIBUTE_ID)

writeLog("6d Client sends read attribute command")
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_4_X_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_4_Y_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_4_INTENSITY_SERVER_ATTRIBUTE_ID)

writeLog("6e Client sends read attribute command")
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_5_X_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_5_Y_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_5_INTENSITY_SERVER_ATTRIBUTE_ID)

writeLog("6f Client sends read attribute command")
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_6_X_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_6_Y_SERVER_ATTRIBUTE_ID)
readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_PRIMARY_6_INTENSITY_SERVER_ATTRIBUTE_ID)

writeLog("7 Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_ENHANCED_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0x01)

if capabilities & 1:# Check hueSaturationSupported in ColorCapabilities
  writeLog("8 Client sends move to hue command")
  sendMoveToHueCommand(client1, 180, ZCL_ZLL_MOVE_TO_HUE_DIRECTION_SHORTEST_DISTANCE, 0x0032)
  receiveAndCheck(server1, moveToHueIndStr)

writeLog("9 Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_ENHANCED_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0)

if capabilities & 1:# Check hueSaturationSupported in ColorCapabilities
  writeLog("10 Client sends move hue command")
  sendMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_UP, 0x0a)
  receiveAndCheck(server1, moveHueIndStr)

  writeLog("11 Client sends move hue command")
  sendMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_DOWN, 0x14)
  receiveAndCheck(server1, moveHueIndStr)

  writeLog("12 Client sends move hue command")
  sendMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_STOP, 1)
  receiveAndCheck(server1, moveHueIndStr)

  writeLog("13 Client sends step hue command")
  sendStepHueCommand(client1, ZCL_ZLL_STEP_SATURATION_STEP_MODE_UP, 0x40, 0x64)
  receiveAndCheck(server1, stepHueIndStr)

  writeLog("14 Client sends move to saturation command")
  sendMoveToSaturationCommand(client1, 0x00, 0x32)
  receiveAndCheck(server1, moveToSaturationIndStr)

  writeLog("15 Client sends move saturation command")
  sendMoveSaturationCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_UP, 0x0a)
  receiveAndCheck(server1, moveSaturationIndStr)

  writeLog("16 Client sends move saturation command")
  sendMoveSaturationCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_DOWN, 0x14)
  receiveAndCheck(server1, moveSaturationIndStr)

  writeLog("17 Client sends move saturation command")
  sendMoveSaturationCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_STOP, 1)
  receiveAndCheck(server1, moveSaturationIndStr)

  writeLog("18 Client sends step saturation command")
  sendStepSaturationCommand(client1, ZCL_ZLL_STEP_SATURATION_STEP_MODE_UP, 0x40, 0x64)
  receiveAndCheck(server1, stepSaturationIndStr)

  writeLog("19a Client sends move to hue and saturation command")
  sendMoveToHueAndSaturationCommand(client1, 180, 0x7F, 0x0064)
  receiveAndCheck(server1, moveToHueAndSaturationIndStr)

  sleep(11)

  writeLog("19b Client sends read attribute command")
  check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_CURRENT_HUE_SERVER_ATTRIBUTE_ID) == 180)

  writeLog("19c Client sends read attribute command")
  check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_CURRENT_SATURATION_SERVER_ATTRIBUTE_ID) == 0x7F)

writeLog("20a Client sends store scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_STORE_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, storeSceneIndStr)
receiveAndCheck(client1, storeSceneRespIndStr % 0)

writeLog("20b Client sends read attribute command")
if capabilities & 8:# Check XYAttributesSupported in ColorCapabilities
  savedCurrentX = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_CURRENT_X_SERVER_ATTRIBUTE_ID)
  savedCurrentY = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_CURRENT_Y_SERVER_ATTRIBUTE_ID)
if capabilities & 2:# Check enhancedHueSupported in ColorCapabilities
  savedEnhancedCurrentHue = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_ENHANCED_CURRENT_HUE_SERVER_ATTRIBUTE_ID)
if capabilities & 1:# Check hueSaturationSupported in ColorCapabilities
  savedCurrentSaturation = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_CURRENT_SATURATION_SERVER_ATTRIBUTE_ID)
 
if capabilities & 8:# Check XYAttributesSupported in ColorCapabilities
  writeLog("20c Client sends move to color command")
  sendMoveToColorCommand(client1, 40000, 20000, 0x0032)
  receiveAndCheck(server1, moveToColorIndStr)

sleep(6)

writeLog("20d Client sends recall scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_RECALL_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, recallSceneIndStr)

writeLog("20e Client sends read attribute command")
if capabilities & 8:# Check XYAttributesSupported in ColorCapabilities
  check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_CURRENT_X_SERVER_ATTRIBUTE_ID) == savedCurrentX)
  check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_CURRENT_Y_SERVER_ATTRIBUTE_ID) == savedCurrentY)
if capabilities & 2:# Check enhancedHueSupported in ColorCapabilities  
  check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_ENHANCED_CURRENT_HUE_SERVER_ATTRIBUTE_ID) == savedEnhancedCurrentHue)
if capabilities & 1:# Check hueSaturationSupported in ColorCapabilities
  check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_CURRENT_SATURATION_SERVER_ATTRIBUTE_ID) == savedCurrentSaturation)

if capabilities & 8:# Check XYAttributesSupported in ColorCapabilities
  writeLog("21 Client sends move to color command")
  sendMoveToColorCommand(client1, 10000, 40000, 0x00C8)
  receiveAndCheck(server1, moveToColorIndStr)

  writeLog("22 Client sends move color command")
  sendMoveColorCommand(client1, 0x03e8, 0xd8f0)
  receiveAndCheck(server1, moveColorIndStr)

  writeLog("23 Client sends move color command")
  sendMoveColorCommand(client1, 0xec78, 0xff9c)
  receiveAndCheck(server1, moveColorIndStr)

  writeLog("24 Client sends move color command")
  sendMoveColorCommand(client1, 0, 0)
  receiveAndCheck(server1, moveColorIndStr)

  writeLog("25 Client sends move to color command")
  sendMoveToColorCommand(client1, 25000, 25000, 0x000A)
  receiveAndCheck(server1, moveToColorIndStr)

  writeLog("26 Client sends step color command")
  sendStepColorCommand(client1, 0x1770, 0xf448, 0x0064)
  receiveAndCheck(server1, stepColorIndStr)

if capabilities & 2:# Check enhancedHueSupported in ColorCapabilities
  writeLog("27a Client sends enhanced move to hue command")
  sendEnhancedMoveToHueCommand(client1, 45000, ZCL_ZLL_MOVE_TO_HUE_DIRECTION_SHORTEST_DISTANCE, 0x0032)
  receiveAndCheck(server1, enhancedMoveToHueIndStr)

sleep(6)

writeLog("27b Client sends read attribute command")
if capabilities & 2:# Check enhancedHueSupported in ColorCapabilities
  check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_ENHANCED_CURRENT_HUE_SERVER_ATTRIBUTE_ID) == 45000)
if capabilities & 8:# Check XYAttributesSupported in ColorCapabilities
  check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0x00)
if capabilities & 2:# Check enhancedHueSupported in ColorCapabilities
  check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_ENHANCED_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0x03)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT, ENABLE_DEFAULT_RESPONSE)

if capabilities & 2:# Check enhancedHueSupported in ColorCapabilities
  writeLog("28 Client sends enhanced move to hue command")
  sendEnhancedMoveToHueCommand(client1, 0xFFFF, ZCL_ZLL_MOVE_TO_HUE_DIRECTION_SHORTEST_DISTANCE, 0x0032)
  receiveAndCheck(server1, enhancedMoveToHueIndStr)
  receiveAndCheck(client1, zclDefRespReceivedIndStr % ZCL_INVALID_VALUE_STATUS)

  writeLog("29 Client sends enhanced move hue command")
  sendEnhancedMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_UP, 0x01f4)
  receiveAndCheck(server1, enhancedMoveHueIndStr)

  writeLog("30 Client sends enhanced move hue command")
  sendEnhancedMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_DOWN, 0x03e8)
  receiveAndCheck(server1, enhancedMoveHueIndStr)

  writeLog("31 Client sends enhanced move hue command")
  sendEnhancedMoveHueCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_STOP, 1)
  receiveAndCheck(server1, enhancedMoveHueIndStr)

  writeLog("32 Client sends enhanced step hue command")
  sendEnhancedStepHueCommand(client1, ZCL_ZLL_STEP_SATURATION_STEP_MODE_UP, 0x4000, 0x0a)
  receiveAndCheck(server1, enhancedStepHueIndStr)

  writeLog("33 Client sends enhanced move to hue and saturation command")
  sendEnhancedMoveToHueAndSaturationCommand(client1, 45000, 0x7f, 0x0064)
  receiveAndCheck(server1, enhancedMoveToHueAndSaturationIndStr)

  writeLog("34 Client sends enhanced move to hue and saturation command")
  sendEnhancedMoveToHueAndSaturationCommand(client1, 0xFFFF, 0xfe, 0x0064)
  receiveAndCheck(server1, enhancedMoveToHueAndSaturationIndStr)
  receiveAndCheck(client1, zclDefRespReceivedIndStr % ZCL_INVALID_VALUE_STATUS)

if capabilities & 8:# Check XYAttributesSupported in ColorCapabilities
  writeLog("35a Client sends move to color command")
  sendMoveToColorCommand(client1, 20000, 20000, 0x0064)
  receiveAndCheck(server1, moveToColorIndStr)

writeLog("35b Client sends stop move step command")
sendStopMoveStepHueCommand(client1)

