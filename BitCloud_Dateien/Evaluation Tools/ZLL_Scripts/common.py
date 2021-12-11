from public import *
import env

#################################################################
#                     Common parameters
#################################################################

maxCommandLength = 0xFF
commandSeparator = '\r\n'

vendorDefinedIdentifyDuration = 0xFFFF

scanRequestsAmountOnFirstChannel = 5
scanRequestsAmountNotOnFirstChannel = 1
touchlinkRssiThreshold = -60
buttonlinkRssiThreshold = -85

mainTestChannel = 0x12

PORT_DEFAULT_TIMEOUT = 60000

HIGHEST_CHANNEL = 26
LOWEST_CHANNEL = 11

# Device types
APP_DEVICE_TYPE_COLOR_SCENE_REMOTE      = 1
APP_DEVICE_TYPE_BRIDGE                  = 2
APP_DEVICE_TYPE_ON_OFF_LIGHT            = 3
APP_DEVICE_TYPE_DIMMABLE_LIGHT          = 4
APP_DEVICE_TYPE_COLOR_LIGHT             = 5
APP_DEVICE_TYPE_EXTENDED_COLOR_LIGHT    = 6
APP_DEVICE_TYPE_TEMPERATURE_COLOR_LIGHT = 7

# APS addressing modes
APS_NO_ADDRESS    = 0x00
APS_GROUP_ADDRESS = 0x01
APS_SHORT_ADDRESS = 0x02
APS_EXT_ADDRESS   = 0x03

# General status
BC_SUCCESS_STATUS      = 0x00
BC_FAILURE_STATUS      = 0x01
BC_DISCONNECTED_STATUS = 0x02
BC_DISCONNECTED_RECONNECTED_SUCCESS_STATUS = 0x03
BC_CONNECTED_STATUS    = 0x04

# Touchlink procdure status
TOUCHLINK_SUCCESS_STATUS               = 0x00
TOUCHLINK_COMMISSIONING_SKIPPED_STATUS = 0x01
TOUCHLINK_FAILED_STATUS                = 0x02

#APS status values
APS_NO_ACK_STATUS           = 0xA7
APS_NO_SHORT_ADDRESS_STATUS = 0xA9

#ZDO status values
ZDO_FAIL_STATUS             = 0x07

# ZCL status values
ZCL_SUCCESS_STATUS                      = 0x00
ZCL_UNSUP_MANUF_CLUSTER_COMMAND         = 0x83
ZCL_UNSUP_MANUF_GENERAL_COMMAND_STATUS  = 0x84
ZCL_UNSUPPORTED_ATTRIBUTE_STATUS        = 0x86
ZCL_INVALID_VALUE_STATUS                = 0x87
ZCL_READ_ONLY_STATUS                    = 0x88
ZCL_NOT_FOUND_STATUS                    = 0x8b
ZCL_NO_RESPONSE_ERROR_STATUS            = 0xC3

# Endpoint Ids
APP_ENDPOINT_COLOR_SCENE_REMOTE = 0x01
APP_ENDPOINT_LIGHT              = 0x0A
APP_ENDPOINT_BRIDGE             = 0x0B

# ZCL data types
ZCL_U8BIT_DATA_TYPE_ID  = 0x20
ZCL_U16BIT_DATA_TYPE_ID = 0x21

# Default response control
ENABLE_DEFAULT_RESPONSE = 0x00
DISABLE_DEFAULT_RESPONSE = 0x01

# General clusters defined by ZCL Specification
IDENTIFY_CLUSTER_ID = 0x0003

#################################################################
#                          Commands
#################################################################

# Resets device
resetCmd            = "reset"

# Resets device to factory defaults
resetToFnCmd        = "resetToFN"

# Returns device extended address
getExtAddressCmd    = "devInfoGetExtAddr"

# Is used to set the link quality between two nodes with special value different from 
# real radio link quality
# 1 - most significiant 4 bytes of extended address
# 2 - least significiant 4 bytes of extended address
# 3 - rssi value which will be set for every packet received from device with 
#     specified extended address
macBanNodeCmd       = "macBanNode %d %d %d"

# Resets mac ban table (is used to cancel previous changes)
macResetBanTableCmd = "macResetBanTable"

# Sets Association Permitted flag for specified time
# 1 - time to allow Association
setPermitJoinReqCmd    = "setPermitJoin %d"

