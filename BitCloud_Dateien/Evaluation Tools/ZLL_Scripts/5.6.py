"""
@testcase
@description 5.6 TP-LLI-TC-05: Touchlink: Non factory new remote, factory new remote

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
from basicCluster import *
sys.path.remove(scriptPath)

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []

configureCommunication()
  
V1RC1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
V2RC1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
V1L1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

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

#*****************************************************************************************
# Test procedure
#*****************************************************************************************\
writeLog("Item 1: Power on V2RC1. (Reset device to FN)")
resetEndDeviceToFN([V2RC1])

writeLog("Item 2: User initiates a touchlink command on V1RC1 with V1RC1 not held close to V2RC1. \
         Touchlink should fail.")
resetBanTable([V1RC1, V2RC1])

V1RC1ExtAddr = getExtAddr(V1RC1)
writeLog("V1RC1 extended address - %016X" % V1RC1ExtAddr)
V2RC1ExtAddr = getExtAddr(V2RC1)
writeLog("V2RC1 extended address - %016X" % V2RC1ExtAddr)

setRssiForExtAddress([V2RC1], V1RC1ExtAddr, touchlinkRssiThreshold - 10)

touchlink(V1RC1, V2RC1, TOUCHLINK_FAILED_STATUS)
idle([V1RC1, V2RC1])

writeLog("Item 3: User initiates a touchlink command on V1RC1 with V1RC1 held close to V2RC1. \
         Touchlink should succeed.")
resetBanTable([V1RC1, V2RC1])
touchlink(V1RC1, V2RC1)
receiveAndCheck(V2RC1, connectedStr)
idle([V1RC1, V2RC1])
V2RC1NwkAddr = getNwkAddress(V2RC1)
writeLog("V2RC1 network address - 0x%04X" % V2RC1NwkAddr)

writeLog("Item 4: User initiates a touchlink command on V2RC1 with V2RC1 held close to V1L1. \
         Touchlink should succeed.")
touchlink(V2RC1, V1L1, TOUCHLINK_COMMISSIONING_SKIPPED_STATUS)
idle([V1RC1, V1L1])

writeLog("Item 5a: User initiates a turn on command on V2RC1.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
sendOnCommand(V2RC1)
receiveOnCommand(V1L1)

writeLog("Item 5b: User initiates a turn off command on V2RC1.")
sendOffCommand(V2RC1)
receiveOffCommand(V1L1)

writeLog("Item 5c: Where support is indicated in the PICS, user initiates a toggle command on V2RC1.")
sendToggleCommand(V2RC1)
receiveToggleCommand(V1L1)

writeLog("Item 6a: User initiates a turn on command on V1RC1.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
sendOnCommand(V1RC1)
receiveOnCommand(V1L1)

writeLog("Item 6b: User initiates a turn off command on V1RC1.")
sendOffCommand(V1RC1)
receiveOffCommand(V1L1)

writeLog("Item 6c: Where support is indicated in the PICS, user initiates a toggle command on V1RC1.")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L1)

idle([V1RC1, V2RC1, V1L1])
