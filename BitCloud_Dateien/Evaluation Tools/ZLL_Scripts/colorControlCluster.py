from public import *
from common import *

#################################################################
#                     Common parameters
#################################################################

# ZLL Cluster server's attributes identifiers
ZCL_ZLL_CLUSTER_CURRENT_HUE_SERVER_ATTRIBUTE_ID                    = 0x0000
ZCL_ZLL_CLUSTER_CURRENT_SATURATION_SERVER_ATTRIBUTE_ID             = 0x0001
ZCL_ZLL_CLUSTER_REMAINING_TIME_SERVER_ATTRIBUTE_ID                 = 0x0002
ZCL_ZLL_CLUSTER_CURRENT_X_SERVER_ATTRIBUTE_ID                      = 0x0003
ZCL_ZLL_CLUSTER_CURRENT_Y_SERVER_ATTRIBUTE_ID                      = 0x0004
ZCL_ZLL_CLUSTER_COLOR_TEMPERATURE_SERVER_ATTRIBUTE_ID              = 0x0007
ZCL_ZLL_CLUSTER_COLOR_MODE_SERVER_ATTRIBUTE_ID                     = 0x0008
ZCL_ZLL_CLUSTER_NUMBER_OF_PRIMARIES_SERVER_ATTRIBUTE_ID            = 0x0010
ZCL_ZLL_CLUSTER_PRIMARY_1_X_SERVER_ATTRIBUTE_ID                    = 0x0011
ZCL_ZLL_CLUSTER_PRIMARY_1_Y_SERVER_ATTRIBUTE_ID                    = 0x0012
ZCL_ZLL_CLUSTER_PRIMARY_1_INTENSITY_SERVER_ATTRIBUTE_ID            = 0x0013
ZCL_ZLL_CLUSTER_PRIMARY_2_X_SERVER_ATTRIBUTE_ID                    = 0x0015
ZCL_ZLL_CLUSTER_PRIMARY_2_Y_SERVER_ATTRIBUTE_ID                    = 0x0016
ZCL_ZLL_CLUSTER_PRIMARY_2_INTENSITY_SERVER_ATTRIBUTE_ID            = 0x0017
ZCL_ZLL_CLUSTER_PRIMARY_3_X_SERVER_ATTRIBUTE_ID                    = 0x0019
ZCL_ZLL_CLUSTER_PRIMARY_3_Y_SERVER_ATTRIBUTE_ID                    = 0x001A
ZCL_ZLL_CLUSTER_PRIMARY_3_INTENSITY_SERVER_ATTRIBUTE_ID            = 0x001B
ZCL_ZLL_CLUSTER_PRIMARY_4_X_SERVER_ATTRIBUTE_ID                    = 0x0020
ZCL_ZLL_CLUSTER_PRIMARY_4_Y_SERVER_ATTRIBUTE_ID                    = 0x0021
ZCL_ZLL_CLUSTER_PRIMARY_4_INTENSITY_SERVER_ATTRIBUTE_ID            = 0x0022
ZCL_ZLL_CLUSTER_PRIMARY_5_X_SERVER_ATTRIBUTE_ID                    = 0x0024
ZCL_ZLL_CLUSTER_PRIMARY_5_Y_SERVER_ATTRIBUTE_ID                    = 0x0025
ZCL_ZLL_CLUSTER_PRIMARY_5_INTENSITY_SERVER_ATTRIBUTE_ID            = 0x0026
ZCL_ZLL_CLUSTER_PRIMARY_6_X_SERVER_ATTRIBUTE_ID                    = 0x0028
ZCL_ZLL_CLUSTER_PRIMARY_6_Y_SERVER_ATTRIBUTE_ID                    = 0x0029
ZCL_ZLL_CLUSTER_PRIMARY_6_INTENSITY_SERVER_ATTRIBUTE_ID            = 0x002A
# Additional attributes
ZCL_ZLL_CLUSTER_ENHANCED_CURRENT_HUE_SERVER_ATTRIBUTE_ID           = 0x4000
ZCL_ZLL_CLUSTER_ENHANCED_COLOR_MODE_SERVER_ATTRIBUTE_ID            = 0x4001
ZCL_ZLL_CLUSTER_COLOR_LOOP_ACTIVE_SERVER_ATTRIBUTE_ID              = 0x4002
ZCL_ZLL_CLUSTER_COLOR_LOOP_DIRECTION_SERVER_ATTRIBUTE_ID           = 0x4003
ZCL_ZLL_CLUSTER_COLOR_LOOP_TIME_SERVER_ATTRIBUTE_ID                = 0x4004
ZCL_ZLL_CLUSTER_COLOR_LOOP_START_ENHANCED_HUE_SERVER_ATTRIBUTE_ID  = 0x4005
ZCL_ZLL_CLUSTER_COLOR_LOOP_STORED_ENHANCED_HUE_SERVER_ATTRIBUTE_ID = 0x4006
ZCL_ZLL_CLUSTER_COLOR_CAPABILITIES_SERVER_ATTRIBUTE_ID             = 0x400A
ZCL_ZLL_CLUSTER_COLOR_TEMP_PHYSICAL_MIN_SERVER_ATTRIBUTE_ID        = 0x400B
ZCL_ZLL_CLUSTER_COLOR_TEMP_PHYSICAL_MAX_SERVER_ATTRIBUTE_ID        = 0x400C

