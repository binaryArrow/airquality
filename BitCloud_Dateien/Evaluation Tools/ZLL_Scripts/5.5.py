"""
@testcase
@description 5.5 TP-LLI-TC-04: Touchlink: Non factory new remote, non factory new lamp

@tags
  POSITIVE

@connection dummyPort = router
"""
#*****************************************************************************************
# Import section
#*****************************************************************************************
import sys
sys.path.append(scriptPath)
from common import *
from deviceScanner import *
from onOffCluster import *
from identifyCluster import *
sys.path.remove(scriptPath)

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []

configureCommunication()
  
V1RC1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
V1L1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
V2RC1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
V2L1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
writeLog("Item P1: Power on V1RC1 and V1L1. (Reset device to FN)")
resetEndDeviceToFN([V1RC1])
resetRouterToFN([V1L1])

writeLog("Item P2: With V1RC1 held close to V1L1, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V1L1)
idle([V1RC1, V1L1])
V1L1NwkAddr = getNwkAddress(V1L1)
writeLog("V1L1 network address - 0x%04X" % V1L1NwkAddr)

writeLog("Item P3: User initiates a turn on command on V1RC1.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
sendOnCommand(V1RC1)
receiveOnCommand(V1L1)

writeLog("Item P4: User initiates a turn off command on V1RC1.")
sendOffCommand(V1RC1)
receiveOffCommand(V1L1)

writeLog("Item P5: Where support is indicated in the PICS, \
         user initiates a toggle command on V1RC1.")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L1)

writeLog("Item P6: Power on V2RC1 and V2L1. (Reset device to FN)")
resetEndDeviceToFN([V2RC1])
resetRouterToFN([V2L1])

writeLog("Item P7: With V2RC1 held close to V2L1, user initiates a touchlink command on V2RC1. \
         Touchlink should succeed.")
touchlink(V2RC1, V2L1)
idle([V2RC1, V2L1])
V2L1NwkAddr = getNwkAddress(V2L1)
writeLog("V2L1 network address - 0x%04X" % V2L1NwkAddr)

writeLog("Item P8: User initiates a turn on command on V2RC1.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
sendOnCommand(V2RC1)
receiveOnCommand(V2L1)

writeLog("Item P9: User initiates a turn off command on V2RC1.")
sendOffCommand(V2RC1)
receiveOffCommand(V2L1)

writeLog("Item P10: Where support is indicated in the PICS, \
         user initiates a toggle command on V2RC1.")
sendToggleCommand(V2RC1)
receiveToggleCommand(V2L1)

#*****************************************************************************************
# Test procedure
#*****************************************************************************************\
writeLog("Item 1a: User initiates a touchlink command on V1RC1 with V1RC1 not held close \
         to V2L1. Touchlink should fail.")
resetBanTable([V1RC1, V2L1])

V1RC1ExtAddr = getExtAddr(V1RC1)
writeLog("V1RC1 extended address - %016X" % V1RC1ExtAddr)
V2L1ExtAddr = getExtAddr(V2L1)
writeLog("V2L1 extended address - %016X" % V2L1ExtAddr)

setRssiForExtAddress([V2L1], V1RC1ExtAddr, touchlinkRssiThreshold - 10)

touchlink(V1RC1, V2L1, TOUCHLINK_FAILED_STATUS)
idle([V1RC1, V2L1])

writeLog("Item 1b: User initiates a turn on command or a turn off command on V1RC1.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
sendOnCommand(V1RC1)
sendOffCommand(V1RC1)
idle([V1RC1, V2L1])

writeLog("Item 2a: User initiates a touchlink command on V1RC1 with V1RC1 held close \
         to V2L1. Touchlink should succeed.")
resetBanTable([V1RC1, V2L1])
touchlink(V1RC1, V2L1)
idle([V1RC1, V2L1])
V2L1NwkAddr = getNwkAddress(V2L1)
writeLog("V2L1 network address - 0x%04X" % V2L1NwkAddr)

writeLog("Item 2b: User initiates a turn on command on V1RC1.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
sendOnCommand(V1RC1)
receiveOnCommand(V2L1)

writeLog("Item 2c: User initiates a turn off command on V1RC1.")
sendOffCommand(V1RC1)
receiveOffCommand(V2L1)

writeLog("Item 2d: Where support is indicated in the PICS, \
         user initiates a toggle command on V1RC1.")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L1)

writeLog("Item 3a: User initiates a turn on command on V2RC1.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
sendOnCommand(V2RC1, BC_DISCONNECTED_STATUS)
idle([V2RC1, V2L1])

writeLog("Item 3b: User initiates a turn off command on V2RC1.")
sendOffCommand(V2RC1, BC_FAILURE_STATUS)
idle([V2RC1, V2L1])

writeLog("Item 3c: Where support is indicated in the PICS, \
         user initiates a toggle command on V2RC1.")
sendToggleCommand(V2RC1, BC_FAILURE_STATUS)
idle([V2RC1, V2L1])



