"""
@testcase
@description 4.13 TP-NWI-TC-13: Touchlinking ZLL devices on the same non ZLL network

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
  
ZC = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_NON_ZLL_COORDINATOR, portList)
dutZED1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
ZR1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
writeLog("Item P1: Power on ZC. (Reset device to FN)")
haResetToFN([ZC], BC_SUCCESS_STATUS)
sleep(1)

writeLog("Item P2: By application specific means, ZC forms a non-ZLL network on a primary ZLL channel.")
haRestartNwk(ZC, getFirstChannel(zllPrimaryChannelMask), BC_SUCCESS_STATUS)

writeLog("Item P3: Power on DUT ZED1")
resetEndDeviceToFN([dutZED1])

writeLog("Item P4: By application specific means, the associate permit of the non-ZLL network is set to TRUE.")
setPermitJoinReq(ZC, PERMIT_JOIN_DURATION_INFINITE)
receiveSetPermitJoinResp(ZC, BC_SUCCESS_STATUS)

writeLog("Item P5: By application specific means, the associate permit of the non-ZLL \
         network is set to TRUE.")
dutZED1NwkAddr = nwkAssociation(dutZED1, BC_SUCCESS_STATUS, BC_SUCCESS_STATUS)
check(dutZED1NwkAddr != None)

writeLog("Item P6: DUT ZED1 attempts to associate to the network through ZC")
sleep(1)
writeLog("Item P7: ZC confirms the association request and allocates a random address to DUT ZED1")
sleep(1)
writeLog("Item P8: ZC transports the network key to DUT ZED1, encrypted with the default \
         trust centre link key.")
sleep(1)

writeLog("Item P9: DUT ZED1 announces itself on the network")
setPermitJoinReq(ZC, PERMIT_JOIN_DURATION_ZERO)
receiveSetPermitJoinResp(ZC, BC_SUCCESS_STATUS)
idle([ZC, dutZED1])

writeLog("Item P10: Power on ZR1. (Reset devices to FN)")
resetRouterToFN([ZR1])

writeLog("Item P11: By application specific means, the associate permit of the non-ZLL network is set to TRUE.")
setPermitJoinReq(ZC, PERMIT_JOIN_DURATION_INFINITE)
receiveSetPermitJoinResp(ZC, BC_SUCCESS_STATUS)

writeLog("Item P12: By application specific means, ZR1 performs a classical network scan \
         on the primary channels and finds the non-ZLL network with associate permit set to TRUE.")
ZR1NwkAddr = nwkAssociation(ZR1, BC_SUCCESS_STATUS, BC_SUCCESS_STATUS)
check(ZR1NwkAddr != None)

writeLog("Item P13: ZR1 attempts to associate to the network through ZC")
sleep(1)
writeLog("Item P14: ZC confirms the association request and allocates a random address to ZR1")
sleep(1)
writeLog("Item P15: ZC transports the network key to ZR1, encrypted with the default \
         trust centre link key.")
sleep(1)

writeLog("Item P16: ZR1 announces itself on the network")
setPermitJoinReq(ZC, PERMIT_JOIN_DURATION_ZERO)
receiveSetPermitJoinResp(ZC, BC_SUCCESS_STATUS)
idle([ZC, ZR1])

#*****************************************************************************************
# Test procedure
#*****************************************************************************************\
writeLog("Item 1a: User initiates touch-link operation on DUT ZED1 with DUT ZED1 held close \
         to ZR1 (10cm apart). DUT ZED1 performs a touchlink discovery at 0dBm nominal output \
         power, and enables its receiver for at least aplcScanTimeBaseDuration seconds.\
         This is repeated 5 times on the first primary ZLL channel, then once on each of \
         the remaining primary ZLL channels in turn. After this, as the DUT ZED1 is on a non \
         ZLL network, it repeats the scan on each of the secondary ZLL channels in turn.")
writeLog("Item 1b: ZR1 responds to the scan back to DUT ZED1.")
writeLog("Item 2a: Optional: DUT ZED1 requests ZR1 identify itself.")
writeLog("Item 2b: Conditional on step 2a being invoked: ZR1 receives identify request from \
         DUT ZED1 and identifies itself.")
writeLog("Item 3a: Optional: DUT ZED1 adds ZR1 to a group for subsequent control.")
writeLog("Item 3b: ZR1 receives the request to add itself to a group and responds back to DUT ZED1.")
touchlink(dutZED1, ZR1, TOUCHLINK_COMMISSIONING_SKIPPED_STATUS)
idle([dutZED1, ZR1])
ZR1NwkAddr = getNwkAddress(ZR1)
writeLog("ZR1 network address - 0x%04X" % ZR1NwkAddr)

writeLog("Item 4a: User initiates a turn on command on DUT ZED1.")
setAddressing(dutZED1, APS_SHORT_ADDRESS, ZR1NwkAddr, APP_ENDPOINT_LIGHT)
sendOnCommand(dutZED1)
receiveOnCommand(ZR1)

writeLog("Item 4b: User initiates a turn off command on DUT ZED1.")
sendOffCommand(dutZED1)
receiveOffCommand(ZR1)

idle([ZC, dutZED1, ZR1])