# ZLL Client Cluster commands identifiers.
MOVE_TO_HUE_COMMAND_ID                         = 0x00
MOVE_HUE_COMMAND_ID                            = 0x01
STEP_HUE_COMMAND_ID                            = 0x02
MOVE_TO_SATURATION_COMMAND_ID                  = 0x03
MOVE_SATURATION_COMMAND_ID                     = 0x04
STEP_SATURATION_COMMAND_ID                     = 0x05
MOVE_TO_HUE_AND_SATURATION_COMMAND_ID          = 0x06
MOVE_TO_COLOR_COMMAND_ID                       = 0x07
MOVE_COLOR_COMMAND_ID                          = 0x08
STEP_COLOR_COMMAND_ID                          = 0x09
MOVE_TO_COLOR_TEMPERATURE_COMMAND_ID           = 0x0A
# Additional commands
ENHANCED_MOVE_TO_HUE_COMMAND_ID                = 0x40
ENHANCED_MOVE_HUE_COMMAND_ID                   = 0x41
ENHANCED_STEP_HUE_COMMAND_ID                   = 0x42
ENHANCED_MOVE_TO_HUE_AND_SATURATION_COMMAND_ID = 0x43
COLOR_LOOP_SET_COMMAND_ID                      = 0x44
STOP_MOVE_STEP_COMMAND_ID                      = 0x47
MOVE_COLOR_TEMPERATURE_COMMAND_ID              = 0x4B
STEP_COLOR_TEMPERATURE_COMMAND_ID              = 0x4C

# MoveToHue command direction values
ZCL_ZLL_MOVE_TO_HUE_DIRECTION_SHORTEST_DISTANCE = 0x00
ZCL_ZLL_MOVE_TO_HUE_DIRECTION_LONGEST_DISTANCE  = 0x01
ZCL_ZLL_MOVE_TO_HUE_DIRECTION_UP                = 0x02
ZCL_ZLL_MOVE_TO_HUE_DIRECTION_DOWN              = 0x03

# MoveSaturation command moveMode values
ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_STOP = 0x00
ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_UP   = 0x01
ZCL_ZLL_MOVE_SATURATION_MOVE_MODE_DOWN = 0x03

# StepSaturation command stepMode values
ZCL_ZLL_STEP_SATURATION_STEP_MODE_UP   = 0x01
ZCL_ZLL_STEP_SATURATION_STEP_MODE_DOWN = 0x03

# ColorLoopSet command action values
ZCL_ZLL_COLOR_LOOP_SET_ACTION_DEACTIVATE        = 0x00
ZCL_ZLL_COLOR_LOOP_SET_ACTION_ACTIVATE          = 0x01
ZCL_ZLL_COLOR_LOOP_SET_ACTION_ACTIVATE_ENHANCED = 0x02

# ColorLoopSet command direction values
ZCL_ZLL_COLOR_LOOP_SET_DIRECTION_DECREMENT_HUE = 0x00
ZCL_ZLL_COLOR_LOOP_SET_DIRECTION_INCREMENT_HUE = 0x01

#################################################################
#                          Commands
#################################################################

# Sends move to hue command.
# param[0] - destination hue value.
# param[1] - direction.
# param[2] - transition time.
moveToHueCmd = "moveToHue %d %d %d"

# Sends move hue command.
# param[0] - move mode.
# param[1] - rate.
moveHueCmd = "moveHue %d %d"

# Sends step hue command.
# param[0] - step mode.
# param[1] - stepSize.
# param[2] - transition time.
stepHueCmd = "stepHue %d %d %d"

# Sends move to saturation command.
# param[0] - destination saturation value.
# param[1] - transition time.
moveToSaturationCmd = "moveToSaturation %d %d"

# Sends move saturation command.
# param[0] - move mode.
# param[1] - rate.
moveSaturationCmd = "moveSaturation %d %d"

# Sends step saturation command.
# param[0] - step mode.
# param[1] - stepSize.
# param[2] - transition time.
stepSaturationCmd = "stepSaturation %d %d %d"

