"""
@testcase
@description 5.4 TP-LLI-TC-03: Touchlink: Non factory new remote, factory new lamp

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
resetRouterToFN([v1l1])
resetRouterToFN([v2l1])
resetEndDeviceToFN([v1rc1])
clearPorts([v1rc1, v1l1, v2l1])

writeLog("Resetting mac ban table")
resetBanTable([v1rc1, v1l1, v2l1])

v1rc1ExtAddr = getExtAddr(v1rc1)
writeLog("v1rc1 extended address - %016X" % v1rc1ExtAddr)

v1l1ExtAddr = getExtAddr(v1l1)
v1l1NwkAddr = getNwkAddress(v1l1)
writeLog("v1l1 extended address - %016X" % v1l1ExtAddr)

v2l1ExtAddr = getExtAddr(v2l1)
v2l1NwkAddr = getNwkAddress(v2l1)
writeLog("v1l1 extended address - %016X" % v2l1ExtAddr)

writeLog("P2: With V1RC1 held close to V1L1, user initiates a touchlink command on V1RC1. Touchlink should succeed.")
touchlink(v1rc1, v1l1)
idle([v1rc1, v1l1])

writeLog("1a: User initiates a touchlink command on V1RC1 with V1RC1 not held close to V2L1. Touchlink should fail.")
writeLog("Change link quality between v2l1 and v1rc1")
setRssiForExtAddress([v2l1], v1rc1ExtAddr, touchlinkRssiThreshold - 10)
sendCommand(v1rc1, touchlickCmd)
idle([v1rc1, v2l1, v1l1])

writeLog("Item 1b: User initiates a turn on command or a turn off command on V2RC1.")
setAddressing(v1rc1, APS_SHORT_ADDRESS, v2l1NwkAddr, APP_ENDPOINT_LIGHT)
sendCommand(v1rc1, "onOff %d" % ZCL_ONOFF_CLUSTER_TOGGLE_COMMAND_ID)
idle([v1rc1, v2l1, v1l1])



writeLog("Revert link quality between v2l1 and v2rc1")
resetBanTable([v2l1])

writeLog("Item 2a: User initiates a touchlink command on V1RC1 with V1RC1 held close to V2L1. Touchlink should succeed.")
touchlink(v1rc1, v2l1)
idle([v1rc1, v2l1])

writeLog("Item 2b: User initiates a turn on command on V1RC1.")
setAddressing(v1rc1, APS_SHORT_ADDRESS, getNwkAddress(v2l1), APP_ENDPOINT_LIGHT)
sendOnCommand(v1rc1)
receiveOnCommand(v2l1)

writeLog("Item 2c: User initiates a turn off command on V1RC1.")
sendOffCommand(v1rc1)
receiveOffCommand(v2l1)

writeLog("Item 2d: Where support is indicated in the PICS, user initiates a toggle command on V1RC1.")
sendToggleCommand(v1rc1)
receiveToggleCommand(v2l1)