setPermitJoinRespCmd = "setPermitJoinRsp %d"

# Permit join duration
PERMIT_JOIN_DURATION_INFINITE = 0xFF
PERMIT_JOIN_DURATION_ZERO     = 0x00

# Target types definitions
TARGET_TYPE_NONE        = 0x00
TARGET_TYPE_BUTTON_LINK = 0x01
TARGET_TYPE_TOUCHLINK   = 0x02
TARGET_TYPE_HYBRID      = TARGET_TYPE_BUTTON_LINK | TARGET_TYPE_TOUCHLINK

# Sets target type
# param[0] - target type;
setTargetTypeCmd = "setTargetType %d"

# Scan types definitions
INITIATOR_SCAN_TYPE_BUTTONLINK                 = 0x01
INITIATOR_SCAN_TYPE_TOUCHLINK                  = 0x02
INITIATOR_SCAN_TYPE_HYBRID                     = (INITIATOR_SCAN_TYPE_BUTTONLINK | INITIATOR_SCAN_TYPE_TOUCHLINK)
INITIATOR_SCAN_TYPE_OWN_PAN_ONLY               = 0x04
INITIATOR_SCAN_TYPE_INCLUDE_SECONDARY_CHANNELS = 0x08

# Perform interPan scanning for existing devices.
# param[0] - scan type.
performScanCmd = "performScan %d"

# Perform touchlink procedure.
touchlickCmd     = "touchlink"

# Perform reset device to FN procedure.
resetDeviceToFnCmd = "resetDeviceToFN"

# Perform identify procedure.
# param[0] - identify period as amount of 100 ms intervals.
identifyDeviceCmd = "identifyDevice %d"

# Enters to the network with specified parameters.
# param[0] - most significiant 4 bytes of extended panId.
# param[1] - least significiant 4 bytes of extended panId.
# param[2] - channel.
# param[3] - panId.
# param[4] - network address.
# param[5] - network update id.
joinNetworkCmd = "joinNetwork %d %d %d %d %d %d"

# Sends nwkMgmtUpdateReq to specified recipient
# param[0] - channel.
# param[1] - scanDuration.
# param[2] - destNwkAddr.
nwkMgmtUpdateReqCmd = "sendNwkMgmtUpdateReq %d %d %d"

# Requests if device is factory new or not
isDeviceFnCmd = "isDeviceFn"

# Requests if device is end device
isEndDeviceCmd = "isEndDevice"

# Requests if a type of device
getDeviceTypeCmd = "getDeviceType"

# Switch off receiver
switchOffRxCmd = "switchOffRx"

# Switch on receiver
switchOnRxCmd = "switchOnRx"

# Set destination addressing parameters
# param[0] - mode.
# param[1] - address value.
# param[2] - endpoint.
# param[3] - manufacturer specific code. If it is set of 0xFFFF then the commands 
#            will be issued with manufacturer specific bit in the ZCL header set to 1
#            and the manufacturer code field in the ZCL header set to 0x0000
# param[4] - default response control. 0 - enable, 1 - disable.
setAddressingCmd = "setAddressing %d %d %d %d %d"

# Returns device network address
getNwkAddressCmd = "getNetworkAddress"

# Enable/disable NWK security
# param[0] - if 0 - disables NWK security, enables otherwise.
setNwkSecurityCmd = "setNwkSecurity %d"

# Restarts remote's activity
restartActivityCmd = "restartActivity"

# Returns current channel
getChannelCmd = "getChannel"

# Returns current channel mask
getChannelMaskCmd = "getChannelMask"

# Powers off device
powerOffCmd = "powerOff"

# Initiates network discovery and association
nwkAssociationCmd = "nwkAssociation"

# Performs write attributes undivided command for two attributes
# param[0] - cluster id.
# param[1] - attribute #1 id.
# param[2] - attribute #1 type.
# param[3] - attribute #1 value to write.
# param[4] - attribute #2 id.
# param[5] - attribute #2 type.
# param[6] - attribute #2 value to write.
writeAttrUndividedCmd = "writeAttrUndivided %d %d %d %d %d %d %d"

# Performs write attributes no response command
# param[0] - cluster id.
# param[1] - attribute id.
# param[2] - attribute type.
# param[3] - attribute value to write.
writeAttrNoResponseCmd = "writeAttrNoResp %d %d %d %d"

# Forces HA device to restart network on specified channel
# param[0] - channel to restart network
haRestartNwkCmd = "restartNwk %d"