# Sends move to hue and saturation command.
# param[0] - destination hue value.
# param[1] - destination saturation value.
# param[2] - transition time.
moveToHueAndSaturationCmd = "moveToHueAndSaturation %d %d %d"

# Sends move to color command.
# param[0] - destination colorX value.
# param[1] - destination colorY value.
# param[2] - transition time.
moveToColorCmd = "moveToColor %d %d %d"

# Sends move color command.
# param[0] - rateX value.
# param[1] - rateY value.
moveColorCmd = "moveColor %d %d"

# Sends step color command.
# param[0] - stepX size.
# param[1] - stepY size.
# param[2] - transition time.
stepColorCmd = "stepColor %d %d %d"

# Sends enhanced move to hue command.
# param[0] - destination hue value.
# param[1] - direction.
# param[2] - transition time.
enhancedMoveToHueCmd = "enhancedMoveToHue %d %d %d"

# Sends enhanced move hue command.
# param[0] - move mode.
# param[1] - rate.
enhancedMoveHueCmd = "enhancedMoveHue %d %d"

# Sends enhanced step hue command.
# param[0] - step mode.
# param[1] - stepSize.
# param[2] - transition time.
enhancedStepHueCmd = "enhancedStepHue %d %d %d"

# Sends enhanced move to hue and saturation command.
# param[0] - destination hue value.
# param[1] - destination saturation value.
# param[2] - transition time.
enhancedMoveToHueAndSaturationCmd = "enhancedMoveToHueAndSaturation %d %d %d"

# Sends color loop set command.
# param[0] - update flags.
# param[1] - action.
# param[2] - direction.
# param[3] - time.
# param[4] - start hue.
colorLoopSetCmd = "colorLoopSet %d %d %d %d %d"

# Sends stop move step command.
stopMoveStepHueCmd = "stopMoveStepHue"

# Sends move to color temperature command.
# param[0] - destination color temperature value.
# param[1] - transition time.
moveToColorTemperatureCmd = "moveToColorTemperature %d %d"

# Sends move color temperature command.
# param[0] - move mode.
# param[1] - rate.
# param[2] - color temperature minimum.
# param[3] - color temperature maximum.
moveColorTemperatureCmd = "moveColorTemperature %d %d %d %d"

# Sends step color temperature command.
# param[0] - step mode.
# param[1] - step size.
# param[2] - transition time.
# param[3] - color temperature minimum.
# param[4] - color temperature maximum.
stepColorTemperatureCmd = "stepColorTemperature %d %d %d %d %d"

# Sends read color control attribute command.
# param[0] - attribute to be read.
readColorControlClusterAttrCmd = "readColorControlAttr %d"

# Write color control cluster attribute on remote device
# param[0] - attribute id.
# param[1] - attribute type.
# param[2] - value to write.
writeColorControlClusterAttrCmd = "writeColorControlAttr %d %d %d"

#################################################################
#                         Responses
#################################################################

# Indicates reception of move to hue command.
moveToHueIndStr = "moveToHueInd()"

# Indicates reception of move hue command.
moveHueIndStr = "moveHueInd()"

# Indicates reception of step hue command.
stepHueIndStr = "stepHueInd()"

# Indicates reception of  move to saturation command.
moveToSaturationIndStr = "moveToSaturationInd()"

# Indicates reception of  move saturation command.
moveSaturationIndStr = "moveSaturationInd()"

# Indicates reception of step saturation command.
stepSaturationIndStr = "stepSaturationInd()"

# Indicates reception of move to hue and saturation command.
moveToHueAndSaturationIndStr = "moveToHueAndSaturationInd()"

# Indicates reception of move to color command.
moveToColorIndStr = "moveToColorInd()"

# Indicates reception of move color command.
moveColorIndStr = "moveColorInd()"

# Indicates reception of step color command.
stepColorIndStr = "stepColorInd()"

# Indicates reception of enhanced move to hue command.
enhancedMoveToHueIndStr = "enhancedMoveToHueInd()"

# Indicates reception of enhanced move hue command.
enhancedMoveHueIndStr = "enhancedMoveHueInd()"

# Indicates reception of enhanced step hue command.
enhancedStepHueIndStr = "enhancedStepHueInd()"

# Indicates reception of enhanced move to hue and saturation command.
enhancedMoveToHueAndSaturationIndStr = "enhancedMoveToHueAndSaturationInd()"

# Indicates reception of color loop set command.
colorLoopSetIndStr = "colorLoopSetInd()"

# Indicates reception of stop move step command.
stopMoveStepIndStr = "stopMoveStepInd()"

# Indicates reception of move to color temperature command.
moveToColorTemperatureIndStr = "moveToColorTemperatureInd()"

# Indicates reception of move color temperature command.
moveColorTemperatureIndStr = "moveColorTemperatureInd()"

