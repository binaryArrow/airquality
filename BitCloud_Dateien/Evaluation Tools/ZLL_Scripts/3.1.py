"""
@testcase
@description 3.1 TP-CST-TC-01: On/off cluster with server as DUT

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
from groupsCluster import *
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

writeLog("P1 Power on client and server")
powerOn([client1, server1])

writeLog("P2 Touchlink client and server")
touchlink(client1, server1)
idle([client1, server1])

server1NwkAddr = getNwkAddress(server1)
writeLog("R1 network address - 0x%04X" % server1NwkAddr)

client1NwkAddr = getNwkAddress(client1)
writeLog("ED1 network address - 0x%04X" % client1NwkAddr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, server1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("P3 Client sends OFF command to server")
sendOffCommand(client1)
receiveOffCommand(server1)

writeLog("P4 Client sends read attribute command to server to read onOff attribute")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)

writeLog("P5 Client sends Add Group command to server")
sendAddGroupCommand(client1, server1NwkAddr, APP_ENDPOINT_LIGHT, group1Id)
check(receiveAddGroupInd(server1) == group1Id)
receiveAndCheck(client1, addGroupResponseStr)
receiveAndCheck(client1, endpointInformationIndStr % APP_ENDPOINT_LIGHT)
receiveAndCheck(server1, zclDefRespReceivedIndStr % 0)

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

writeLog("4 Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)

writeLog("5 Client sends toggle command")
sendToggleCommand(client1)
receiveToggleCommand(server1)

writeLog("6 Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)

writeLog("7a Client sends on command")
sendOnCommand(client1)
receiveOnCommand(server1)

writeLog("7b Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_GLOBAL_SCENE_CONTROL_SERVER_ATTRIBUTE_ID) == 1)

writeLog("8a Client sends off with effect command")
sendOffWithEffectCmd(client1, 0x00, 0x00)

sleep(5)

writeLog("8b After 5 s client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_GLOBAL_SCENE_CONTROL_SERVER_ATTRIBUTE_ID) == 0)

writeLog("9a Client sends on with recall global scene command")
sendOnWithRecallCommand(client1)

writeLog("9b Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_GLOBAL_SCENE_CONTROL_SERVER_ATTRIBUTE_ID) == 1)

writeLog("10 Client sends store scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_STORE_SCENE_COMMAND_ID, group1Id, 0x01)
receiveAndCheck(server1, storeSceneIndStr)
receiveAndCheck(client1, storeSceneRespIndStr % 0)

writeLog("11a Client sends off with effect command")
sendOffWithEffectCmd(client1, 0x00, 0x00)

sleep(5)

writeLog("11b Client sends recall scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_RECALL_SCENE_COMMAND_ID, group1Id, 0x01)
receiveAndCheck(server1, recallSceneIndStr)

writeLog("11c Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_GLOBAL_SCENE_CONTROL_SERVER_ATTRIBUTE_ID) == 1)

writeLog("12a Client sends off with effect command with Dying light effect")
sendOffWithEffectCmd(client1, 0x01, 0x00)

sleep(2)

writeLog("12b Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_GLOBAL_SCENE_CONTROL_SERVER_ATTRIBUTE_ID) == 0)

writeLog("13a Client sends move to level command")
sendMoveToLevelCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MINIMUM_LEVEL + 1)

sleep(1)

writeLog("13b Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_GLOBAL_SCENE_CONTROL_SERVER_ATTRIBUTE_ID) == 1)

writeLog("14a Client sends on with recall global scene command")
sendOnWithRecallCommand(client1)

writeLog("14b Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_GLOBAL_SCENE_CONTROL_SERVER_ATTRIBUTE_ID) == 1)

writeLog("15 Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0)

writeLog("16a Client sends on with timed off with \'accept only if on\' condition")
sendOnWithTimedOffCmd(client1, 1, 300, 300)

writeLog("16b Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) <= 0x012C)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0x012C)

writeLog("17a Client sends on with timed off with \'accept only if on\' condition")
sendOnWithTimedOffCmd(client1, 1, 300, 300)

sleep(10)

writeLog("17b After 10s client sends on with timed off with \'accept only if on\' condition")
sendOnWithTimedOffCmd(client1, 1, 300, 300)

sleep(10)

writeLog("17c After 10s client sends on with timed off with \'accept only if on\' condition")
sendOnWithTimedOffCmd(client1, 1, 300, 300)

sleep(10)

writeLog("17d After 10s client sends on with timed off with \'accept only if on\' condition")
sendOnWithTimedOffCmd(client1, 1, 300, 300)

writeLog("17e Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) <= 0x012C)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0x012C)

sleep(10)

writeLog("18a After 10s client sends off with effect command")
sendOffWithEffectCmd(client1, 0x00, 0x00)

writeLog("18b Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
offWaitTimeCheck = readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID)
check(offWaitTimeCheck <= 0x012C)
check(offWaitTimeCheck > 0x0100)

sleep(10)

writeLog("19a After 10s client sends on with timed off with \'accept only if on\' condition")
sendOnWithTimedOffCmd(client1, 1, 300, 300)

writeLog("19b Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
offWaitTimeCheck = readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID)
check(offWaitTimeCheck <= 0x00C8)
check(offWaitTimeCheck > 0x0090)

sleep(10)

writeLog("20a After 10s client sends on command")
sendOnCommand(client1)
receiveOnCommand(server1)

writeLog("20b Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0)

sleep(10)

writeLog("21a After 10s client sends on with timed off with \'accept only if on\' condition")
sendOnWithTimedOffCmd(client1, 1, 300, 300)

sleep(10)

writeLog("21b After 10s client sends off command")
sendOffCommand(client1)
receiveOffCommand(server1)

writeLog("21c Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) <= 0x012C)

sleep(30)

writeLog("22 After 30s client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0)

writeLog("23a Client sends on with timed off with \'accept only if on\' condition")
sendOnWithTimedOffCmd(client1, 1, 300, 300)

writeLog("23b Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0)

writeLog("24a Client sends on command")
sendOnCommand(client1)
receiveOnCommand(server1)

sleep(10)

writeLog("24b After 10s client sends on with timed off with \'accept only if on\' condition")
sendOnWithTimedOffCmd(client1, 1, 300, 300)

writeLog("24c Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) <= 0x012C)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0x012C)

sleep(40)

writeLog("22 After 40s client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0)

writeLog("25a Client sends on with timed off")
sendOnWithTimedOffCmd(client1, 0, 300, 300)

writeLog("25b Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) <= 0x012C)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0x012C)

writeLog("26a Client sends on with timed off")
sendOnWithTimedOffCmd(client1, 0, 300, 300)

writeLog("26b Client sends on with timed off")
sendOnWithTimedOffCmd(client1, 0, 300, 300)

writeLog("26c Client sends on with timed off")
sendOnWithTimedOffCmd(client1, 0, 300, 300)

writeLog("26d Client sends on with timed off")
sendOnWithTimedOffCmd(client1, 0, 300, 300)

writeLog("26e Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) <= 0x012C)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0x012C)

writeLog("27a Client sends off command")
sendOffCommand(client1)
receiveOffCommand(server1)

writeLog("27b Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) <= 0x012C)

writeLog("28a Client sends on with timed off")
sendOnWithTimedOffCmd(client1, 0, 300, 300)

writeLog("28b Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) <= 0x012C)

writeLog("29a Client sends on command")
sendOnCommand(client1)
receiveOnCommand(server1)

writeLog("29b Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0)

writeLog("30a Client sends on with timed off")
sendOnWithTimedOffCmd(client1, 0, 300, 300)

writeLog("30b Client sends off command")
sendOffCommand(client1)
receiveOffCommand(server1)

writeLog("30c Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) <= 0x012C)

sleep(40)

writeLog("30d After 40s client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0)

sleep(10)

writeLog("31a Client sends on with timed off")
sendOnWithTimedOffCmd(client1, 0, 300, 300)

writeLog("31b Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) <= 0x012C)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0x012C)

sleep(40)

writeLog("31c After 40s client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0)

writeLog("32a Client sends on with timed off")
sendOnWithTimedOffCmd(client1, 0, 300, 300)

sleep(10)

writeLog("32b After 10s client sends move to level command")
sendMoveToLevelCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MINIMUM_LEVEL, time = 0)

writeLog("32c Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) <= 0x012C)

sleep(10)

writeLog("33a After 10s client sends move to level command")
sendMoveToLevelCommand(client1, ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_W_ONOFF_COMMAND_ID, ZCL_LEVEL_CONTROL_CLUSTER_MAXIMUM_LEVEL, time = 0)

writeLog("33b Client immediately sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID) == 0)
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID) == 0)

