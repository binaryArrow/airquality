"""
@testcase
@description 4.7 TP-NWI-TC-07: Classical joining ZR to DUT ZR on ZLL network

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
  
ZED1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
dutZR1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
ZR2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
writeLog("Item P1: Power on ZED1 and DUT ZR1. (Reset devices to FN)")
resetRouterToFN([dutZR1])
resetEndDeviceToFN([ZED1])

writeLog("Item P2: User initiates a touchlink command on ZED1 with ZED1 held close to DUT ZR1. Touchlink should succeed")
touchlink(ZED1, dutZR1)
idle([ZED1, dutZR1])
ZR1NwkAddr = getNwkAddress(dutZR1)
writeLog("DUT ZR1 network address - 0x%04X" % ZR1NwkAddr)

writeLog("Item P3: User initiates a turn on command on ZED1")
setAddressing(ZED1, APS_SHORT_ADDRESS, ZR1NwkAddr, APP_ENDPOINT_LIGHT)
sendOnCommand(ZED1)
receiveOnCommand(dutZR1)

writeLog("Item P4: User initiates a turn off command on ZED1")
sendOffCommand(ZED1)
receiveOffCommand(dutZR1)

#*****************************************************************************************
# Test procedure
#*****************************************************************************************\
writeLog("Item 1: Power on ZR2")
powerOn([ZR2])
resetRouterToFN([ZR2])

writeLog("Item 2a: By application specific means, ZR2 performs a classical network \
          scan on the primary channels but finds no networks with associate permit set to TRUE")
sleep(1)
writeLog("Item 2b: ZR2 then performs a classical network scan on the secondary \
          channels but finds no networks with associate permit set to TRUE")
sleep(1)
writeLog("Item 2c: ZR2 may repeat the above scans or simply wait for further instructions")
sleep(1)

writeLog("Item 3: By application specific means, the associate permit of the ZLL network is set to TRUE")
setPermitJoinReq(dutZR1, PERMIT_JOIN_DURATION_INFINITE)
receiveSetPermitJoinResp(dutZR1, BC_SUCCESS_STATUS)

writeLog("Item 4a: By application specific means, ZR2 performs a classical network scan \
         on the primary channels and finds the ZLL network with associate permit set to TRUE")
sleep(1)
writeLog("Item 4b: ZR2 attempts to associate to the network through DUT ZR1")
sleep(1)
writeLog("Item 4c: DUT ZR1 confirms the association request and allocates a random address to ZR2")
dutZED2NwkAddr = nwkAssociation(ZR2, BC_SUCCESS_STATUS, BC_SUCCESS_STATUS)
check(dutZED2NwkAddr != None)

writeLog("Item 5: DUT ZR1 transports the network key to ZR2, setting the source address field to \
         0xffffffffffffffff and encrypted with the certification pre-installed link key")
sleep(1)

writeLog("Item 6: ZR2 announces itself on the network")
idle([ZED1, dutZR1, ZR2])
