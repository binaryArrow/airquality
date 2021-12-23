from public import *
from common import *

#################################################################
#                     Common parameters
#################################################################

ZCL_SCENES_CLUSTER_COPY_SINGLE_SCENE = 0x00
ZCL_SCENES_CLUSTER_COPY_ALL_SCENES   = 0x01

# Scenes Cluster server's attributes identifiers
ZCL_SCENES_CLUSTER_SCENE_COUNT_SERVER_ATTRIBUTE_ID    = 0x0000
ZCL_SCENES_CLUSTER_CURRENT_SCENE_SERVER_ATTRIBUTE_ID  = 0x0001
ZCL_SCENES_CLUSTER_CURRENT_GROUP_SERVER_ATTRIBUTE_ID  = 0x0002
ZCL_SCENES_CLUSTER_SCENE_VALID_SERVER_ATTRIBUTE_ID    = 0x0003
ZCL_SCENES_CLUSTER_NAME_SUPPORT_SERVER_ATTRIBUTE_ID   = 0x0004

# Scenes Cluster client's command identifiers
ZCL_SCENES_CLUSTER_ADD_SCENE_COMMAND_ID            = 0x00
ZCL_SCENES_CLUSTER_VIEW_SCENE_COMMAND_ID           = 0x01
ZCL_SCENES_CLUSTER_REMOVE_SCENE_COMMAND_ID         = 0x02
ZCL_SCENES_CLUSTER_REMOVE_ALL_SCENES_COMMAND_ID    = 0x03
ZCL_SCENES_CLUSTER_STORE_SCENE_COMMAND_ID          = 0x04
ZCL_SCENES_CLUSTER_RECALL_SCENE_COMMAND_ID         = 0x05
ZCL_SCENES_CLUSTER_GET_SCENE_MEMBERSHIP_COMMAND_ID = 0x06
ZCL_SCENES_CLUSTER_ENHANCED_ADD_SCENE_COMMAND_ID   = 0x40
ZCL_SCENES_CLUSTER_ENHANCED_VIEW_SCENE_COMMAND_ID  = 0x41
ZCL_SCENES_CLUSTER_COPY_SCENE_COMMAND_ID           = 0x42

#################################################################
#                          Commands
#################################################################

# Sends simple scene command.
# param[0] - command.
# param[1] - group identifier.
# param[2] - scene identifier.
sceneCmd = "scene %d %d %d"

# Sends get scene membership command.
# param[0] - groupId.
getSceneMembershipCmd = "getSceneMembership %d"

# Sends remove all scenes command.
# param[0] - groupId.
removeAllScenesCmd = "removeAllScenes %d"

# Sends add scene command.
# param[0] - groupId.
# param[1] - sceneId.
# param[0] - transition time.
sendAddSceneCmd = "addScene %d %d %d"

# Sends remove scene command.
# param[0] - groupId.
# param[1] - sceneId.
sendRemoveSceneCmd = "removeScene %d %d"

# Sends add scene command.
# param[0] - groupId.
# param[1] - sceneId.
# param[2] - transition time.
sendEnhancedAddSceneCmd = "enhancedAddScene %d %d %d"

# Sends add scene command.
# param[0] - destination groupId.
# param[1] - destination sceneId.
# param[2] - source groupId.
# param[3] - source sceneId.
# param[4] - copy mode.
sendCopySceneCmd = "copyScene %d %d %d %d %d"

# Sends read scene attribute command.
# param[0] - attribute to be read.
readSceneClusterAttrCmd = "readSceneAttr %d"

#################################################################
#                         Responses
#################################################################

readSceneClusterAttrRespStr = "Attr 0x%04x = "

# Indicates that add scene command has been received
addSceneIndStr = "addSceneInd(): 0x%04x, 0x%02x"
# Indicates that add scene response command has been received
addSceneRespIndStr = "Add scene response: status = 0x%02x"
addSceneRespGroupIdIndStr = "groupId = 0x%04x"
addSceneRespSceneIdIndStr = "sceneId = 0x%02x"

# Indicates that view scene command has been received
viewSceneIndStr = "viewSceneInd(): 0x%04x, 0x%02x"
# Indicates that view scene response command has been received
viewSceneRespIndStr = "View scene response: status = 0x%02x"
viewSceneRespIndGroupIdStr = "groupId = 0x%04x"
viewSceneRespIndSceneIdStr = "sceneId = 0x%02x"
viewSceneRespIndTransitionTimeIdStr = "transitionTime = 0x%04x"

# Indicates that remove scene command has been received
removeSceneIndStr = "removeSceneInd(): 0x%04x, 0x%02x"
# Indicates that remove scene response command has been received
removeSceneRespIndStr = "Remove scene response: status = 0x%02x"
removeSceneRespGroupIdIndStr = "groupId = 0x%04x"
removeSceneRespSceneIdIndStr = "sceneId = 0x%02x"

# Indicates that remove all scenes command has been received
removeAllScenesIndStr = "removeAllScenesInd(): 0x%04x"
# Indicates that remove all scenes response command has been received
removeAllScenesRespIndStr = "Remove all scenes response: status = 0x%02x"
removeAllScenesRespGroupIdIndStr = "groupId = 0x%04x"

# Indicates that store scene command has been received
storeSceneIndStr = "storeSceneInd():"
# Indicates that store scene response has been received.
storeSceneRespIndStr = "Store scene response: status = 0x%02x"

# Indicates that recall scene command has been received
recallSceneIndStr = "recallSceneInd():"