# Indicates reception of step color temperature command.
stepColorTemperatureIndStr = "stepColorTemperatureInd()"

# Indicates reception of read attribute response
readColorControlClusterAttrRespStr = "Attr 0x%04x = "

#################################################################
#                         Functions
#################################################################
def sendMoveToHueCommand(port, hue, direction, time):
  sendCommand(port, moveToHueCmd % (hue, direction, time))
  idle([port], timeout = 100)

def sendMoveHueCommand(port, mode, rate):
  sendCommand(port, moveHueCmd % (mode, rate))
  idle([port], timeout = 100)

def sendStepHueCommand(port, mode, size, time):
  sendCommand(port, stepHueCmd % (mode, size, time))
  idle([port], timeout = 100)

def sendMoveToSaturationCommand(port, saturation, time):
  sendCommand(port, moveToSaturationCmd % (saturation, time))
  idle([port], timeout = 100)

def sendMoveSaturationCommand(port, mode, rate):
  sendCommand(port, moveSaturationCmd % (mode, rate))
  idle([port], timeout = 100)

def sendStepSaturationCommand(port, mode, size, time):
  sendCommand(port, stepSaturationCmd % (mode, size, time))
  idle([port], timeout = 100)

def sendMoveToHueAndSaturationCommand(port, hue, saturation, time):
  sendCommand(port, moveToHueAndSaturationCmd % (hue, saturation, time))
  idle([port], timeout = 100)

def sendMoveToColorCommand(port, colorX, colorY, time):
  sendCommand(port, moveToColorCmd % (colorX, colorY, time))
  idle([port], timeout = 100)

def sendMoveColorCommand(port, rateX, rateY):
  sendCommand(port, moveColorCmd % (rateX, rateY))
  idle([port], timeout = 100)
  
def sendStepColorCommand(port, stepX, stepY, time):
  sendCommand(port, stepColorCmd % (stepX, stepY, time))
  idle([port], timeout = 100)
  
def sendEnhancedMoveToHueCommand(port, hue, direction, time):
  sendCommand(port, enhancedMoveToHueCmd % (hue, direction, time))
  idle([port], timeout = 100)

def sendEnhancedMoveHueCommand(port, mode, rate):
  sendCommand(port, enhancedMoveHueCmd % (mode, rate))
  idle([port], timeout = 100)

def sendEnhancedStepHueCommand(port, mode, size, time):
  sendCommand(port, enhancedStepHueCmd % (mode, size, time))
  idle([port], timeout = 100)

def sendEnhancedMoveToHueAndSaturationCommand(port, hue, saturation, time):
  sendCommand(port, enhancedMoveToHueAndSaturationCmd % (hue, saturation, time))
  idle([port], timeout = 100)

def sendColorLoopSetCmdCommand(port, flags, action = 0, direction = 0, time = 0, startHue = 0):
  sendCommand(port, colorLoopSetCmd % (flags, action, direction, time, startHue))
  idle([port], timeout = 100)

def sendStopMoveStepHueCommand(port):
  sendCommand(port, stopMoveStepHueCmd)
  idle([port], timeout = 100)

def sendMoveToColorTemperatureCommand(port, colorTemp, time):
  sendCommand(port, moveToColorTemperatureCmd % (colorTemp, time))
  idle([port], timeout = 100)

def sendMoveColorTemperatureCommand(port, mode, rate, colorTempMin, colorTempMax):
  sendCommand(port, moveColorTemperatureCmd % (mode, rate, colorTempMin, colorTempMax))
  idle([port], timeout = 100)

def sendStepColorTemperatureCommand(port, mode, size, time, colorTempMin, colorTempMax):
  sendCommand(port, stepColorTemperatureCmd % (mode, size, time, colorTempMin, colorTempMax))
  idle([port], timeout = 100)

def readColorControlClusterAttribute(port, attr, retStatus = 0):
  sendCommand(port, readColorControlClusterAttrCmd % attr)
  writeLog("Client receives response from server")
  receiveAndCheck(port, zclRespReceivedIndStr % retStatus)
  
  if retStatus == 0:
    buffer = receiveNextStr(port)
    print '<-' + buffer
    expectedString = readColorControlClusterAttrRespStr % attr
    check(buffer[:len(expectedString)] == expectedString)
    attrValue = buffer[len(expectedString):]
    try:
      attrValue = int(attrValue)
    except ValueError:
      attrValue = attrValue.strip()
    idle([port], timeout = 150)
    return attrValue
  
  return None

def writeColorControlClusterAttribute(port, attr, type, value, retStatus = 0):
  sendCommand(port, writeColorControlClusterAttrCmd % (attr, type, value))
  writeLog("Client receives response from server")
  receiveAndCheck(port, zclRespReceivedIndStr % retStatus)
  idle([port], timeout = 150)
  