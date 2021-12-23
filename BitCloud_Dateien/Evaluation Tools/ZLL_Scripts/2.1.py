"""
@testcase
@description 2.1 TP-PRE-TC-00: Network start - ZED & ZR factory new

@tags
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
sys.path.remove(scriptPath)

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []

configureCommunication()

ed1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
ed2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
r1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
r2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
#Script body - feature checking
#*****************************************************************************************
writeLog("Resetting nodes to FN")
resetRouterToFN([r1, r2])
resetEndDeviceToFN([ed1, ed2])
clearPorts([r1, r2, ed1, ed2])

writeLog("Resetting mac ban table")
resetBanTable([r1, r2, ed1, ed2])

ed1ExtAddr = getExtAddr(ed1)
writeLog("ED1 extended address - %016X" % ed1ExtAddr)

ed2ExtAddr = getExtAddr(ed2)
writeLog("ED2 extended address - %016X" % ed2ExtAddr)

r1ExtAddr = getExtAddr(r1)
writeLog("R1 extended address - %016X" % r1ExtAddr)

r2ExtAddr = getExtAddr(r2)
writeLog("R2 extended address - %016X" % r1ExtAddr)

writeLog("Change link quality between R1, R2, ED2 and ED1")
setRssiForExtAddress([r1, r2, ed2], ed1ExtAddr, touchlinkRssiThreshold - 10)

setTargetType(r1, TARGET_TYPE_TOUCHLINK)
sleep(2)

writeLog("2a Start touchlink ED1 to R1")
sendCommand(ed1, touchlickCmd)
writeLog("2b No scan response indication on ED1")
idle([ed1, r1, r2])

writeLog("Revert link quality between R1 and ED1")
resetBanTable([r1])
setTargetType(r1, TARGET_TYPE_TOUCHLINK)
sleep(2)

writeLog("3 Start touchlink ED1 to R1")
sendCommand(ed1, touchlickCmd)
writeLog("4 Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