# Sets primary channel mask for a device
setPrimaryChannelMaskCmd = "setPrimaryChannelMask %d"

# Sets secondary channel mask for a device
setSecondaryChannelMaskCmd = "setSecondaryChannelMask %d"

#################################################################
#                         Responses
#################################################################

# Common response which is indicated successful procedure 
doneStr = "Done"

# Indicates that device has entered to the network with specified parameters
joinNetworkDoneStr = 'Join to the network is done - %d'

# Indicates that device has been connected to the network 
connectedStr = "Connected"
# Indicates that device has been disconnected to the network 
disconnectedStr = "Disconnected"

# Indicates that device has joined to the network 
joinDoneStr   = "Joining succeded"
# Indicates that device has failed to join to the network 
joinFailedStr = "Joining failed"

# Indicates that device has completed discovery network procedure and found 
# one or more networks
discoveryDoneStr   = "Discovery done"
# Indicates that device has completed discovery network procedure and didn't
# find any network
discoveryFailedStr = "Discovery failed"

# Indicates that device has associated to the network 
associationDoneStr   = "Association succeded"
# Indicates that device has failed to associate to the network 
associationFailedStr = "Association failed"

# Indicates that NWK addres has been allocated during the association
allocNwkAddrStr = "Got NWK address 0x%04x"

# Indicates that network has been changed
nwkUpdateStatusStr = "Network update status - 0x%02x"
# Network update statuses
ZDO_CHILD_JOINED_STATUS = 0x92

# Is issued on interPan scan response reception
scanRespIndStr     = "Scan Response received"

# Is issued on interPan device info response reception
devInfoRespIndStr  = "Device Info response received"
# Is issued on interPan device info request reception
devInfoReqIndStr  = "Device Info request received"

# Is issued on interPan network start response reception
startNwkRespIndStr = "Network Start response received"
# Is issued on interPan network start request reception
startNwkReqIndStr = "Network Start request received"

# Is issued on interPan network join router response reception
networkJoinRouterRespStr = 'Network Join Router response received'
# Is issued on interPan network join router request reception
networkJoinRouterReqStr = 'Network Join Router request received'

# Is issued on interPan network join endDevice response reception
networkJoinEndDeviceRespStr = 'Network Join End Device response received'
# Is issued on interPan network join endDevice request reception
networkJoinEndDeviceReqStr = 'Network Join End Device request received'

# Indicates that interPan scanning for devices has been finished and consist of three
# string sparated by "\n\r".
# Second string contains the amount of found devices
scanDoneStr        = "Scan is Done"
statusStr          = "Status is %d" 
deviceAmountStr    = "Device amount is %d"

# Is issued on interPan identify request reception
identifyReqIndStr = "Identify request received"

# Indicates that ZDP coomand has been received
zdpCommandReceivedStr = "ZDP command received"

# Response to the device FN flag request mutable part is ommited
deviceFnStatusStr = "DeviceIsFN = "

# Response to the device type request mutable part is ommited
isEndDeviceStr = "IsEndDevice = "

# Response to the device type request mutable part is ommited
deviceTypeStr = "DeviceType = "

# Indicates that a zcl response has been received
zclRespReceivedIndStr = "ZclResponse: status = 0x%02x"

# Indicates that a zcl dafault response has been received
zclDefRespReceivedIndStr = "ZclDefaultResponse: status = 0x%02x"

# Indicates that a zcl confirm has been received
zclConfirmStr = "ZclConfirm: status = 0x%02x"

# Response on restarting network by HA device
haNwkCommunicationEstablishedStr = "Network communication established"

#################################################################
#                         Functions
#################################################################

def bytesListToStr(list):
  return ''.join([chr(byte) for byte in list])

def receiveNextStr(port):
  buffer = bytesListToStr(port.receiveBuffer(len(commandSeparator)))
  while buffer == commandSeparator:
    buffer = bytesListToStr(port.receiveBuffer(len(commandSeparator)))
  while buffer[-len(commandSeparator):] != commandSeparator:
    buffer += bytesListToStr(port.receiveBuffer(1))
    check(len(buffer) < maxCommandLength)
    
  return buffer[:-len(commandSeparator)]

def clearPorts(ports):
  print 'Clearing ports'
  for port in ports:
    port.setTimeout(50)
    port.receiveBuffer()
    port.setTimeout(60000)
  
