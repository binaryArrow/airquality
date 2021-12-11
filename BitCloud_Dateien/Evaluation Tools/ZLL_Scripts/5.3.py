"""
@testcase
@description 5.3 TP-LLI-TC-02: Touchlink: Factory new remote, non factory new lamp

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
v2rc1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)

#*****************************************************************************************
#Script body - feature checking
#*****************************************************************************************
writeLog("P1: Power on V1RC1 and V1L1. Resetting nodes to FN")
resetRouterToFN([v1l1])
resetEndDeviceToFN([v1rc1])
resetEndDeviceToFN([v2rc1])
clearPorts([v1rc1, v1l1, v2rc1])

writeLog("Resetting mac ban table")
resetBanTable([v1rc1, v1l1, v2rc1])

v1rc1ExtAddr = getExtAddr(v1rc1)
writeLog("v1rc1 extended address - %016X" % v1rc1ExtAddr)

v2rc1ExtAddr = getExtAddr(v2rc1)
writeLog("v2rc1 extended address - %016X" % v2rc1ExtAddr)

v1l1ExtAddr = getExtAddr(v1l1)
v1l1NwkAddr = getNwkAddress(v1l1)
writeLog("v1l1 extended address - %016X" % v1l1ExtAddr)

writeLog("P2: With V1RC1 held close to V1L1, user initiates a touchlink command on V1RC1. Touchlink should succeed.")
touchlink(v1rc1, v1l1)
idle([v1rc1, v1l1])

writeLog("1a: User initiates a touchlink command on V2RC1 with V2RC1 not held close to V1L1. Touchlink should fail.")
writeLog("Change link quality between v2l1 and v1rc1")
setRssiForExtAddress([v1l1], v2rc1ExtAddr, touchlinkRssiThreshold - 10)
sendCommand(v1rc1, touchlickCmd)
idle([v1rc1, v2rc1, v1l1])

writeLog("Item 1b: User initiates a turn on command or a turn off command on V2RC1.")
setAddressing(v2rc1, APS_SHORT_ADDRESS, v1l1NwkAddr, APP_ENDPOINT_LIGHT)
sendToggleCommandErr(v2rc1)


writeLog("Revert link quality between v1l1 and v2rc1")
resetBanTable([v1l1])

writeLog("Item 2a: User initiates a touchlink command on V2RC1 with V2RC1 held close to V1L1. Touchlink should succeed.")
touchlink(v2rc1, v1l1)
idle([v2rc1, v1l1])

writeLog("Item 2b: User initiates a turn on command on V2RC1.")
setAddressing(v2rc1, APS_SHORT_ADDRESS, getNwkAddress(v1l1), APP_ENDPOINT_LIGHT)
sendOnCommand(v2rc1)
receiveOnCommand(v1l1)

writeLog("Item 2c: User initiates a turn off command on V2RC1.")
sendOffCommand(v2rc1)
receiveOffCommand(v1l1)

writeLog("Item 2d: Where support is indicated in the PICS, user initiates a toggle command on V2RC1.")
sendToggleCommand(v2rc1)
receiveToggleCommand(v1l1)
