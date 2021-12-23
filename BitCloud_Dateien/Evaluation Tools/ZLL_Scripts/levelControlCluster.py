from public import *
from common import *

#################################################################
#                     Common parameters
#################################################################

ZCL_LEVEL_CONTROL_CLUSTER_MINIMUM_LEVEL = 1
ZCL_LEVEL_CONTROL_CLUSTER_MEDIUM_LEVEL = 128
ZCL_LEVEL_CONTROL_CLUSTER_MAXIMUM_LEVEL = 254

ZCL_LEVEL_CONTROL_CLUSTER_MODE_UP = 0x00
ZCL_LEVEL_CONTROL_CLUSTER_MODE_DOWN = 0x01

# Level Control Cluster server's attributes identifiers
ZCL_LEVEL_CONTROL_CLUSTER_CURRENT_LEVEL_ATTRIBUTE_ID          = 0x0000
ZCL_LEVEL_CONTROL_CLUSTER_REMAINING_TIME_ATTRIBUTE_ID         = 0x0001
ZCL_LEVEL_CONTROL_CLUSTER_ON_OFF_TRANSITION_TIME_ATTRIBUTE_ID = 0x0010
ZCL_LEVEL_CONTROL_CLUSTER_ON_LEVEL_ATTRIBUTE_ID               = 0x0011

# On/Off Cluster client's command identifiers
ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_COMMAND_ID          = 0x00
ZCL_LEVEL_CONTROL_CLUSTER_MOVE_COMMAND_ID                   = 0x01
ZCL_LEVEL_CONTROL_CLUSTER_STEP_COMMAND_ID                   = 0x02
ZCL_LEVEL_CONTROL_CLUSTER_STOP_COMMAND_ID                   = 0x03
ZCL_LEVEL_CONTROL_CLUSTER_MOVE_TO_LEVEL_W_ONOFF_COMMAND_ID  = 0x04
ZCL_LEVEL_CONTROL_CLUSTER_MOVE_W_ONOFF_COMMAND_ID           = 0x05
ZCL_LEVEL_CONTROL_CLUSTER_STEP_W_ONOFF_COMMAND_ID           = 0x06
ZCL_LEVEL_CONTROL_CLUSTER_STOP_W_ONOFF_COMMAND_ID           = 0x07

#################################################################
#                          Commands
#################################################################

# Sends simple level control command.
# param[0] - command.
levelControlCmd = "levelControl %d"

# Sends move to level command.
# param[0] - command.
# param[1] - target level.
# param[2] - time.
moveToLevelCmd = "moveToLevel %d %d %d"

# Sends move command.
# param[0] - command.
# param[1] - move mode.
# param[2] - rate.
moveCmd = "move %d %d %d"

# Sends step command.
# param[0] - command.
# param[1] - step mode.
# param[2] - step size.
# param[3] - transition time.
stepCmd = "step %d %d %d %d"

# Sends read scene attribute command.
# param[0] - attribute to be read.
readLevelControlClusterAttrCmd = "readLevelControlAttr %d"

#################################################################
#                         Responses
#################################################################

readLevelControlClusterAttrRespStr = "Attr 0x%04x = "

#################################################################
#                         Functions
#################################################################
def sendSimpleLevelControlCommand(port, command):
  sendCommand(port, levelControlCmd % command)
  idle([port], timeout = 200)

def sendMoveToLevelCommand(port, command, level, time = 5):
  sendCommand(port, moveToLevelCmd % (command, level, time))
  idle([port], timeout = 200)

def sendMoveCommand(port, command, moveMode, rate):
  sendCommand(port, moveCmd % (command, moveMode, rate))
  idle([port], timeout = 200)

def sendStepCommand(port, command, stepMode, size, time):
  sendCommand(port, stepCmd % (command, stepMode, size, time))
  idle([port], timeout = 200)
  
def readLevelControlClusterAttribute(port, attr):
  sendCommand(port, readLevelControlClusterAttrCmd % attr)
  writeLog("Client receives response from server")
  receiveAndCheck(port, zclRespReceivedIndStr % 0)
  buffer = receiveNextStr(port)
  print '<-' + buffer
  expectedString = readLevelControlClusterAttrRespStr % attr
  check(buffer[:len(expectedString)] == expectedString)
  attrValue = buffer[len(expectedString):]
  idle([port], timeout = 100)
  return int(attrValue)
