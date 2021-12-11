"""
@testcase
@description 2.6 TP-PRE-TC-06: Frequency agility

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
# Test preparation
#*****************************************************************************************\
resetRouterToFN([r1, r2])
resetEndDeviceToFN([ed1, ed2])
clearPorts([r1, r2, ed1, ed2])
powerOff([r1, r2, ed1, ed2])

ed1ExtAddr = getExtAddr(ed1)
writeLog("ED1 extended address - %016X" % ed1ExtAddr)

r1ExtAddr = getExtAddr(r1)
writeLog("R1 extended address - %016X" % r1ExtAddr)

r2ExtAddr = getExtAddr(r2)
writeLog("R2 extended address - %016X" % r1ExtAddr)

writeLog("P1 Power on ED1 and R1")
powerOn([ed1, r1])

writeLog("P2 Initiate touchlink on ED1 with R1")
touchlink(ed1, r1)
idle([ed1, r1])

writeLog("P3 Power off ED1 and R1")
powerOff([ed1, r1])

#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1a Power on ZR1")
powerOn([r1])
writeLog("1b ZR1 announces itself (Shall be checked by a sniffer")

writeLog("2a Power on ED1")
sendCommand(ed1, resetCmd)
writeLog("2b,2c,2d ED1 rejoins its previous network (Shall be checked by a sniffer)")
receiveAndCheck(ed1, connectedStr)
idle([ed1, r1])

currentChannel = getChannel(ed1)
channelMask = getChannelMask(ed1)
targetChannel = getNextChannel(channelMask, currentChannel)
check(targetChannel != 0) # Channel mask shall contain more than one channel to pass this test
writeLog("Current channel: %d; channelMask: %08x" % (currentChannel, channelMask))
writeLog("Target channel: %d" % targetChannel)

sleep(5)

writeLog("3 ED1 broadcasts MgmtNwkUpdateReq to all RxOnWhenIdle devices")
sendNwkMgmtUpdateReq(ed1, targetChannel, 0xFE, 0xFFFD)
writeLog("4 R1 changes its channel")
writeLog("5a, 5b ED1 rejoins the network")
writeLog("Disconnected indication on ED1")
receiveAndCheck(ed1, disconnectedStr)
writeLog("Connected indication on ED1")
receiveAndCheck(ed1, connectedStr)