# Indicates that get scene membership command has been received
getSceneMembershipIndStr = "getSceneMembershipInd(): 0x%04x"
# Indicates that get scene membership response command has been received
getSceneMembershipRespIndStr = "Get scene membership response: status = 0x%02x"
getSceneMembershipRespGroupIdIndStr = "groupId = 0x%04x"
getSceneMembershipRespSceneCountIndStr = "sceneCount = 0x%02x"
getSceneMembershipRespSceneIdIndStr = "sceneId = 0x"

# Indicates that enhanced add scene command has been received
enhancedAddSceneIndStr = "enhancedAddSceneInd(): 0x%04x, 0x%02x"

# Indicates that enhanced view scene command has been received
enhancedViewSceneIndStr = "enhancedViewSceneInd(): 0x%04x, 0x%02x"

# Indicates that copy scene command has been received
copySceneIndStr = "copySceneInd()"
# Indicates that copy scene response command has been received
copySceneRespIndStr = "Copy scene response: status = 0x%02x"

#################################################################
#                         Functions
#################################################################
def sendSimpleSceneCommand(port, command, group, scene):
  sendCommand(port, sceneCmd % (command, group, scene))
  idle([port], timeout = 100)

def sendGetSceneMembershipCommand(port, groupId):
  sendCommand(port, getSceneMembershipCmd % groupId)
  idle([port], timeout = 100)

def sendRemoveAllScenesCommand(port, groupId):
  sendCommand(port, removeAllScenesCmd % groupId)
  idle([port], timeout = 100)

def sendAddSceneCommand(port, groupId, sceneId, transitionTime):
  sendCommand(port, sendAddSceneCmd % (groupId, sceneId, transitionTime))
  idle([port], timeout = 100)

def sendRemoveSceneCommand(port, groupId, sceneId):
  sendCommand(port, sendRemoveSceneCmd % (groupId, sceneId))
  idle([port], timeout = 100)

def sendEnhancedAddSceneCommand(port, groupId, sceneId, transitionTime):
  sendCommand(port, sendEnhancedAddSceneCmd % (groupId, sceneId, transitionTime))
  idle([port], timeout = 100)

def sendCopySceneCommand(port, destGroupId, destSceneId, srcGroupId, srcGceneId, mode = ZCL_SCENES_CLUSTER_COPY_SINGLE_SCENE):
  sendCommand(port, sendCopySceneCmd % (destGroupId, destSceneId, srcGroupId, srcGceneId, mode))
  idle([port], timeout = 100)
  
def receiveViewSceneResponse(port, groupId, sceneId, transitionTime, status = 0):
  receiveAndCheck(port, viewSceneRespIndStr % status)
  receiveAndCheck(port, viewSceneRespIndGroupIdStr % groupId)
  receiveAndCheck(port, viewSceneRespIndSceneIdStr % sceneId)
  receiveAndCheck(port, viewSceneRespIndTransitionTimeIdStr % transitionTime)

def receiveGetSceneMembershipResponse(port, groupId, scenesCount, sceneList, status = 0):
  receiveAndCheck(port, getSceneMembershipRespIndStr % status)
  receiveAndCheck(port, getSceneMembershipRespGroupIdIndStr % groupId)
  receiveAndCheck(port, getSceneMembershipRespSceneCountIndStr % scenesCount)
  
  scenes = {}
  for sceneId in sceneList:
    scenes[sceneId] = False
    
  for i in range(len(sceneList)):
    buffer = receiveNextStr(port)
    print '<-' + buffer
    check(buffer[:len(getSceneMembershipRespSceneIdIndStr)] == getSceneMembershipRespSceneIdIndStr)
    sceneId = int(buffer[len(getSceneMembershipRespSceneIdIndStr):], 16)
    scenes[sceneId] = True
    
  for sceneId in sceneList:
    check(scenes[sceneId] == True)

def receiveRemoveAllScenesResponse(port, groupId, status = 0):
  receiveAndCheck(port, removeAllScenesRespIndStr % status)
  receiveAndCheck(port, removeAllScenesRespGroupIdIndStr % groupId)

def receiveAddSceneResponse(port, groupId, sceneId, status = 0):
  receiveAndCheck(port, addSceneRespIndStr % status)
  receiveAndCheck(port, addSceneRespGroupIdIndStr % groupId)
  receiveAndCheck(port, addSceneRespSceneIdIndStr % sceneId)

def receiveRemoveSceneResponse(port, groupId, sceneId, status = 0):
  receiveAndCheck(port, removeSceneRespIndStr % status)
  receiveAndCheck(port, removeSceneRespGroupIdIndStr % groupId)
  receiveAndCheck(port, removeSceneRespSceneIdIndStr % sceneId)

def receiveEnhancedAddSceneResponse(port, groupId, sceneId, status = 0):
  receiveAddSceneResponse(port, groupId, sceneId, status)

def receiveEnhancedViewSceneResponse(port, groupId, sceneId, transitionTime, status = 0):
  receiveViewSceneResponse(port, groupId, sceneId, transitionTime, status)
  
def readSceneClusterAttribute(port, attr, status = 0):
  sendCommand(port, readSceneClusterAttrCmd % attr)
  writeLog("Client receives response from server")
  receiveAndCheck(port, zclRespReceivedIndStr % status)
  buffer = receiveNextStr(port)
  print '<-' + buffer
  expectedString = readSceneClusterAttrRespStr % attr
  check(buffer[:len(expectedString)] == expectedString)
  attrValue = buffer[len(expectedString):]
  idle([port], timeout = 100)
  return int(attrValue)
