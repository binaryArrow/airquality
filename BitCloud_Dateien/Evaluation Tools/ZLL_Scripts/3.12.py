"""
@testcase
@description 3.12 TP-CST-TC-11: Groups cluster with client as DUT

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
from identifyCluster import *
from groupsCluster import *
from commissioningCluster import *
sys.path.remove(scriptPath)

group1Id = 0x0001
group2Id = 0x0002
group3Id = 0x0003
group4Id = 0x0004

broadcastAllAddr = 0xFFFF
broadcastEndpoint = 0xFF

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

writeLog("2 Client sends get group membership command")
sendGetGroupMembershipCommand(client1, [])
receiveAndCheck(server1, getGroupMembershipIndStr)
receiveGetGroupMembershipResp(client1, 1, [group1Id])

writeLog("3 Client sends view group #1 command")
sendViewGroupCommand(client1, group1Id)
check(receiveViewGroupInd(server1) == group1Id)
receiveViewGroupResp(client1, 0, group1Id)

writeLog("4 Client sends add group command")
sendAddGroupCommand(client1, broadcastAllAddr, broadcastEndpoint, group2Id)
check(receiveAddGroupInd(server1) == group2Id)
idle([client1, server1], 1000)

writeLog("5 Client sends view group #3 command")
sendViewGroupCommand(client1, group2Id)
check(receiveViewGroupInd(server1) == group2Id)
receiveViewGroupResp(client1, 0, group2Id)

writeLog("6 Client sends view group #42 command")
sendViewGroupCommand(client1, 0x0042)
check(receiveViewGroupInd(server1) == 0x0042)
receiveViewGroupResp(client1, ZCL_NOT_FOUND_STATUS, 0x0042)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, broadcastAllAddr, broadcastEndpoint)

writeLog("7 Client sends view group #1 command to all devices")
sendViewGroupCommand(client1, group1Id)
check(receiveViewGroupInd(server1) == group1Id)
idle([client1, server1], 1000)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("8 Client sends get group membership command")
sendGetGroupMembershipCommand(client1, [group1Id])
receiveAndCheck(server1, getGroupMembershipIndStr)
receiveGetGroupMembershipResp(client1, 1, [group1Id])

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, broadcastAllAddr, broadcastEndpoint)

writeLog("9 Client sends get group membership command")
sendGetGroupMembershipCommand(client1, [group2Id])
receiveAndCheck(server1, getGroupMembershipIndStr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("10 Client sends add group command")
sendAddGroupCommand(client1, r1NwkAddr, APP_ENDPOINT_LIGHT, group3Id)
check(receiveAddGroupInd(server1) == group3Id)
receiveAndCheck(client1, addGroupResponseStr)
receiveAndCheck(client1, endpointInformationIndStr % APP_ENDPOINT_LIGHT)
receiveAndCheck(server1, zclDefRespReceivedIndStr % 0)

writeLog("11 Client sends get group membership command")
sendGetGroupMembershipCommand(client1, [])
receiveAndCheck(server1, getGroupMembershipIndStr)
receiveGetGroupMembershipResp(client1, 3, [group1Id, group3Id, group2Id])

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, broadcastAllAddr, broadcastEndpoint)

writeLog("12 Client sends remove group command to all devices")
sendRemoveGroupCommand(client1, group2Id)
check(receiveRemoveGroupInd(server1) == group2Id)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("13 Client sends remove group command to server")
sendRemoveGroupCommand(client1, group3Id)
check(receiveRemoveGroupInd(server1) == group3Id)
receiveAndCheck(client1, removeGroupResponseStr)

writeLog("14 Client sends get group membership command")
sendGetGroupMembershipCommand(client1, [])
receiveAndCheck(server1, getGroupMembershipIndStr)
receiveGetGroupMembershipResp(client1, 1, [group1Id])

writeLog("15 Client sends remove all groups command")
sendRemoveAllGroupsCommand(client1)
receiveAndCheck(server1, removeAllGroupsIndStr)

writeLog("16 Client sends get group membership command")
sendGetGroupMembershipCommand(client1, [])
receiveAndCheck(server1, getGroupMembershipIndStr)
receiveGetGroupMembershipResp(client1, 0, [])

writeLog("17a Client sends an identify command")
sendIdentifyCommand(client1, identifyTime = 10)
receiveIdentify(server1)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, broadcastAllAddr, broadcastEndpoint)

writeLog("17b Client sends an add group if identifying command")
sendAddGroupIfIdentifyingCommand(client1, group4Id)
check(receiveAddGroupIfIdentifyingInd(server1) == group4Id)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("18 Client sends get group membership command")
sendGetGroupMembershipCommand(client1, [])
receiveAndCheck(server1, getGroupMembershipIndStr)
receiveGetGroupMembershipResp(client1, 1, [group4Id])

writeLog("19 Client reads NameSupport attribute")
check(readGroupsClusterAttribute(client1, ZCL_GROUPS_CLUSTER_NAME_SUPPORT_SERVER_ATTRIBUTE_ID) == 0)
