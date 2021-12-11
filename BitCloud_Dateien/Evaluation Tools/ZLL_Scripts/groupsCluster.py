from public import *
from common import *

#################################################################
#                     Common parameters
#################################################################
# Groups Cluster client's command identifiers
ZCL_GROUPS_CLUSTER_ADD_GROUP_COMMAND_ID = 0x00
ZCL_GROUPS_CLUSTER_VIEW_GROUP_COMMAND_ID = 0x01
ZCL_GROUPS_CLUSTER_GET_GROUP_MEMBERSHIP_COMMAND_ID = 0x02
ZCL_GROUPS_CLUSTER_REMOVE_GROUP_COMMAND_ID = 0x03
ZCL_GROUPS_CLUSTER_REMOVE_ALL_GROUPS_COMMAND_ID = 0x04
ZCL_GROUPS_CLUSTER_ADD_GROUP_IF_IDENTIFYING_COMMAND_ID = 0x05

# Groups Cluster servers's command identifiers
ZCL_GROUPS_CLUSTER_ADD_GROUP_RESPONSE_COMMAND_ID = 0x00
ZCL_GROUPS_CLUSTER_VIEW_GROUP_RESPONSE_COMMAND_ID = 0x01
ZCL_GROUPS_CLUSTER_GET_GROUP_MEMBERSHIP_RESPONSE_COMMAND_ID = 0x02
ZCL_GROUPS_CLUSTER_REMOVE_GROUP_RESPONSE_COMMAND_ID = 0x03

# Groups Cluster server's attributes identifiers
ZCL_GROUPS_CLUSTER_NAME_SUPPORT_SERVER_ATTRIBUTE_ID = 0x0000

#################################################################
#                          Commands
#################################################################

# Sends add group command.
# param[0] - group id.
addGroupCmd = "addGroup %d %d %d"

# Sends remove group command.
# param[0] - group id.
removeGroupCmd = "removeGroup %d"

# Sends remove all groups command.
removeAllGroupsCmd = "removeAllGroups"

# Sends get group membership command.
# param[0] - group count.
# param[1] - group list 1st entity.
getGroupMembershipCmd = "getGroupMembership %d %d"

# Sends view group command.
# param[0] - group identifier.
viewGroupCmd = "viewGroup %d"

# Sends add group if identifying command.
# param[0] - group identifier.
addGroupIfIdentifyingCmd = "addGroupIfIdentifying %d"

# Sends read scene attribute command.
# param[0] - attribute to be read.
readGroupsClusterAttrCmd = "readGroupsAttr %d"

#################################################################
#                         Responses
#################################################################

# Indicates that Remove All Groups command has been received
removeAllGroupsIndStr = "removeAllGroupsInd()"

# Indicates that Remove Group command has been received
removeGroupIndStr = "removeGroupInd():" # Group number is ommited as unpredictable

# Indicates that group has been added
addGroupIndStr = "addGroupInd():" # Group number is ommited as unpredictable

# Indicates that Get Groups Membership command has been received
getGroupMembershipIndStr = "getGroupMembershipInd()"

# Indicates that View Group command has been received
viewGroupIndStr = "viewGroupInd()"

# Indicates that Add Group If Identifying command has been received
addGroupIfIdentifyingIndStr = "addGroupIfIdentifyingInd()"

# Indicates that Add Group Response command has been received
addGroupResponseStr = "addGroupResponseInd()"

# Indicates that Remove Group Response command has been received
removeGroupResponseStr = "removeGroupResponseInd()"

# Indicates that Get Group Membership Response command has been received
getGroupMembershipRespStr = "getGroupMembershipResponse()"
getGroupMembershipRespGroupCountStr = "groupCount = %d"
getGroupMembershipRespGroupStr = "groupId = 0x"

# Indicates that Get Group Membership Response command has been received
viewGroupRespStr = "viewGroupResponse(): status = 0x%02x"
viewGroupRespGroupStr = "groupId = 0x%04x"

readGroupsClusterAttrRespStr = "Attr 0x%04x = "

#################################################################
#                         Functions
#################################################################
def sendAddGroupCommand(port, destAddr, destEp, groupId):
  sendCommand(port, addGroupCmd % (destAddr, destEp, groupId))
  idle([port], timeout = 100)

def sendRemoveGroupCommand(port, groupId):
  sendCommand(port, removeGroupCmd % groupId)
  idle([port], timeout = 100)

def sendRemoveAllGroupsCommand(port):
  sendCommand(port, removeAllGroupsCmd)
  idle([port], timeout = 100)

def sendGetGroupMembershipCommand(port, groupList):
  if groupList:
    groupId = groupList[0] 
  else: 
    groupId = 0
  sendCommand(port, getGroupMembershipCmd % (len(groupList), groupId))
  idle([port], timeout = 100)

def receiveGetGroupMembershipResp(port, groupCount, groupList):
  receiveAndCheck(port, getGroupMembershipRespStr)
  buffer = receiveNextStr(port)
  print '<-' + buffer
  expectedString = getGroupMembershipRespGroupCountStr % groupCount
  check(buffer[:len(expectedString)] == expectedString)
  
  groups = {}
  for groupId in groupList:
    groups[groupId] = False
  
  for i in range(len(groupList)):
    buffer = receiveNextStr(port)
    print '<-' + buffer
    check(buffer[:len(getGroupMembershipRespGroupStr)] == getGroupMembershipRespGroupStr)
    groupId = int(buffer[len(getGroupMembershipRespGroupStr):], 16)
    groups[groupId] = True
    
  for groupId in groupList:
    check(groups[groupId] == True)
  
def sendViewGroupCommand(port, groupId):
  sendCommand(port, viewGroupCmd % groupId)
  idle([port], timeout = 100)
  
def receiveViewGroupResp(port, status, groupId):
  buffer = receiveNextStr(port)
  print '<-' + buffer
  expectedString = viewGroupRespStr % status
  check(buffer[:len(expectedString)] == expectedString)
  
  buffer = receiveNextStr(port)
  print '<-' + buffer
  expectedString = viewGroupRespGroupStr % groupId
  check(buffer[:len(expectedString)] == expectedString)

def sendAddGroupIfIdentifyingCommand(port, groupId):
  sendCommand(port, addGroupIfIdentifyingCmd % groupId)
  idle([port], timeout = 100)

def receiveInd(port, string):
  buffer = receiveNextStr(port)
  print '<-' + buffer
  buffer = buffer.strip().split()
  str = buffer[0].strip()
  groupId = buffer[1].strip()
  check(str[:len(string)] == string)
  return int(groupId[2:], 16)
  
def receiveAddGroupInd(port):
  return receiveInd(port, addGroupIndStr)
  
def receiveRemoveGroupInd(port):
  return receiveInd(port, removeGroupIndStr)

def receiveViewGroupInd(port):
  return receiveInd(port, viewGroupIndStr)

def receiveAddGroupIfIdentifyingInd(port):
  return receiveInd(port, addGroupIfIdentifyingIndStr)
  
def readGroupsClusterAttribute(port, attr):
  sendCommand(port, readGroupsClusterAttrCmd % attr)
  writeLog("Client receives response from server")
  receiveAndCheck(port, zclRespReceivedIndStr % 0)
  buffer = receiveNextStr(port)
  print '<-' + buffer
  expectedString = readGroupsClusterAttrRespStr % attr
  check(buffer[:len(expectedString)] == expectedString)
  attrValue = buffer[len(expectedString):]
  idle([port], timeout = 100)
  return int(attrValue)

  