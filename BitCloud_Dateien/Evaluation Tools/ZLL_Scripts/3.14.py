"""
@testcase
@description 3.14 TP-CST-TC-14: Scenes cluster with client as DUT

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
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("P3 Client sends on command")
sendOnCommand(client1) 
receiveOnCommand(server1)

writeLog("P4 Client sends remove all groups command")
sendRemoveAllGroupsCommand(client1)
receiveAndCheck(server1, removeAllGroupsIndStr)

idle([client1, server1])
#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 Client sends add group command")
sendAddGroupCommand(client1, r1NwkAddr, APP_ENDPOINT_LIGHT, group1Id)
check(receiveAddGroupInd(server1) == group1Id)
receiveAndCheck(client1, addGroupResponseStr)
receiveAndCheck(client1, endpointInformationIndStr % APP_ENDPOINT_LIGHT)
receiveAndCheck(server1, zclDefRespReceivedIndStr % 0)

writeLog("2 Client sends add scene command")
sendAddSceneCommand(client1, group1Id, scene1Id, 0x000a)
receiveAndCheck(server1, addSceneIndStr % (group1Id, scene1Id))
receiveAddSceneResponse(client1, group1Id, scene1Id)

writeLog("3 Client sends view scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_VIEW_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, viewSceneIndStr % (group1Id, scene1Id))
receiveViewSceneResponse(client1, 
                         groupId = group1Id, 
                         sceneId = scene1Id, 
                         transitionTime = 0x000a)

writeLog("4 Client sends remove scene command")
sendRemoveSceneCommand(client1, group1Id, scene1Id)
receiveAndCheck(server1, removeSceneIndStr % (group1Id, scene1Id))
receiveRemoveSceneResponse(client1, group1Id, scene1Id)

writeLog("5 Client sends remove all scenes command")
sendRemoveAllScenesCommand(client1, group1Id)
receiveAndCheck(server1, removeAllScenesIndStr % group1Id)
receiveRemoveAllScenesResponse(client1, group1Id)

writeLog("6 Client sends store scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_STORE_SCENE_COMMAND_ID, group1Id, scene2Id)
receiveAndCheck(server1, storeSceneIndStr)
receiveAndCheck(client1, storeSceneRespIndStr % 0)

writeLog("7 Client sends recall scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_RECALL_SCENE_COMMAND_ID, group1Id, scene2Id)
receiveAndCheck(server1, recallSceneIndStr)

writeLog("8 Client sends get scene membership command")
sendGetSceneMembershipCommand(client1, group1Id)
receiveAndCheck(server1, getSceneMembershipIndStr % group1Id)
receiveGetSceneMembershipResponse(client1, group1Id, 1, [scene2Id])

writeLog("9 Client sends enhanced add scene command")
sendEnhancedAddSceneCommand(client1, group1Id, scene2Id, 0x000a)
receiveAndCheck(server1, enhancedAddSceneIndStr % (group1Id, scene2Id))
receiveEnhancedAddSceneResponse(client1, group1Id, scene2Id)

writeLog("10 Client sends enhanced view command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_ENHANCED_VIEW_SCENE_COMMAND_ID, group1Id, scene2Id)
receiveAndCheck(server1, enhancedViewSceneIndStr % (group1Id, scene2Id))
receiveEnhancedViewSceneResponse(client1, 
                                 groupId = group1Id, 
                                 sceneId = scene2Id, 
                                 transitionTime = 0x000a)

writeLog("11 Client sends copy scene command")
sendCopySceneCommand(client1, group1Id, scene3Id, group1Id, scene2Id)
receiveAndCheck(server1, copySceneIndStr)
receiveAndCheck(client1, copySceneRespIndStr % 0)
