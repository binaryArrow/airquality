"""
@testcase
@description TP-LLI-TC-06: Frequency agility: Non factory new remote, non factory new lamp

@tags
  INTEROPERABILITY
  CHAPTER_5
  TOUCHLINK
  POSITIVE

"""

#*****************************************************************************************
#Defines section
#*****************************************************************************************
import sys
sys.path.append(scriptPath)
from common import *
from deviceScanner import *
from onOffCluster import *
sys.path.remove(scriptPath)

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []

configureCommunication()

v1rc1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
v1l1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
v2l1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
#Script body - feature checking
#*****************************************************************************************
writeLog("P1: Power on V1RC1 and V1L1. Resetting nodes to FN")
resetRouterToFN([v1l1, v2l1])
resetEndDeviceToFN([v1rc1])
clearPorts([v1rc1, v1l1, v2l1])

writeLog("Resetting mac ban table")
resetBanTable([v1rc1, v1l1, v2l1])

v1rc1ExtAddr = getExtAddr(v1rc1)
v1rc1NwkAddr = getNwkAddress(v1rc1)
writeLog("v1rc1 extended address - %016X" % v1rc1ExtAddr)

v1l1ExtAddr = getExtAddr(v1l1)
v1l1NwkAddr = getNwkAddress(v1l1)
writeLog("v1l1 extended address - %016X" % v1l1ExtAddr)

v2l1ExtAddr = getExtAddr(v2l1)
v2l1NwkAddr = getNwkAddress(v2l1)
writeLog("v1l1 extended address - %016X" % v2l1ExtAddr)

writeLog("P2: With V1RC1 held close to V2L1, user initiates a touchlink command on V1RC1. Touchlink should succeed.")
touchlink(v1rc1, v2l1)
idle([v1rc1, v2l1])

writeLog("P3: User initiates a turn on command on V1RC1.")
setAddressing(v1rc1, APS_SHORT_ADDRESS, getNwkAddress(v2l1), APP_ENDPOINT_LIGHT)
sendOnCommand(v1rc1)
receiveOnCommand(v2l1)

writeLog("P4: User initiates a turn on command on V1RC1.")
sendOffCommand(v1rc1)
receiveOffCommand(v2l1)

writeLog("P5: Where support is indicated in the PICS, user initiates a toggle command on V1RC1.")
sendToggleCommand(v1rc1)
receiveToggleCommand(v2l1)


writeLog("Item 1a: User initiates a frequency agility command on V1RC1 with V1RC1 in range of V2L1. V2L1 executes its channel change procedure.")
currentChannel = getChannel(v1rc1)
channelMask = getChannelMask(v1rc1)
targetChannel = getNextChannel(channelMask, currentChannel)
writeLog("Current channel: %d; channelMask: %08x" % (currentChannel, channelMask))
writeLog("Target channel: %d" % targetChannel)
check(targetChannel != 0) # Channel mask shall contain more than one channel to pass this test

sendNwkMgmtUpdateReq(v1rc1, targetChannel, 0xFE, 0xFFFD)
writeLog("Item 1b: V1RC1 rejoins the network.")
receiveAndCheck(v1rc1, disconnectedStr)
writeLog("Connected indication on ED1")
receiveAndCheck(v1rc1, connectedStr)
idle([v1rc1, v2l1])

writeLog("Item 2a: User initiates a turn on command on V1RC1.")
setAddressing(v1rc1, APS_SHORT_ADDRESS, getNwkAddress(v2l1), APP_ENDPOINT_LIGHT)
sendOnCommand(v1rc1)
receiveOnCommand(v2l1)

writeLog("Item 2b: User initiates a turn off command on V1RC1.")
sendOffCommand(v1rc1)
receiveOffCommand(v2l1)

writeLog("Item 2c: Where support is indicated in the PICS, user initiates a toggle command on V1RC1.")
sendToggleCommand(v1rc1)
receiveToggleCommand(v2l1)

writeLog("Item 3a: Optional: Power off V2L1. Power on V1L1. ")
sleep(2)
powerOff([v2l1])
sendCommand(v1rc1, restartActivityCmd)
receiveAndCheck(v1rc1, disconnectedStr)
powerOn([v1l1])
idle([v1l1])

writeLog("Item 3b: With V1RC1 held close to V1L1, user initiates a touchlink command on V1RC1. Touchlink should succeed. ")
touchlink(v1rc1, v1l1)
receiveAndCheck(v1rc1, connectedStr)
idle([v1rc1, v1l1])

writeLog("Item 3c: User initiates a turn on command on V1RC1.")
setAddressing(v1rc1, APS_SHORT_ADDRESS, getNwkAddress(v1l1), APP_ENDPOINT_LIGHT)
sendOnCommand(v1rc1)
receiveOnCommand(v1l1)

writeLog("TODO Item 4a: User initiates a frequency agility command on V1RC1 with V1RC1 not in range of V2L1.")
currentChannel = getChannel(v1rc1)
channelMask = getChannelMask(v1rc1)
targetChannel = getNextChannel(channelMask, currentChannel)
writeLog("Current channel: %d; channelMask: %08x" % (currentChannel, channelMask))
writeLog("Target channel: %d" % targetChannel)
check(targetChannel != 0) # Channel mask shall contain more than one channel to pass this test

sendNwkMgmtUpdateReq(v1rc1, targetChannel, 0xFE, 0xFFFD)
writeLog("V1RC1 rejoins the network.")
receiveAndCheck(v1rc1, disconnectedStr)
writeLog("Connected indication on V1RC1")
receiveAndCheck(v1rc1, connectedStr)
idle([v1rc1, v1l1])

writeLog("Item 4b: User initiates a turn on command or a turn off command on V1RC1.")
sendOffCommand(v1rc1)
receiveOffCommand(v1l1)

writeLog("Item 5a: Power off V1L1.Power on V2L1.")
sleep(2)
powerOff([v1l1])
sendCommand(v1rc1, restartActivityCmd)
receiveAndCheck(v1rc1, disconnectedStr)
powerOn([v2l1])
idle([v2l1])

writeLog("Item 6a: User initiates a touchlink command on V1RC1 with V1RC1 held close to V2L1. Touchlink should succeed.")
touchlink(v1rc1, v2l1, TOUCHLINK_COMMISSIONING_SKIPPED_STATUS)
receiveAndCheck(v1rc1, connectedStr)
idle([v1rc1, v2l1])

writeLog("Item 6b: User initiates a turn on command on V1RC1.")
setAddressing(v1rc1, APS_SHORT_ADDRESS, getNwkAddress(v2l1), APP_ENDPOINT_LIGHT)
sendOnCommand(v1rc1)
receiveOnCommand(v2l1)

writeLog("Item 6c: User initiates a turn off command on V1RC1.")
sendOffCommand(v1rc1)
receiveOffCommand(v2l1)

writeLog("Item 6d: Where support is indicated in the PICS, user initiates a toggle command on V1RC1.")
sendToggleCommand(v1rc1)
receiveToggleCommand(v2l1)
