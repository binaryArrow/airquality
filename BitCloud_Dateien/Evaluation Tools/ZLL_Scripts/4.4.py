"""
@testcase
@description 4.4 TP-NWI-TC-04: Classical joining DUT ZED to ZLL network

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
ZR1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
dutZED2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
writeLog("Item P1: Power on ZED1 and ZR1. (Reset devices to FN)")
resetRouterToFN([ZR1])
resetEndDeviceToFN([ZED1])

writeLog("Item P2: User initiates a touchlink command on ZED1 with ZED1 held close to ZR1. Touchlink should succeed")
touchlink(ZED1, ZR1)
idle([ZED1, ZR1])
ZR1NwkAddr = getNwkAddress(ZR1)
writeLog("ZR1 network address - 0x%04X" % ZR1NwkAddr)

writeLog("Item P3: User initiates a turn on command on ZED1")
setAddressing(ZED1, APS_SHORT_ADDRESS, ZR1NwkAddr, APP_ENDPOINT_LIGHT)
sendOnCommand(ZED1)
receiveOnCommand(ZR1)

writeLog("Item P4: User initiates a turn off command on ZED1")
sendOffCommand(ZED1)
receiveOffCommand(ZR1)

#*****************************************************************************************
# Test procedure
#*****************************************************************************************\
writeLog("Item 1: Power on DUT ZED2")
powerOn([dutZED2])
resetEndDeviceToFN([dutZED2])

writeLog("Item 2a: By application specific means, DUT ZED2 performs a classical network \
          scan on the primary channels but finds no networks with associate permit set to TRUE")
nwkAssociation(dutZED2, BC_FAILURE_STATUS, BC_FAILURE_STATUS)
writeLog("Item 2b: DUT ZED2 then performs a classical network scan on the secondary \
          channels but finds no networks with associate permit set to TRUE")
sleep(1)
writeLog("Item 2c: DUT ZED2 may repeat the above scans or simply wait for further instructions")
sleep(1)

writeLog("Item 3: By application specific means, the associate permit of the ZLL network is set to TRUE")
setPermitJoinReq(ZR1, PERMIT_JOIN_DURATION_INFINITE)
receiveSetPermitJoinResp(ZR1, BC_SUCCESS_STATUS)

writeLog("Item 4a: By application specific means, DUT ZED2 performs a classical network scan \
         on the primary channels and finds the ZLL network with associate permit set to TRUE")
sleep(1)
writeLog("Item 4b: DUT ZED2 attempts to associate to the network through ZR1")
sleep(1)
writeLog("Item 4c: ZR1 confirms the association request and allocates a random address to DUT ZED2")
dutZED2NwkAddr = nwkAssociation(dutZED2, BC_SUCCESS_STATUS, BC_SUCCESS_STATUS)
check(dutZED2NwkAddr != None)

writeLog("Item 5: ZR1 transports the network key to DUT ZED2, encrypted with the \
         certification pre-installed link key")
sleep(1)

writeLog("Item 6: DUT ZED2 announces itself on the network")
idle([ZED1, ZR1, dutZED2])
