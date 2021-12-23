from public import *
from common import *

#################################################################
#                     Common parameters
#################################################################

# Atribute Ids of Basic Device Information Attribute Set at the server side
# ZCL Basic Cluster server side ZCLVersion attribute id
ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID             = 0x0000
# ZCL Basic Cluster server side ApplicationVersion attribute id
ZCL_BASIC_CLUSTER_SERVER_APPLICATION_VERSION_ATTRIBUTE_ID     = 0x0001
# ZCL Basic Cluster server side StackVersion attribute id
ZCL_BASIC_CLUSTER_SERVER_STACK_VERSION_ATTRIBUTE_ID           = 0x0002
# ZCL Basic Cluster server side HWVersion attribute id
ZCL_BASIC_CLUSTER_SERVER_HW_VERSION_ATTRIBUTE_ID              = 0x0003
# ZCL Basic Cluster server side ManufacturerName attribute id
ZCL_BASIC_CLUSTER_SERVER_MANUFACTURER_NAME_ATTRIBUTE_ID       = 0x0004
# ZCL Basic Cluster server side ModelIdentifier attribute id
ZCL_BASIC_CLUSTER_SERVER_MODEL_IDENTIFIER_ATTRIBUTE_ID        = 0x0005
# ZCL Basic Cluster server side DateCode attribute id
ZCL_BASIC_CLUSTER_SERVER_DATE_CODE_ATTRIBUTE_ID               = 0x0006
# ZCL Basic Cluster server side PowerSource attribute id
ZCL_BASIC_CLUSTER_SERVER_POWER_SOURCE_ATTRIBUTE_ID            = 0x0007

# Atribute Ids of Basic Device Settings Attribute Set at the server side
# ZCL Basic Cluster server side LocationDescription attribute id
ZCL_BASIC_CLUSTER_SERVER_LOCATION_DESCRIPTION_ATTRIBUTE_ID    = 0x0010
# ZCL Basic Cluster server side PhysicalEnvironment attribute id
ZCL_BASIC_CLUSTER_SERVER_PHYSICAL_ENVIRONMENT_ATTRIBUTE_ID    = 0x0011
# ZCL Basic Cluster server side DeviceEnabled attribute id
ZCL_BASIC_CLUSTER_SERVER_DEVICE_ENABLED_ATTRIBUTE_ID          = 0x0012
# ZCL Basic Cluster server side AlarmMask attribute id
ZCL_BASIC_CLUSTER_SERVER_ALARM_MASK_ATTRIBUTE_ID              = 0x0013

# ZLL Basic Cluster server side SWBuildID attribute id
ZCL_BASIC_CLUSTER_SERVER_SW_BUILD_ID_ATTRIBUTE_ID             = 0x4000

# ZCL Basic Cluster server side ResetToFactoryDeafaults commabd id
ZCL_BASIC_CLUSTER_SERVER_RESET_TO_FACTORY_DEFAULTS_COMMAND_ID = 0x00

#################################################################
#                          Commands
#################################################################

# Read basic cluster attribute on remote device
# param[0] - attribute id.
readBasicClusterAttrCmd = "readBasicAttr %d"

# Write basic cluster attribute on remote device
# param[0] - attribute id.
# param[1] - attribute type.
# param[2] - value to write.
writeBasicClusterAttrCmd = "writeBasicAttr %d %d %d"

#################################################################
#                         Responses
#################################################################

readBasicClusterAttrRespStr = "Attr 0x%04x = "

#################################################################
#                         Functions
#################################################################
def readBasicClusterAttribute(port, attr, retStatus = 0):
  sendCommand(port, readBasicClusterAttrCmd % attr)

  if BC_DISCONNECTED_STATUS == retStatus:
    receiveAndCheck(port, disconnectedStr)
    return

  if BC_DISCONNECTED_RECONNECTED_SUCCESS_STATUS == retStatus:
    receiveAndCheck(port, disconnectedStr)
    receiveAndCheck(port, connectedStr)
    writeLog("Client receives response from server")
    receiveAndCheck(port, zclRespReceivedIndStr % BC_SUCCESS_STATUS)
  else:
    writeLog("Client receives response from server")
    receiveAndCheck(port, zclRespReceivedIndStr % retStatus)
  
  if retStatus == BC_SUCCESS_STATUS or \
   retStatus == BC_DISCONNECTED_RECONNECTED_SUCCESS_STATUS:
    buffer = receiveNextStr(port)
    print '<-' + buffer
    expectedString = readBasicClusterAttrRespStr % attr
    check(buffer[:len(expectedString)] == expectedString)
    attrValue = buffer[len(expectedString):]
    try:
      attrValue = int(attrValue)
    except ValueError:
      attrValue = attrValue.strip()
    idle([port], timeout = 150)
    return attrValue
  
  return None

def writeBasicClusterAttribute(port, attr, type, value, retStatus = 0):
  sendCommand(port, writeBasicClusterAttrCmd % (attr, type, value))
  writeLog("Client receives response from server")
  receiveAndCheck(port, zclRespReceivedIndStr % retStatus)
  idle([port], timeout = 150)
