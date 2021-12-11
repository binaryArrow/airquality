"""
@testcase
@description 2.5 TP-PRE-TC-05: Network start - ZED1 not factory new & ZED2 factory new

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
powerOff([ed1, r2])

#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 Power on ED2")
powerOn([ed2])

writeLog("Resetting mac ban table on ED2")
resetBanTable([ed2])
writeLog("Set bad link quality between ED2 and ED1")
setRssiForExtAddress([ed2], ed1ExtAddr, touchlinkRssiThreshold - 10)

writeLog("2a Power on ED1")
powerOn([ed1])
writeLog("2b ED1 attempts to join its previous network (Shall be checked by a sniffer)")

writeLog("3a ED2 enables its receiver")
setTargetType(ed2, TARGET_TYPE_TOUCHLINK)
writeLog("3b Start touchlink ED1 to ED2")
sendCommand(ed1, touchlickCmd)
writeLog("3c No scan response indication on ED1")
idle([ed1, ed2])

writeLog("Set good link quality between ED1 and ED2")
resetBanTable([ed2])

writeLog("4a ED2 enables its receiver")
setTargetType(ed2, TARGET_TYPE_TOUCHLINK)
writeLog("4b Start touchlink ED1 to ED2")
sendCommand(ed1, touchlickCmd)
writeLog("5 Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("6 Device info request indication on ED2 (Ommited as optional)")
writeLog("7 Device info response indication on ED1 (Ommited as optional)")
writeLog("8, 9 Identify request indication on R1")
receiveAndCheck(ed2, identifyReqIndStr)
writeLog("10 Network Join EndDevice request indication on ED2")
receiveAndCheck(ed2, networkJoinEndDeviceReqStr)
writeLog("Join indication on ED2")
receiveAndCheck(ed2, joinDoneStr)
writeLog("11a ED2 issues network join router response (Shall be checked by a sniffer)")
writeLog("11a ED2 attempts to join given network (Shall be checked by a sniffer)")
writeLog("12 Network join EndDevice response indication on ED1")
receiveAndCheck(ed1, disconnectedStr)
receiveAndCheck(ed1, networkJoinEndDeviceRespStr)
idle([ed1, ed2])

writeLog("13 ED1 carries out a touchlink operation to further device (Ommited as optional)")

writeLog("14a ED2 enables its receiver")
setTargetType(ed2, TARGET_TYPE_TOUCHLINK)
sleep(1)
writeLog("14b ED1 performs scanning to locate ED2")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_TOUCHLINK)
writeLog("14c Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("14d Perform reset to FN request")
sendCommand(ed1, resetDeviceToFnCmd)
receiveAndCheck(ed1, doneStr)
writeLog("15 ED2 resets network parameters and performs a warm-boot")
idle([ed1, ed2])

writeLog("16a ED2 enables its receiver")
setTargetType(ed2, TARGET_TYPE_TOUCHLINK)
writeLog("16b ED1 performs scanning to locate ED2")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_TOUCHLINK)
writeLog("16c Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("16d ED1 requests ED2 to identify itself for a period of 10s (identifyDuration = 10)")
sendCommand(ed1, identifyDeviceCmd % 10)
receiveAndCheck(ed1, doneStr)
writeLog("16e Identify request indication on ED2")
receiveAndCheck(ed2, identifyReqIndStr)
idle([ed1, ed2])

writeLog("17a ED2 enables its receiver")
setTargetType(ed2, TARGET_TYPE_TOUCHLINK)
writeLog("17b ED1 performs scanning to locate ED2")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_TOUCHLINK)
writeLog("17c Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("17d Perform identify request with identifyDuration = 0xFFFF")
sendCommand(ed1, identifyDeviceCmd % vendorDefinedIdentifyDuration)
receiveAndCheck(ed1, doneStr)
writeLog("17e Identify request indication on ED2")
receiveAndCheck(ed2, identifyReqIndStr)
idle([ed1, ed2])

writeLog("18a ED2 enables its receiver")
setTargetType(ed2, TARGET_TYPE_TOUCHLINK)
writeLog("18b ED1 performs scanning to locate ED2")
sendCommand(ed1, performScanCmd % INITIATOR_SCAN_TYPE_TOUCHLINK)
writeLog("18c Scan response indication on ED1")
receiveAndCheck(ed1, scanRespIndStr)
writeLog("Scan request done")
receiveAndCheck(ed1, scanDoneStr)
receiveAndCheck(ed1, statusStr % 0)
receiveAndCheck(ed1, deviceAmountStr % 1)
writeLog("18d ED1 requests ZR1 to identify itself for a period of 10s (identifyDuration = 10)")
sendCommand(ed1, identifyDeviceCmd % 10)
receiveAndCheck(ed1, doneStr)
writeLog("18e Identify request indication on ED2")
receiveAndCheck(ed2, identifyReqIndStr)
sleep(2)
writeLog("18f ED1 requests ZR1 to stop identifying itself (identifyDuration = 0)")
sendCommand(ed1, identifyDeviceCmd % 0)
receiveAndCheck(ed1, doneStr)
writeLog("Identify request indication on ED2")
receiveAndCheck(ed2, identifyReqIndStr)
idle([ed1, ed2])
