from public import *
from common import *

#################################################################
#                     Common parameters
#################################################################

# Identify Server Cluster attributes identifiers.
ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID = 0x0000

# Identify Server Cluster commands identifiers.
ZCL_IDENTIFY_CLUSTER_IDENTIFY_QUERY_RESPONSE_COMMAND_ID = 0x00

# Identify Client Cluster commands identifiers.
ZCL_IDENTIFY_CLUSTER_IDENTIFY_COMMAND_ID = 0x00
ZCL_IDENTIFY_CLUSTER_IDENTIFY_QUERY_COMMAND_ID = 0x01
ZCL_IDENTIFY_CLUSTER_TRIGGER_EFFECT_COMMAND_ID = 0x40

# Possible values for the Effect Identifier field.
ZCL_EFFECT_IDENTIFIER_BLINK = 0x00
ZCL_EFFECT_IDENTIFIER_BREATHE = 0x01
ZCL_EFFECT_IDENTIFIER_OKAY = 0x02
ZCL_EFFECT_IDENTIFIER_CHANNEL_CHANGE = 0x0b
ZCL_EFFECT_IDENTIFIER_FINISH_EFFECT = 0xfe
ZCL_EFFECT_IDENTIFIER_STOP_EFFECT = 0xff

# Possible values for the Effect Variant field.
ZCL_EFFECT_VARIANT_DEFAULT = 0x00
ZCL_EFFECT_VARIANT_UNKNOWN = 0x42

#################################################################
#                          Commands
#################################################################

# Sends identify command.
# param[0] - identify time
identifyCmd = "identify %d"

# Sends identify query command.
identifyQueryCmd = "identifyQuery"

# Sends trigger effect command.
# param[0] - effect identifier
# param[1] - effect variant
triggerEffectCmd = "triggerEffect %d %d"

# Read identify cluster attribute on remote device
# param[0] - attribute id.
readIdentifyClusterAttrCmd = "readIdentifyAttr %d"

# Write identify cluster attribute on remote device
# param[0] - attribute id.
# param[1] - attribute type.
# param[2] - value to write.
writeIdentifyClusterAttrCmd = "writeIdentifyAttr %d %d %d"

#################################################################
#                         Responses
#################################################################

readIdentifyClusterAttrRespStr = "Attr 0x%04x = "

# The response on identify query command
identifyQueryRespStr = "IdentifyQueryResp: timeout = 0x"

# Indicates that an identify command has been received
identifyIndStr = "Identify"

# Indicates that an trigger effect command has been received
triggerEffectIndStr = "TriggerEffect %d"

#################################################################
#                         Functions
#################################################################
def sendIdentifyCommand(port, identifyTime = 0x3C):
  sendCommand(port, identifyCmd % identifyTime)

def sendIdentifyQueryCommand(port):
  sendCommand(port, identifyQueryCmd)

def sendTriggerEffectCommand(port, id, variant):
  sendCommand(port, triggerEffectCmd % (id, variant))

def readIdentifyClusterAttribute(port, attr):
  sendCommand(port, readIdentifyClusterAttrCmd % attr)
  writeLog("Client receives response from server")
  receiveAndCheck(port, zclRespReceivedIndStr % 0)
  buffer = receiveNextStr(port)
  print '<-' + buffer
  expectedString = readIdentifyClusterAttrRespStr % attr
  check(buffer[:len(expectedString)] == expectedString)
  attrValue = buffer[len(expectedString):]
  try:
    attrValue = int(attrValue)
  except ValueError:
    attrValue = attrValue.strip()
  idle([port], timeout = 150)
  return attrValue

def writeIdentifyClusterAttribute(port, attr, type, value, retStatus = 0):
  sendCommand(port, writeIdentifyClusterAttrCmd % (attr, type, value))
  writeLog("Client receives response from server")
  receiveAndCheck(port, zclRespReceivedIndStr % retStatus)
  idle([port], timeout = 150)

def receiveIdentify(port):
  receiveAndCheck(port, identifyIndStr)
  
def receiveIdentifyQueryResponse(port):
  buffer = receiveNextStr(port)
  print '<-' + buffer
  check(buffer[:len(identifyQueryRespStr)] == identifyQueryRespStr)
  attrValue = buffer[len(identifyQueryRespStr):]
  return int(attrValue, 16)

def receiveTriggerEffect(port, effectId):
  receiveAndCheck(port, triggerEffectIndStr % effectId)
