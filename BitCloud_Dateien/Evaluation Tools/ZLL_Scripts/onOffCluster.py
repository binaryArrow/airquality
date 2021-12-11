from public import *
from common import *

#################################################################
#                     Common parameters
#################################################################

# On/Off Cluster server's attributes identifiers
ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID = 0x0000
ZCL_ONOFF_CLUSTER_GLOBAL_SCENE_CONTROL_SERVER_ATTRIBUTE_ID = 0x4000
ZCL_ONOFF_CLUSTER_ON_TIME_SERVER_ATTRIBUTE_ID = 0x4001
ZCL_ONOFF_CLUSTER_OFF_WAIT_TIME_SERVER_ATTRIBUTE_ID = 0x4002

# On/off cluster commands
ZCL_ONOFF_CLUSTER_OFF_COMMAND_ID = 0x00
ZCL_ONOFF_CLUSTER_ON_COMMAND_ID = 0x01
ZCL_ONOFF_CLUSTER_TOGGLE_COMMAND_ID = 0x02
ZCL_ONOFF_CLUSTER_OFF_WITH_EFFECT_COMMAND_ID = 0x40
ZCL_ONOFF_CLUSTER_ON_WITH_RECALL_GLOBAL_SCENE_COMMAND_ID = 0x41
ZCL_ONOFF_CLUSTER_ON_WITH_TIMED_OFF_COMMAND_ID = 0x42

#################################################################
#                          Commands
#################################################################

# Sends simple onOff command.
# param[0] - command.
onOffCmd = "onOff %d"

# Sends off with effect command.
# param[0] - effect identifier.
# param[1] - effect variant.
offWithEffectCmd = "offWithEffect %d %d"

# Sends on with timed off command.
# param[0] - on/off control.
# param[1] - on time.
# param[2] - off wait time.
onWithTimedOffCmd = "onWithTimedOff %d %d %d"

# Sends read onOff attribute command.
# param[0] - attribute to be read.
readOnOffClusterAttrCmd = "readOnOffAttr %d"


#################################################################
#                         Responses
#################################################################

readAttrRespStr = "Attr 0x%04x = "

# Indicates thet On command has been received.
onStr = "On"

# Indicates thet Off command has been received.
offStr = "Off"

# Indicates thet Toggle command has been received.
toggleStr = "Toggle"

#################################################################
#                         Functions
#################################################################
def sendOnWithRecallCommand(port):
  sendCommand(port, onOffCmd % ZCL_ONOFF_CLUSTER_ON_WITH_RECALL_GLOBAL_SCENE_COMMAND_ID)
  idle([port], timeout = 200)

def sendOffWithEffectCmd(port, effectId, effectVar):
  sendCommand(port, offWithEffectCmd % (effectId, effectVar))
  idle([port], timeout = 200)

def sendOnWithTimedOffCmd(port, onOffControl, onTime, offWaitTime):
  sendCommand(port, onWithTimedOffCmd % (onOffControl, onTime, offWaitTime))
  idle([port], timeout = 200)
  
def readOnOffClusterAttribute(port, attr):
  sendCommand(port, readOnOffClusterAttrCmd % attr)
  writeLog("Client receives response from server")
  receiveAndCheck(port, zclRespReceivedIndStr % 0)
  buffer = receiveNextStr(port)
  print '<-' + buffer
  expectedString = readAttrRespStr % attr
  check(buffer[:len(expectedString)] == expectedString)
  attrValue = buffer[len(expectedString):]
  idle([port], timeout = 200)
  return int(attrValue)

def sendOnCommand(port, status = BC_SUCCESS_STATUS):
  sendCommand(port, onOffCmd % ZCL_ONOFF_CLUSTER_ON_COMMAND_ID)
  if BC_SUCCESS_STATUS == status:
    idle([port], timeout = 200)
  else:
    if BC_DISCONNECTED_STATUS == status:
      receiveAndCheck(port, disconnectedStr)
      return receiveNextStr(port)
    if BC_CONNECTED_STATUS == status:
      receiveAndCheck(port, connectedStr)
    if BC_FAILURE_STATUS == status:
      receiveAndCheck(port, zclConfirmStr % ZDO_FAIL_STATUS)

def sendOffCommand(port, status = BC_SUCCESS_STATUS):
  sendCommand(port, onOffCmd % ZCL_ONOFF_CLUSTER_OFF_COMMAND_ID)
  if BC_SUCCESS_STATUS == status:
    idle([port], timeout = 200)
  else:
    if BC_DISCONNECTED_STATUS == status:
      receiveAndCheck(port, disconnectedStr)
      return receiveNextStr(port)
    if BC_CONNECTED_STATUS == status:
      receiveAndCheck(port, connectedStr)
    if BC_FAILURE_STATUS == status:
      receiveAndCheck(port, zclConfirmStr % ZDO_FAIL_STATUS)

def sendToggleCommand(port, status = BC_SUCCESS_STATUS):
  sendCommand(port, onOffCmd % ZCL_ONOFF_CLUSTER_TOGGLE_COMMAND_ID)
  if BC_SUCCESS_STATUS == status:
    idle([port], timeout = 200)
  else:
    if BC_DISCONNECTED_STATUS == status:
      receiveAndCheck(port, disconnectedStr)
      return receiveNextStr(port)
    if BC_CONNECTED_STATUS == status:
      receiveAndCheck(port, connectedStr)
    if BC_FAILURE_STATUS == status:
      receiveAndCheck(port, zclConfirmStr % ZDO_FAIL_STATUS)

def receiveOnCommand(port):
  receiveAndCheck(port, onStr)

def receiveOffCommand(port):
  receiveAndCheck(port, offStr)

def receiveToggleCommand(port):
  receiveAndCheck(port, toggleStr)

def sendToggleCommandErr(port):
  sendCommand(port, onOffCmd % ZCL_ONOFF_CLUSTER_TOGGLE_COMMAND_ID)
  return receiveNextStr(port)
