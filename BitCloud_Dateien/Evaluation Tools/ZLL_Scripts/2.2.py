"""
@testcase
@description 2.1 TP-PRE-TC-01: Network start - ZED & ZR factory new

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
writeLog("5 Device info request indication on R1 (Ommited as optional)")
writeLog("6 Device info response indication on ED1 (Ommited as optional)")
writeLog("7, 8 Identify request indication on R1")
receiveAndCheck(r1, identifyReqIndStr)
writeLog("9 Network Start request indication on R1")
receiveAndCheck(r1, startNwkReqIndStr)
writeLog("10a ZR1 performs a network discovery (Ommited as optional)")
writeLog("10b ZR1 issues network start response (Shall be checked by a sniffer)")
writeLog("10c ZR1 announces itself on the network (Shall be checked by a sniffer)")
writeLog("Join indication on R1")
receiveAndCheck(r1, joinDoneStr)
writeLog("Connected indication on R1")
receiveAndCheck(r1, connectedStr)
writeLog("11a Network start response indication on ED1")
receiveAndCheck(ed1, startNwkRespIndStr)
writeLog("11b Join indication on ED1")
receiveAndCheck(ed1, joinDoneStr)
writeLog("Connected indication on ED1")
receiveAndCheck(ed1, connectedStr)
writeLog("12a ED1 announces itself on the network (Shall be checked by a sniffer)")
writeLog("12b R1  rebroadcasts announce from ED1 (Shall be checked by a sniffer)")
idle([ed1, r1, r2])

writeLog("Revert link quality between R2 and ED1")
resetBanTable([r2])
setTargetType(r2, TARGET_TYPE_TOUCHLINK)
sleep(2)

writeLog("13 ED1 carries out a touchlink operation to R2")
sendCommand(ed1, touchlickCmd)
writeLog("Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Identify request indication on R2")
receiveAndCheck(r2, identifyReqIndStr)
writeLog("Network join router request indication on R2")
receiveAndCheck(r2, networkJoinRouterReqStr)
writeLog("Join indication on R2")
receiveAndCheck(r2, joinDoneStr)
writeLog("Connected indication on R2")
receiveAndCheck(r2, connectedStr)
writeLog("Network join router response indication on ED1")
receiveAndCheck(ed1, networkJoinRouterRespStr)
idle([ed1, r1, r2])

writeLog("Set R1 as target")
setTargetType(r1, TARGET_TYPE_TOUCHLINK)
sleep(2)

writeLog("14a ED1 performs scanning to locate ZR1")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_HYBRID)
writeLog("14b Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("14c Perform reset to FN request")
sendCommand(ed1, resetDeviceToFnCmd)
receiveAndCheck(ed1, doneStr)
writeLog("15 ZR1 resets network parameters and performs a warm-boot")
receiveAndCheck(r1, discoveryFailedStr)
sendCommand(ed1, restartActivityCmd)
receiveAndCheck(ed1, disconnectedStr)
receiveAndCheck(ed1, connectedStr)
idle([ed1, r1])

writeLog("16a ED1 performs scanning to locate ZR1")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_TOUCHLINK)
writeLog("16b Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("16c ED1 requests ZR1 to identify itself for a period of 10s (identifyDuration = 10)")
sendCommand(ed1, identifyDeviceCmd % 10)
receiveAndCheck(ed1, doneStr)
writeLog("16d Identify request indication on R1")
receiveAndCheck(r1, identifyReqIndStr)
idle([ed1, r1])

writeLog("17a ED1 performs scanning to locate ZR1")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_TOUCHLINK)
writeLog("17b Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("17c Perform identify request with identifyDuration = 0xFFFF")
sendCommand(ed1, identifyDeviceCmd % vendorDefinedIdentifyDuration)
receiveAndCheck(ed1, doneStr)
writeLog("17d Identify request indication on R1")
receiveAndCheck(r1, identifyReqIndStr)
idle([ed1, r1])

writeLog("18a ED1 performs scanning to locate ZR1")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_TOUCHLINK)
writeLog("18b Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("18c ED1 requests ZR1 to identify itself for a period of 10s (identifyDuration = 10)")
sendCommand(ed1, identifyDeviceCmd % 10)
receiveAndCheck(ed1, doneStr)
writeLog("18d Identify request indication on R1")
receiveAndCheck(r1, identifyReqIndStr)
sleep(2)
writeLog("18e ED1 requests ZR1 to stop identifying itself (identifyDuration = 0)")
sendCommand(ed1, identifyDeviceCmd % 0)
receiveAndCheck(ed1, doneStr)
writeLog("Identify request indication on R1")
receiveAndCheck(r1, identifyReqIndStr)
idle([ed1, r1])
