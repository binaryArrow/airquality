from public import *
from common import *

#################################################################
#                     Common parameters
#################################################################

# Commissioning Server Cluster commands identifiers.
ZCL_COMMISSIONING_CLUSTER_ENDPOINT_INFORMATION_COMMAND_ID           = 0x40
ZCL_COMMISSIONING_CLUSTER_GET_GROUP_IDENTIFIERS_RESPONSE_COMMAND_ID = 0x41
ZCL_COMMISSIONING_CLUSTER_GET_ENDPOINT_LIST_RESPONSE_COMMAND_ID     = 0x42

# Commissioning Client Cluster commands identifiers.
ZCL_COMMISSIONING_CLUSTER_GET_GROUP_IDENTIFIERS_COMMAND_ID          = 0x41
ZCL_COMMISSIONING_CLUSTER_GET_ENDPOINT_LIST_COMMAND_ID              = 0x42

#################################################################
#                          Commands
#################################################################

# Sends endpoint information command.
# param[0] - endpoint id
sendEndpointInformationCmd = "sendEndpointInformation %d"

# Sends get group identifiers request command.
# param[0] - start index
getGroupIdentifiersReqCmd = "getGroupIdentifiersReq %d"

# Sends get endpoint list request command.
# param[0] - start index
getEndpointListReqCmd = "getEndpointListReq %d"

#################################################################
#                         Responses
#################################################################

# Indicates the reception of endpoint information command
endpointInformationIndStr = "endpointInformationInd(): epId = 0x%02x"

# Indicates the reception of get group identifiers request command
getGroupIdentifiersIndStr = "getGroupIdentifiersInd()"

# Indicates the reception of get endpoint list request command
getEndpointListIndStr = "getEndpointListInd()"

# The response on get group identifiers request command
getGroupIdentifiersRespStr = "getGroupIdentifiersResp()"
getGroupIdentifiersRespTotalStr = "total = %d"
getGroupIdentifiersRespGroupIdStr = "groupId = 0x%04x"

# The response on get endpoint list request command
getEndpointListRespStr = "GetEndpointListResp()"

#################################################################
#                         Functions
#################################################################

def sendEndpointInformationCommand(port, endpoint = 0):
  sendCommand(port, sendEndpointInformationCmd % endpoint)
  idle([port], timeout = 150)

def sendGetGroupIdentifiersReqCommand(port, startIndx):
  sendCommand(port, getGroupIdentifiersReqCmd % startIndx)
  idle([port], timeout = 150)

def sendGetEndpointListReqCommand(port, startIndx):
  sendCommand(port, getEndpointListReqCmd % startIndx)
  idle([port], timeout = 150)
