"""
@testcase
@description 2.3 TP-PRE-TC-03: Network start - ZED not factory new & ZR factory new

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

r1ExtPanId = 0x0000000000000001
r2ExtPanId = 0x0000000000000002

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
# Test preparation
#*****************************************************************************************\
resetRouterToFN([r1, r2])
resetEndDeviceToFN([ed1, ed2])
clearPorts([r1, r2, ed1, ed2])
powerOff([r1, r2, ed1, ed2])

ed1ExtAddr = getExtAddr(ed1)
writeLog("ED1 extended address - %016X" % ed1ExtAddr)

ed2ExtAddr = getExtAddr(ed2)
writeLog("ED2 extended address - %016X" % ed2ExtAddr)

r1ExtAddr = getExtAddr(r1)
writeLog("R1 extended address - %016X" % r1ExtAddr)

r2ExtAddr = getExtAddr(r2)
writeLog("R2 extended address - %016X" % r2ExtAddr)

writeLog("P1 Power on ED1 and R2")
powerOn([ed1, r2])

writeLog("P2 Initiate touchlink on ED1 with R2")
touchlink(ed1, r2)
idle([ed1, r2])

writeLog("P3 Power off ED1 and R2")
resetRouterToFN([r2])
powerOff([ed1, r2])

#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 Power on R1")
powerOn([r1])

writeLog("Resetting mac ban table on R1")
resetBanTable([r1])
writeLog("Set bad link quality between R1 and ED1")
setRssiForExtAddress([r1], ed1ExtAddr, touchlinkRssiThreshold - 10)

writeLog("2a Power on ED1")
powerOn([ed1])
writeLog("2b ED1 attempts to join its previous network (Shall be checked by a sniffer)")

writeLog("3a Start touchlink ED1 to R1")
sendCommand(ed1, touchlickCmd)
writeLog("3b No scan response indication on ED1")
idle([ed1, r1])

writeLog("Revert link quality between R1 and ED1")
resetBanTable([r1])
setTargetType(r1, TARGET_TYPE_TOUCHLINK)
sleep(2)

writeLog("4 Start touchlink ED1 to R1")
setTargetType(r1, TARGET_TYPE_TOUCHLINK)
sendCommand(ed1, touchlickCmd)
writeLog("5 Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("6 Device info request indication on R1 (Ommited as optional)")
writeLog("7 Device info response indication on ED1 (Ommited as optional)")
writeLog("8, 9 Identify request indication on R1")
receiveAndCheck(r1, identifyReqIndStr)
writeLog("10 Network Join Router request indication on R1")
receiveAndCheck(r1, networkJoinRouterReqStr)
writeLog("11a ZR1 issues network join router response (Shall be checked by a sniffer)")
writeLog("Join indication on R1")
receiveAndCheck(r1, joinDoneStr)
writeLog("Connected indication on R1")
receiveAndCheck(r1, connectedStr)
writeLog("11b Network join router response indication on ED1")
receiveString = receiveNextStr(ed1)
check(receiveString in [networkJoinRouterRespStr, disconnectedStr])
receiveString = receiveNextStr(ed1)
check(receiveString in [networkJoinRouterRespStr, disconnectedStr])
writeLog("11c ZR1 announces itself on the network (Shall be checked by a sniffer)")
writeLog("12a, 12b Join indication on ED1")
writeLog("Connected indication on ED1")
receiveAndCheck(ed1, connectedStr)
writeLog("13a ED1 announces itself on the network (Shall be checked by a sniffer)")
writeLog("13b R1 rebroadcasts announce from ED1 (Shall be checked by a sniffer)")
idle([ed1, r1])

writeLog("Power on R2")
powerOn([r2])
writeLog("Resetting mac ban table on R2")
resetBanTable([r2])
setTargetType(r2, TARGET_TYPE_TOUCHLINK)
sleep(2)

writeLog("14 ED1 carries out a touchlink operation to R2")
sendCommand(ed1, touchlickCmd)
sleep(2)
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

sleep(2)

writeLog("Set R1 as target")
setTargetType(r1, TARGET_TYPE_TOUCHLINK)
sleep(2)
writeLog("15a ED1 performs scanning to locate ZR1")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_TOUCHLINK)
writeLog("15b Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("15c Perform reset to FN request")
sendCommand(ed1, resetDeviceToFnCmd)
receiveAndCheck(ed1, doneStr)
sleep(2)
writeLog("16 ZR1 resets network parameters and performs a warm-boot")
receiveAndCheck(r1, discoveryFailedStr)
sendCommand(ed1, restartActivityCmd)
receiveAndCheck(ed1, disconnectedStr)
receiveAndCheck(ed1, connectedStr)
idle([ed1, r1])
sleep(2)
writeLog("17a ED1 performs scanning to locate ZR1")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_TOUCHLINK)
writeLog("17b Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("17c ED1 requests ZR1 to identify itself for a period of 10s (identifyDuration = 10)")
sendCommand(ed1, identifyDeviceCmd % 10)
receiveAndCheck(ed1, doneStr)
writeLog("17d Identify request indication on R1")
receiveAndCheck(r1, identifyReqIndStr)
idle([ed1, r1])
sleep(2)
writeLog("18a ED1 performs scanning to locate ZR1")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_TOUCHLINK)
writeLog("18b Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("18c Perform identify request with identifyDuration = 0xFFFF")
sendCommand(ed1, identifyDeviceCmd % vendorDefinedIdentifyDuration)
receiveAndCheck(ed1, doneStr)
writeLog("18d Identify request indication on R1")
receiveAndCheck(r1, identifyReqIndStr)
idle([ed1, r1])
sleep(2)
writeLog("19a ED1 performs scanning to locate ZR1")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_TOUCHLINK)
writeLog("19b Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("19c ED1 requests ZR1 to identify itself for a period of 10s (identifyDuration = 10)")
sendCommand(ed1, identifyDeviceCmd % 10)
receiveAndCheck(ed1, doneStr)
writeLog("19d Identify request indication on R1")
receiveAndCheck(r1, identifyReqIndStr)
sleep(2)
writeLog("19e ED1 requests ZR1 to stop identifying itself (identifyDuration = 0)")
sendCommand(ed1, identifyDeviceCmd % 0)
receiveAndCheck(ed1, doneStr)
writeLog("Identify request indication on R1")
receiveAndCheck(r1, identifyReqIndStr)
idle([ed1, r1])