def preparePorts(ports):
  for port in ports:
    port.setTesterMode(0)
  clearPorts(ports)
  
def receiveAndCheck(port, string):
  buffer = receiveNextStr(port)
  if buffer:
    print '<-' + buffer
  else:
    writeLog('Connection timeout.\r\n Receive: None\r\n  Expect:"%s"' % string.strip())
  try:
    check(buffer[:len(string)] == string)
  except exc.TestFailed:
    if buffer is None:
      buffer = ''
    writeLog('Check failed.\r\n Receive:"%s"\r\n  Expect:"%s"' % (buffer.strip(), string.strip()))
    raise

def sendCommand(port, cmdStr):
  print '->' + cmdStr
  buffer = strToList(cmdStr + commandSeparator)
  port.sendBuffer(buffer)

def setTargetType(port, type):
  sendCommand(port, setTargetTypeCmd % type)
  receiveAndCheck(port, doneStr)

def haResetToFN(ports, nwkJoinStatus):
  for port in ports:
    sendCommand(port, resetToFnCmd)
    if nwkJoinStatus == BC_SUCCESS_STATUS:
      sleep(5)
      receiveAndCheck(port, haNwkCommunicationEstablishedStr)
      setPermitJoinReq(port, PERMIT_JOIN_DURATION_ZERO)
      receiveSetPermitJoinResp(port, BC_SUCCESS_STATUS)

def resetRouterToFN(ports):
  environment = env.getVariables()
  for port in ports:
    sendCommand(port, resetToFnCmd)
    receiveAndCheck(port, discoveryFailedStr)
    setPrimaryChannelMask([port], eval(environment["zllPrimaryChannelMask"]))
    setSecondaryChannelMask([port], eval(environment["zllSecondaryChannelMask"]))
    setTargetType(port, TARGET_TYPE_NONE)

def resetEndDeviceToFN(ports):
  environment = env.getVariables()
  for port in ports:
    sendCommand(port, resetToFnCmd)
  sleep(5)
  setPrimaryChannelMask([port], eval(environment["zllPrimaryChannelMask"]))
  setSecondaryChannelMask([port], eval(environment["zllSecondaryChannelMask"]))

def resetRouter(ports):
  for port in ports:
    factoryNew = isDeviceFN(port)
    sendCommand(port, resetCmd)
    if factoryNew:
      receiveAndCheck(port, discoveryFailedStr)
    else:
      sleep(6)

def resetEndDevice(ports):
  for port in ports:
    sendCommand(port, resetCmd)
  sleep(6)
  
def isPortEmpty(port):
  buffer = port.receiveBuffer()
  if buffer:
    print 'Unexpected input: %s' % bytesListToStr(buffer)
  return buffer == None;
    
def idle(ports, timeout = 5000):
  print 'Idle for %d ms' % timeout
  port = ports[0]
  port.setTimeout(timeout)
  check(isPortEmpty(port))
  port.setTimeout(60000)
  
  for port in ports[1:]:
    port.setTimeout(1)
    check(isPortEmpty(port))
    port.setTimeout(60000)
  
def getExtAddr(port):
  sendCommand(port, getExtAddressCmd)
  buffer = receiveNextStr(port)
  buffer = [buffer[i:i+2] for i in range(0, len(buffer), 2)]
  buffer.reverse()
  buffer = ''.join(buffer)
  return int(buffer, 16)
  
def setRssiForExtAddress(ports, extAddr, rssi):
  for port in ports:
    sendCommand(port, macBanNodeCmd % ((extAddr >> 32) & 0xFFFFFFFF, extAddr & 0xFFFFFFFF, rssi))
    receiveAndCheck(port, doneStr)
  
def resetBanTable(ports):
  for port in ports:
    sendCommand(port, macResetBanTableCmd)
    receiveAndCheck(port, doneStr)

def joinNetwork(port, extPanId, channel, panId, nwkAddr, nwkUpdateId):
  msPart = (extPanId >> 32) & 0xFFFFFFFF
  lsPart = extPanId & 0xFFFFFFFF
  sendCommand(port, joinNetworkCmd % (extPanId, lsPart, channel, panId, nwkAddr, nwkUpdateId))
  receiveAndCheck(port, joinDoneStr)
  receiveAndCheck(port, connectedStr)
  receiveAndCheck(port, joinNetworkDoneStr % 0)

