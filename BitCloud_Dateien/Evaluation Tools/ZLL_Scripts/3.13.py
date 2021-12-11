"""
@testcase
@description 3.13 TP-CST-TC-13: Scenes cluster with server as DUT

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

writeLog("Set addressing on client")
setAddressing(client1, APS_GROUP_ADDRESS, group1Id, APP_ENDPOINT_LIGHT)

writeLog("2 Client sends store scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_STORE_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, storeSceneIndStr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("3a Client sends off command")
sendOffCommand(client1)
receiveOffCommand(server1)
idle([client1, server1])

writeLog("3b Power off server1")
powerOff([server1])

writeLog("3c Power on server1")
powerOn([server1])
clearPorts([server1, client1])

writeLog("Set addressing on client")
setAddressing(client1, APS_GROUP_ADDRESS, group1Id, APP_ENDPOINT_LIGHT)

writeLog("3d Client sends recall scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_RECALL_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, recallSceneIndStr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

sleep(2)

writeLog("4 Client sends read attributes command")
check(readSceneClusterAttribute(client1, ZCL_SCENES_CLUSTER_SCENE_COUNT_SERVER_ATTRIBUTE_ID) == 0x01)
check(readSceneClusterAttribute(client1, ZCL_SCENES_CLUSTER_CURRENT_SCENE_SERVER_ATTRIBUTE_ID) == scene1Id)
check(readSceneClusterAttribute(client1, ZCL_SCENES_CLUSTER_CURRENT_GROUP_SERVER_ATTRIBUTE_ID) == 0x0001)
check(readSceneClusterAttribute(client1, ZCL_SCENES_CLUSTER_SCENE_VALID_SERVER_ATTRIBUTE_ID) == 1)
check(readSceneClusterAttribute(client1, ZCL_SCENES_CLUSTER_NAME_SUPPORT_SERVER_ATTRIBUTE_ID) == 0x00)

writeLog("5 Client sends view scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_VIEW_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, viewSceneIndStr % (group1Id, scene1Id))
receiveViewSceneResponse(client1, 
                         groupId = group1Id, 
                         sceneId = scene1Id, 
                         transitionTime = 0)

writeLog("6 Client sends get scene membership command")
sendGetSceneMembershipCommand(client1, group1Id)
receiveAndCheck(server1, getSceneMembershipIndStr % group1Id)
receiveGetSceneMembershipResponse(client1, group1Id, 1, [scene1Id])

writeLog("7a Client sends read scene count attribute command")
check(readSceneClusterAttribute(client1, ZCL_SCENES_CLUSTER_SCENE_COUNT_SERVER_ATTRIBUTE_ID) == 0x01)

writeLog("7b Client sends read current scene attribute command")
check(readSceneClusterAttribute(client1, ZCL_SCENES_CLUSTER_CURRENT_SCENE_SERVER_ATTRIBUTE_ID) == scene1Id)

writeLog("7c Client sends read current group attribute command")
check(readSceneClusterAttribute(client1, ZCL_SCENES_CLUSTER_CURRENT_GROUP_SERVER_ATTRIBUTE_ID) == 0x0001)

writeLog("7e Client sends read name support attribute command")
check(readSceneClusterAttribute(client1, ZCL_SCENES_CLUSTER_NAME_SUPPORT_SERVER_ATTRIBUTE_ID) == 0x00)

writeLog("8 Client sends remove all scenes command")
sendRemoveAllScenesCommand(client1, group1Id)
receiveAndCheck(server1, removeAllScenesIndStr % group1Id)
receiveRemoveAllScenesResponse(client1, group1Id)

writeLog("9 Client sends get scene membership command")
sendGetSceneMembershipCommand(client1, group1Id)
receiveAndCheck(server1, getSceneMembershipIndStr % group1Id)
receiveGetSceneMembershipResponse(client1, group1Id, 0, [])

writeLog("10a Client sends add scene command")
sendAddSceneCommand(client1, group1Id, scene1Id, 0x000a)
receiveAndCheck(server1, addSceneIndStr % (group1Id, scene1Id))
receiveAddSceneResponse(client1, group1Id, scene1Id)

writeLog("Set addressing on client")
setAddressing(client1, APS_GROUP_ADDRESS, group1Id, APP_ENDPOINT_LIGHT)

writeLog("10b Client sends add scene command")
sendAddSceneCommand(client1, group1Id, scene1Id, 0x000a)
receiveAndCheck(server1, addSceneIndStr % (group1Id, scene1Id))

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("11 Client sends get scene membership command")
sendGetSceneMembershipCommand(client1, group1Id)
receiveAndCheck(server1, getSceneMembershipIndStr % group1Id)
receiveGetSceneMembershipResponse(client1, group1Id, 1, [scene1Id])

writeLog("12 Client sends remove scene command")
sendRemoveSceneCommand(client1, group1Id, scene1Id)
receiveAndCheck(server1, removeSceneIndStr % (group1Id, scene1Id))
receiveRemoveSceneResponse(client1, group1Id, scene1Id)

writeLog("13 Client sends get scene membership command")
sendGetSceneMembershipCommand(client1, group1Id)
receiveAndCheck(server1, getSceneMembershipIndStr % group1Id)
receiveGetSceneMembershipResponse(client1, group1Id, 0, [])

writeLog("14 Client sends store scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_STORE_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, storeSceneIndStr)
receiveAndCheck(client1, storeSceneRespIndStr % 0)

writeLog("15 Client sends get scene membership command")
sendGetSceneMembershipCommand(client1, group1Id)
receiveAndCheck(server1, getSceneMembershipIndStr % group1Id)
receiveGetSceneMembershipResponse(client1, group1Id, 1, [scene1Id])

writeLog("16a Client sends enhanced add scene command")
sendEnhancedAddSceneCommand(client1, group1Id, scene1Id, 0x000a)
receiveAndCheck(server1, enhancedAddSceneIndStr % (group1Id, scene1Id))
receiveEnhancedAddSceneResponse(client1, group1Id, scene1Id)

writeLog("Set addressing on client")
setAddressing(client1, APS_GROUP_ADDRESS, group1Id, APP_ENDPOINT_LIGHT)

writeLog("16b Client sends enhanced add scene command")
sendEnhancedAddSceneCommand(client1, group1Id, scene1Id, 0x000a)
receiveAndCheck(server1, enhancedAddSceneIndStr % (group1Id, scene1Id))

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("17 Client sends enhanced view command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_ENHANCED_VIEW_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, enhancedViewSceneIndStr % (group1Id, scene1Id))
receiveEnhancedViewSceneResponse(client1, 
                                 groupId = group1Id, 
                                 sceneId = scene1Id, 
                                 transitionTime = 0x000a)

writeLog("18a Client sends copy scene command")
sendCopySceneCommand(client1, group1Id, scene2Id, group1Id, scene1Id)
receiveAndCheck(server1, copySceneIndStr)
receiveAndCheck(client1, copySceneRespIndStr % 0)

writeLog("Set addressing on client")
setAddressing(client1, APS_GROUP_ADDRESS, group1Id, APP_ENDPOINT_LIGHT)

writeLog("18b Client sends copy scene command")
sendCopySceneCommand(client1, group1Id, scene2Id, group1Id, scene1Id)
receiveAndCheck(server1, copySceneIndStr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, broadcastAllAddr, broadcastEndpoint)

writeLog("19 Client sends view scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_VIEW_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, viewSceneIndStr % (group1Id, scene1Id))

writeLog("20a Client sends remove scene command")
sendRemoveSceneCommand(client1, group1Id, scene1Id)
receiveAndCheck(server1, removeSceneIndStr % (group1Id, scene1Id))

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("20b Client sends get scene membership command")
sendGetSceneMembershipCommand(client1, group1Id)
receiveAndCheck(server1, getSceneMembershipIndStr % group1Id)
receiveGetSceneMembershipResponse(client1, group1Id, 1, [scene2Id])

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, broadcastAllAddr, broadcastEndpoint)

writeLog("21a Client sends remove all scenes command")
sendRemoveAllScenesCommand(client1, group1Id)
receiveAndCheck(server1, removeAllScenesIndStr % group1Id)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("21b Client sends get scene membership command")
sendGetSceneMembershipCommand(client1, group1Id)
receiveAndCheck(server1, getSceneMembershipIndStr % group1Id)
receiveGetSceneMembershipResponse(client1, group1Id, 0, [])

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, broadcastAllAddr, broadcastEndpoint)

writeLog("22a Client sends store scene command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_STORE_SCENE_COMMAND_ID, group1Id, scene3Id)
receiveAndCheck(server1, storeSceneIndStr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("22b Client sends get scene membership command")
sendGetSceneMembershipCommand(client1, group1Id)
receiveAndCheck(server1, getSceneMembershipIndStr % group1Id)
receiveGetSceneMembershipResponse(client1, group1Id, 1, [scene3Id])

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, broadcastAllAddr, broadcastEndpoint)

writeLog("23 Client sends get scene membership command")
sendGetSceneMembershipCommand(client1, group1Id)
receiveAndCheck(server1, getSceneMembershipIndStr % group1Id)

writeLog("24 Client sends enhanced view command")
sendSimpleSceneCommand(client1, ZCL_SCENES_CLUSTER_ENHANCED_VIEW_SCENE_COMMAND_ID, group1Id, scene1Id)
receiveAndCheck(server1, enhancedViewSceneIndStr % (group1Id, scene1Id))

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("25a Client sends add group command")
sendAddGroupCommand(client1, r1NwkAddr, APP_ENDPOINT_LIGHT, group2Id)
check(receiveAddGroupInd(server1) == group2Id)
receiveAndCheck(client1, addGroupResponseStr)
receiveAndCheck(client1, endpointInformationIndStr % APP_ENDPOINT_LIGHT)
receiveAndCheck(server1, zclDefRespReceivedIndStr % 0)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, broadcastAllAddr, broadcastEndpoint)

writeLog("25b Client sends copy scene command")
sendCopySceneCommand(client1, group2Id, 0, group1Id, 0, ZCL_SCENES_CLUSTER_COPY_ALL_SCENES)
receiveAndCheck(server1, copySceneIndStr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("25c Client sends get scene membership command")
sendGetSceneMembershipCommand(client1, group2Id)
receiveAndCheck(server1, getSceneMembershipIndStr % group2Id)
receiveGetSceneMembershipResponse(client1, group2Id, 1, [scene3Id])
