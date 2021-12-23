"""
@testcase
@description 5.2 TP-LLI-TC-01: Touchlink: Factory new remote, factory new lamp

@tags
  INTEROPERABILITY
  CHAPTER_5
  TOUCHLINK
  POSITIVE

@connection dummyPort = router
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
v2l1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
#Script body - feature checking
#*****************************************************************************************
writeLog("Item 1: Resetting nodes to FN")
resetRouterToFN([v2l1])
resetEndDeviceToFN([v1rc1])
clearPorts([v1rc1, v2l1])

writeLog("Resetting mac ban table")
resetBanTable([v1rc1, v2l1])

v1rc1ExtAddr = getExtAddr(v1rc1)
writeLog("v1rc1 extended address - %016X" % v1rc1ExtAddr)

v2l1ExtAddr = getExtAddr(v2l1)
v2l1NwkAddr = getNwkAddress(v2l1)
writeLog("v2l1 extended address - %016X" % v2l1ExtAddr)

writeLog("Change link quality between v2l1 and v1rc1")
setRssiForExtAddress([v2l1], v1rc1ExtAddr, touchlinkRssiThreshold - 10)

writeLog("Item 2a: Start touchlink v1rc1 to v2l1")
sendCommand(v1rc1, touchlickCmd)
writeLog("Item 2a: No scan response indication on ED1")
idle([v1rc1, v2l1])

writeLog("Item 2b: User initiates a turn on command on v1rc1")
setAddressing(v1rc1, APS_SHORT_ADDRESS, v2l1NwkAddr, APP_ENDPOINT_LIGHT)
sendToggleCommandErr(v1rc1)

writeLog("Revert link quality between v2l1 and v1rc1")
resetBanTable([v2l1, v1rc1])

writeLog("Item 3a: User initiates a touchlink command on V1v1rc1 with V1v1rc1 held close to V2v2l1.Touchlink should succeed. ")
touchlink(v1rc1, v2l1)
idle([v1rc1, v2l1])

writeLog("Item 3b: User initiates a turn on command on V1v1rc1.")
setAddressing(v1rc1, APS_SHORT_ADDRESS, getNwkAddress(v2l1), APP_ENDPOINT_LIGHT)
sendOnCommand(v1rc1)
receiveOnCommand(v2l1)

writeLog("Item 3c: User initiates a turn off command on V1v1rc1.")
sendOffCommand(v1rc1)
receiveOffCommand(v2l1)

writeLog("Item 3d: Where support is indicated in the PICS, user initiates a toggle command on V1v1rc1.")
sendToggleCommand(v1rc1)
receiveToggleCommand(v2l1)