def sendNwkMgmtUpdateReq(port, channel, scanDuration, destNwkAddr):
  sendCommand(port, nwkMgmtUpdateReqCmd % (channel, scanDuration, destNwkAddr))
  receiveAndCheck(port, doneStr)

def isDeviceFN(port):
  sendCommand(port, isDeviceFnCmd)
  buffer = receiveNextStr(port)
  buffer = buffer[len(deviceFnStatusStr):]
  return int(buffer.strip().split()[0])

def getDeviceType(port):
  sendCommand(port, getDeviceTypeCmd)
  buffer = receiveNextStr(port)
  buffer = buffer[len(deviceTypeStr):]
  return int(buffer.strip().split()[0])

def isEndDeviceType(port):
  sendCommand(port, isEndDeviceCmd)
  buffer = receiveNextStr(port)
  buffer = buffer[len(isEndDeviceStr):]
  return int(buffer.strip().split()[0])
  
def touchlink(initiator, target, touchlinkStatus = TOUCHLINK_SUCCESS_STATUS):
  sleep(1)
  if TOUCHLINK_SUCCESS_STATUS == touchlinkStatus or TOUCHLINK_COMMISSIONING_SKIPPED_STATUS == touchlinkStatus:
    resetBanTable([target])
    setRssiForExtAddress([target], getExtAddr(initiator), touchlinkRssiThreshold + 10)

  isInitiatorFN = isDeviceFN(initiator)
  isTargetFN = isDeviceFN(target)

  initiatorIsEndDevice = isEndDeviceType(initiator)
  targetIsEndDevice = isEndDeviceType(target)

  writeLog("Initiator: isFN = %d; isEndDevice = %d" % (isInitiatorFN, isTargetFN))
  writeLog("Target: isFN = %d; isEndDevice = %d" % (isTargetFN, targetIsEndDevice))

  writeLog("Target enables its receiver")
  setTargetType(target, TARGET_TYPE_TOUCHLINK)
  writeLog("Start touchlink")
  sendCommand(initiator, touchlickCmd)

  if touchlinkStatus == TOUCHLINK_FAILED_STATUS:
    return

  writeLog("Scan response indication on Initiator")
  receiveAndCheck(initiator, scanRespIndStr)
  writeLog("Identify request indication on Target")
  receiveAndCheck(target, identifyReqIndStr)
  
  if touchlinkStatus == TOUCHLINK_SUCCESS_STATUS:
    if targetIsEndDevice:
      writeLog("Network Join EndDevice request indication on Target")
      receiveAndCheck(target, networkJoinEndDeviceReqStr)
    else:
      if isInitiatorFN:
        writeLog("Network Start request indication on Target")
        receiveAndCheck(target, startNwkReqIndStr)
      else:
        writeLog("Network Join Router request indication on Target")
        receiveAndCheck(target, networkJoinRouterReqStr)
          
    writeLog("Join indication on Target")
    receiveAndCheck(target, joinDoneStr)
    
    if not targetIsEndDevice:
      writeLog("Connected indication on Target")
      receiveAndCheck(target, connectedStr)
  
    if targetIsEndDevice:
      writeLog("Network join EndDevice response indication on Initiator")
      receiveAndCheck(initiator, networkJoinEndDeviceRespStr)
    else:
      if isInitiatorFN:
        writeLog("Network start response indication on Initiator")
        receiveAndCheck(initiator, startNwkRespIndStr)
      else:
        writeLog("Network join router response indication on Target")
        receiveAndCheck(initiator, networkJoinRouterRespStr)
        
    if isInitiatorFN:
      writeLog("Join indication on Initiator")
      receiveAndCheck(initiator, joinDoneStr)
    
      if not targetIsEndDevice:
        writeLog("Connected indication on Initiator")
        receiveAndCheck(initiator, connectedStr)

def switchOffRx(ports):
  for port in ports:
    sendCommand(port, switchOffRxCmd)
    receiveAndCheck(port, doneStr)

def switchOnRx(ports):
  for port in ports:
    sendCommand(port, switchOnRxCmd)
    receiveAndCheck(port, doneStr)
    
def getNwkAddress(port):
  sendCommand(port, getNwkAddressCmd)
  buffer = receiveNextStr(port)
  return int(buffer, 16)

