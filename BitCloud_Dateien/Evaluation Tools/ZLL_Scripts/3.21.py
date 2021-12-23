"""
@testcase
@description 3.21 TP-CST-TC-21: Color control cluster (color temperature) with server as DUT

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

writeLog("P5 Client sends move to color temperature command")
sendMoveToColorTemperatureCommand(client1, 100, 0x000a) #100-Random
receiveAndCheck(server1, moveToColorTemperatureIndStr)

idle([client1, server1])
#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 Client sends read attribute command")
colorTemp = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID)
print('colorTemp', colorTemp)
tempPhyMin = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMP_PHYSICAL_MIN_SERVER_ATTRIBUTE_ID)
print('tempPhyMin', tempPhyMin)
tempPhyMax = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMP_PHYSICAL_MAX_SERVER_ATTRIBUTE_ID)
print('tempPhyMax', tempPhyMax)
tempGrad = (int)(tempPhyMax - tempPhyMin) / 40
print('tempGrad', tempGrad)

writeLog("2a Client sends move to color temperature command")
sendMoveToColorTemperatureCommand(client1, tempPhyMin + tempGrad * 20, 0x0064)
receiveAndCheck(server1, moveToColorTemperatureIndStr)

sleep(12)

writeLog("2b Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID) == tempPhyMin + tempGrad * 20)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0x02)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_ENHANCED_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0x02)

writeLog("3a Client sends move to color temperature command")
sendMoveToColorTemperatureCommand(client1, tempPhyMax + 1, 0x0064)
receiveAndCheck(server1, moveToColorTemperatureIndStr)
receiveAndCheck(client1, zclDefRespReceivedIndStr % ZCL_SUCCESS_STATUS)

sleep(12)

writeLog("3b Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID) == tempPhyMax)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0x02)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_ENHANCED_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0x02)

writeLog("4a Client sends move to color temperature command")
sendMoveToColorTemperatureCommand(client1, tempPhyMin - 1, 0x0064)
receiveAndCheck(server1, moveToColorTemperatureIndStr)
receiveAndCheck(client1, zclDefRespReceivedIndStr % ZCL_SUCCESS_STATUS)

sleep(12)

writeLog("4b Client sends read attribute command")
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID) == tempPhyMin)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0x02)
check(readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_ENHANCED_COLOR_MODE_SERVER_ATTRIBUTE_ID) == 0x02)

writeLog("5a Client sends move color temperature command")
sendMoveColorTemperatureCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_UP, 3 * tempGrad, 0, tempPhyMax - tempGrad)
receiveAndCheck(server1, moveColorTemperatureIndStr)

sleep(10)

writeLog("5b Client sends move color temperature command")
sendMoveColorTemperatureCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_STOP, 1, 0, 0)
receiveAndCheck(server1, moveColorTemperatureIndStr)

writeLog("5c Client sends read attribute command")
currColorTemp = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID)
check(currColorTemp >= (tempPhyMin + tempGrad * 28) and currColorTemp <= (tempPhyMin + tempGrad * 32)) # 5 percent window near 11000

writeLog("6a Client sends move color temperature command")
sendMoveColorTemperatureCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_UP, tempGrad, 0, tempPhyMin + 34 * tempGrad)
receiveAndCheck(server1, moveColorTemperatureIndStr)

sleep(6)

writeLog("6b Client sends read attribute command")
currColorTemp = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID)
check(currColorTemp >= (tempPhyMin + 32 * tempGrad) and currColorTemp <= (tempPhyMin + 36 * tempGrad)) # 5 percent window near 15000

writeLog("7a Client sends move color temperature command")
sendMoveColorTemperatureCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_DOWN, 2 * tempGrad, tempGrad + tempPhyMin, 0)
receiveAndCheck(server1, moveColorTemperatureIndStr)

sleep(10)

writeLog("7b Client sends move color temperature command")
sendMoveColorTemperatureCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_STOP, 1, 0, 0)
receiveAndCheck(server1, moveColorTemperatureIndStr)

writeLog("7c Client sends read attribute command")
currColorTemp = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID)
check(currColorTemp >= (tempPhyMin + 12 * tempGrad) and currColorTemp <= (tempPhyMin + 16 * tempGrad)) # 5 percent window near 10000

writeLog("8a Client sends move color temperature command")
sendMoveColorTemperatureCommand(client1, ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_DOWN, 2 * tempGrad, 8 * tempGrad + tempPhyMin, 0)
receiveAndCheck(server1, moveColorTemperatureIndStr)

sleep(5)

writeLog("8b Client sends read attribute command")
currColorTemp = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID)
check(currColorTemp >= (6 * tempGrad + tempPhyMin) and currColorTemp <= (10 * tempGrad + tempPhyMin)) # 5 percent window near 7000

writeLog("9a Client sends step color temperature command")
sendStepColorTemperatureCommand(client1, ZCL_ZLL_STEP_SATURATION_STEP_MODE_UP, 20 * tempGrad, 0x00c8, tempPhyMin, tempPhyMax - tempGrad)
receiveAndCheck(server1, stepColorTemperatureIndStr)

sleep(10)

writeLog("9b Client sends move color temperature command")
sendStopMoveStepHueCommand(client1)
receiveAndCheck(server1, stopMoveStepIndStr)

writeLog("9c Client sends read attribute command")
currColorTemp = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID)
check(currColorTemp >= (tempPhyMin + 16 * tempGrad) and currColorTemp <= (tempPhyMin + 20 * tempGrad)) # 5 percent window near 12000

writeLog("10a Client sends step color temperature command")
sendStepColorTemperatureCommand(client1, ZCL_ZLL_STEP_SATURATION_STEP_MODE_UP, 20 * tempGrad, 0x0032, 0, tempPhyMin + 30 * tempGrad)
receiveAndCheck(server1, stepColorTemperatureIndStr)

sleep(6)

writeLog("10b Client sends read attribute command")
currColorTemp = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID)
check(currColorTemp >= (tempPhyMin + 28 * tempGrad) and currColorTemp <= (tempPhyMin + 32 * tempGrad)) # 5 percent window near 15000

writeLog("11a Client sends step color temperature command")
sendStepColorTemperatureCommand(client1, ZCL_ZLL_STEP_SATURATION_STEP_MODE_DOWN, 10 * tempGrad, 0x00c8, tempPhyMin + tempGrad, 0)
receiveAndCheck(server1, stepColorTemperatureIndStr)

sleep(10)

writeLog("11b Client sends stop move step temperature command")
sendStopMoveStepHueCommand(client1)
receiveAndCheck(server1, stopMoveStepIndStr)

writeLog("11c Client sends read attribute command")
currColorTemp = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID)
check(currColorTemp >= (tempPhyMin + 23 * tempGrad) and currColorTemp <= (tempPhyMin + 27 * tempGrad))

writeLog("12a Client sends step color temperature command")
sendStepColorTemperatureCommand(client1, ZCL_ZLL_STEP_SATURATION_STEP_MODE_DOWN, 10 * tempGrad, 0x0032, tempPhyMin + 19 * tempGrad, 0)
receiveAndCheck(server1, stepColorTemperatureIndStr)

sleep(6)

writeLog("12b Client sends read attribute command")
currColorTemp = readColorControlClusterAttribute(client1, ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID)
check(currColorTemp >= (tempPhyMin + 17 * tempGrad) and currColorTemp <= (tempPhyMin + 21 * tempGrad))