def apsBindReq(port, destExtAddr, srcEp, dstEp, clusterId):
  msPart = (destExtAddr >> 32) & 0xFFFFFFFF
  lsPart = destExtAddr & 0xFFFFFFFF
  sendCommand(port, "apsBindReq %d %d %d %d %d" % (msPart, lsPart, srcEp, dstEp, clusterId))
  receiveAndCheck(port, doneStr)

def setAddressing(port, addrMode, dstAddr, dstEp, manSpecCode = 0, defaultResp = DISABLE_DEFAULT_RESPONSE):
  sendCommand(port, setAddressingCmd % (addrMode, dstAddr, dstEp, manSpecCode, defaultResp))
  sleep(1)

def getChannel(port):
  sendCommand(port, getChannelCmd)
  buffer = receiveNextStr(port)
  return int(buffer)
  
def getChannelMask(port):
  sendCommand(port, getChannelMaskCmd)
  buffer = receiveNextStr(port)
  return int(buffer, 16)

def getNextChannel(channelMask, currentChannel):
  nextChannel = currentChannel + 1
  
  while nextChannel <= HIGHEST_CHANNEL:
    if (1 << nextChannel) & channelMask:
      return nextChannel
    else:
      nextChannel = nextChannel + 1
      
  nextChannel = LOWEST_CHANNEL
  while nextChannel < currentChannel:
    if (1 << nextChannel) & channelMask:
      return nextChannel
    else:
      nextChannel = nextChannel + 1

  return 0
  
def getFirstChannel(channelMask):
  channel = LOWEST_CHANNEL
  
  while channel <= HIGHEST_CHANNEL:
    if (1 << channel) & channelMask:
      return channel
    else:
      channel = channel + 1
  return 0

def powerOff(ports):
  for port in ports:
    sendCommand(port, powerOffCmd)

def powerOn(ports):
  for port in ports:
    isEndDevice = isEndDeviceType(port)
    factoryNew = isDeviceFN(port)
    sendCommand(port, resetCmd)
    if not isEndDevice and factoryNew:
      receiveAndCheck(port, discoveryFailedStr)
    else:
      sleep(10)
    setTargetType(port, TARGET_TYPE_NONE)

def setPermitJoinReq(port, permitDuration):
  sendCommand(port, setPermitJoinReqCmd % permitDuration)

def receiveSetPermitJoinResp(port, status):
  receiveAndCheck(port, setPermitJoinRespCmd % status)

def nwkAssociation(port, discoveryStatus, associationStatus):
  sendCommand(port, nwkAssociationCmd)
  if BC_SUCCESS_STATUS == discoveryStatus:
    receiveAndCheck(port, discoveryDoneStr)
  else:
    receiveAndCheck(port, discoveryFailedStr)
    return None

  if BC_SUCCESS_STATUS == associationStatus:
    nwkAddr = None
    receiveAndCheck(port, associationDoneStr)
    buffer = receiveNextStr(port)
    receiveAndCheck(port, joinDoneStr)
    receiveAndCheck(port, connectedStr)
    return buffer.strip().split()[3]
  else:
    receiveAndCheck(port, associationFailedStr)
    return None

def haRestartNwk(port, channel, status):
  sendCommand(port, haRestartNwkCmd % channel)
  if BC_SUCCESS_STATUS == status:
    receiveAndCheck(port, haNwkCommunicationEstablishedStr)
    sleep(3)
    setPermitJoinReq(port, PERMIT_JOIN_DURATION_ZERO)
    receiveSetPermitJoinResp(port, BC_SUCCESS_STATUS)

def setPrimaryChannelMask(portList, channelMask):
  for port in portList:
    sendCommand(port, setPrimaryChannelMaskCmd % channelMask)
  sleep(1)

def setSecondaryChannelMask(portList, channelMask):
  for port in portList:
    sendCommand(port, setSecondaryChannelMaskCmd % channelMask)
  sleep(1)

def writeAttributesUndivided(port, clusterId, attr1, type1, value1, attr2, type2, value2, retStatus = 0):
  sendCommand(port, writeAttrUndividedCmd % (clusterId, attr1, type1, value1, attr2, type2, value2))
  writeLog("Client receives response from server")
  receiveAndCheck(port, zclRespReceivedIndStr % retStatus)
  idle([port], timeout = 150)

def writeAttributesNoResponse(port, clusterId, attr, type, value, retStatus = 0):
  sendCommand(port, writeAttrNoResponseCmd % (clusterId, attr, type, value))
  idle([port], timeout = 150)